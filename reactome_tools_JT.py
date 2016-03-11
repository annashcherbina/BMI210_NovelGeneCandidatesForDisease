import MySQLdb as mdb
import pandas as pd
import argparse
import sys

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)[1]
print sys.argv[1:len(sys.argv)]


#parser = argparse.ArgumentParser(description='Process the genes required.')
#parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                   help='an integer for the accumulator')
#parser.add_argument('--sum', dest='accumulate', action='store_const',
#                   const=sum, default=max,
#                   help='sum the integers (default: find the max)')

#args = parser.parse_args()
#print(args.accumulate(args.integers))




pd.set_option('max_colwidth',100)

def get_cursor():
    """ gets MySQLdb cursor to access database """
    db = mdb.connect('bmi210project.czxrvyi7olca.us-west-1.rds.amazonaws.com', 'bmi210project', 'bmi210project', 'bmi210project', 3306)
    return db.cursor()

def get_reaction_from_reactionid(c, reactionId):
    """ gets name of reaction from reaction id """
    nrows = c.execute('select * from ReactionLikeEvent where id=%d' % reactionId)
    if nrows == 0:
        raise ValueError('ReactionLikeEvent ID %d not valid' % reactionId)
    else:
        return c.fetchall()[0][1]

def get_entityids_from_entityname(c, entityName):
    """ gets all possible entity ids corresponding to an entity name """
    nrows = c.execute('select * from PhysicalEntity where lower(displayName) like lower(\'%%%s%%\') and species=\'Homo sapiens\';' % entityName)
    if nrows == 0:
        raise ValueError('Could not find PhysicalEntity matching \'%s\'' % entityName)
    else:
        result = [row[0] for row in c.fetchall() if row[2] == 'Homo sapiens' and \
                   row[3] in ['GenomeEncodedEntity', 'EntityWithAccessionedSequence']]
        if not result:
            raise ValueError('Could not find human gene or protein matching \'%s\'' % entityName)
        return result
    
def get_entityid_from_uniprot(c, uniprotId):
    """ gets entity id corresponding to a UniProt id """
    nrows = c.execute('select * from Id_To_ExternalIdentifier where externalIdentifier=\'%s\' and referenceDatabase=\'UniProt\';' % uniprotId)
    if nrows == 0:
        raise ValueError('Could not find PhysicalEntity with UniProt ID \'%s\'' % uniprotId)
    else:
        return [row[0] for row in c.fetchall()]

def get_entityid_from_ensembl(c, ensemblId):
    """ gets entity id corresponding to an ENSEMBL id """
    nrows = c.execute('select * from Id_To_ExternalIdentifier where externalIdentifier=\'%s\' and referenceDatabase=\'ENSEMBL\';' % ensemblId)
    if nrows == 0:
        raise ValueError('Could not find PhysicalEntity with ENSEMBL ID \'%s\'' % ensemblId)
    else:
        return [row[0] for row in c.fetchall()]

def get_entity_from_entityid(c, entityId):
    """ gets name of entity from entity id """
    nrows = c.execute('select * from PhysicalEntity where id=%d' % entityId)
    if nrows == 0:
        raise ValueError('PhysicalEntity ID %d not valid' % entityId)
    else:
        return c.fetchall()[0][1]

def get_pathway_from_pathwayid(c, pathwayId):
    """ gets name of pathway from pathway id """
    nrows = c.execute('select * from Pathway where id=%d' % pathwayId)
    if nrows == 0:
        raise ValueError('Pathway ID %d not valid' % pathwayId)
    else:
        return c.fetchall()[0][1]

def check_if_genomic_entity(c, entityId):
    """ checks if an entity id is associated with a gene or protein """
    nrows = c.execute('select * from PhysicalEntity where id=%d' % entityId)
    if nrows == 0:
        raise ValueError('ReactionLikeEvent ID %d not valid' % entityId)
    else:
        row = c.fetchall()[0]
        return row[2] == 'Homo sapiens' and \
               row[3] in ['GenomeEncodedEntity', 'EntityWithAccessionedSequence']

def check_if_human_reaction(c, reactionId):
    """ checks if a reaction id is associated with Homo sapiens """
    nrows = c.execute('select * from ReactionLikeEvent where id=%d' % reactionId)
    if nrows == 0:
        raise ValueError('ReactionLikeEvent ID %d not valid' % reactionId)
    else:
        return c.fetchall()[0][2] == 'Homo sapiens'
    
def check_if_human_pathway(c, pathwayId):
    """ checks if a pathway id is associated with Homo sapiens """
    nrows = c.execute('select * from Pathway where id=%d' % pathwayId)
    if nrows == 0:
        raise ValueError('Pathway ID %d not valid' % pathwayId)
    else:
        return c.fetchall()[0][2] == 'Homo sapiens'
    
def get_reactionids_from_entityid(c, entityId):
    """ gets reaction ids associated with an entity id """
    c.execute('select * from ReactionLikeEvent_To_PhysicalEntity where physicalEntityId=%d' % entityId)
    reactionIds = [row[0] for row in c.fetchall() if check_if_human_reaction(c, row[0])]
    return reactionIds

def get_reactionids_from_entityids(c, entityIds):
    """ gets reaction ids associated with a list of entity ids """
    reactionIds = []
    for entityId in entityIds:
        reactionIds.extend(get_reactionids_from_entityid(c, entityId))
    return reactionIds

def get_entityids_from_reactionid(c, reactionId):
    """ gets entity ids associated with a reaction id """
    c.execute('select * from ReactionLikeEvent_To_PhysicalEntity where reactionLikeEventId=%d' % reactionId)
    entityIds = [row[1] for row in c.fetchall() if check_if_genomic_entity(c, row[1])]
    return entityIds

def get_entityids_from_reactions(c, reactions):
    """
    gets entity ids associated with multiple reactions
    propogates counts from given reactions to their associated entities
    """
    entities = pd.Series()
    for reaction, count in reactions.iteritems():
        entityIds = get_entityids_from_reactionid(c, reaction)
        entities = entities.append(pd.Series([count]*len(entityIds), index=entityIds))
    totalCounts = entities.groupby(entities.index).sum().to_frame('weight')
    totalCounts['id'] = totalCounts.index
    return totalCounts

def get_pathwayids_from_reactionid(c, reactionId):
    """ gets pathway ids associated with a reaction id """
    c.execute('select * from Pathway_To_ReactionLikeEvent where reactionLikeEventId=%d' % reactionId)
    pathwayIds = [row[0] for row in c.fetchall() if check_if_human_pathway(c, row[0])]
    return pathwayIds

#def get_pathwayids_from_reactionids(c, reactionIds):
#   """ gets pathway ids associated with a list of reaction ids """
#   allPathwayIds = []
#   for reactionId in reactionIds:
#       allPathwayIds.extend(get_pathwayids_from_reactionid(c, reactionId))
#   return allPathwayIds
#
#def get_pathwayids_from_entityid(c, entityId):
#   """ get pathway ids associated with an entity id """
#   reactionIds = get_reactionids_from_entityid(c, entityId)
#   pathwayIds = get_pathwayids_from_reactionids(c, reactionIds)    
#   return pathwayIds

def get_pathwaycounts_from_reactioncounts(c, reactions):
    """ propogate reaction counts to the pathway level """
    pathways = pd.Series()
    for reactionId, count in reactions.iteritems():
        pathwayIds = get_pathwayids_from_reactionid(c, reactionId)
        counts = pd.Series(pathwayIds).value_counts()*count
        pathways = pathways.append(counts)
    totalCounts = pathways.groupby(pathways.index).sum()
    return totalCounts.sort_values(ascending=False)

def get_reactionids_from_pathwayid(c, pathwayId):
    """ gets reaction ids associated with a pathway id """
    c.execute('select * from Pathway_To_ReactionLikeEvent where pathwayId=%d' % pathwayId)
    reactionIds = [row[1] for row in c.fetchall()]
    return reactionIds

def get_entityids_from_pathwayid(c, pathwayId):
    """ gets entity ids associated with a pathway id """
    entityIds = []  
    for reactionId in get_reactionids_from_pathwayid(c, pathwayId):
        entityIds.extend(get_entityids_from_reactionid(c, reactionId))
    return entityIds

def get_entityids_from_pathways(c, pathways):
    """
    gets entity ids associated with multiple pathways
    propogates counts from given pathways to their associated entities
    """
    entities = pd.Series()
    for pathwayId, count in pathways.iteritems():
        entityIds = get_entityids_from_pathwayid(c, pathwayId)
        entities = entities.append(pd.Series([count]*len(entityIds), index=entityIds))
    totalCounts = entities.groupby(entities.index).sum().to_frame('weight')
    totalCounts['id'] = totalCounts.index
    return totalCounts

def clean_entity_list(entities, entityIds, type_):
    """ sort and clean entity list """
    entities = entities.sort_values('weight', ascending=False)
    entities['type'] = type_
    return entities[~entities.id.isin(entityIds)]

def get_associated_genes(c, entityIds, n=10):
    """ get top n genes of each association type for given entities """
    reactionIds = get_reactionids_from_entityids(c, entityIds)
    reactionCounts = pd.Series(reactionIds).value_counts()
    rEntities = get_entityids_from_reactions(c, reactionCounts)
    rEntities = clean_entity_list(rEntities, entityIds, 'reaction')

    pathways =  get_pathwaycounts_from_reactioncounts(c, reactionCounts)
    #print [(get_pathway_from_pathwayid(c, i), count) for i, count in pathways.iteritems()]
    pEntities = get_entityids_from_pathways(c, pathways)
    pEntities = clean_entity_list(pEntities, entityIds, 'pathway')
    
    allEntities = pd.concat([rEntities.head(n), pEntities.head(n)])
    allEntities['name'] = allEntities.id.apply(lambda id: get_entity_from_entityid(c, id))
    
    return allEntities

def main():
	c = get_cursor()
	#hcmGenes = ['RGS11', 'FGFBP3', 'TMEM177', 'GAGE12D', 'KAT5', 'SCOC', 'GTF2H4', 'CENPW', 'ACRV1', 'MGC45800', 'PSMC6', 'HOXA3']
	hcmGenes = sys.argv[1:len(sys.argv)]	
	#hcmGenes = ['ACTC1', 'GLA', 'LAMP2', 'MYBPC3', 'MYH7', 'MYL2', 'MYL3',
	#            'PRKAG2', 'TNNI3', 'TNNT2', 'TPM1', 'TNNC1', 'TTR']
	entityIds = []
	for gene in hcmGenes:
		entityIds.extend(get_entityids_from_entityname(c, gene))
	print get_associated_genes(c, entityIds)
    

if __name__ == '__main__':
    main()
