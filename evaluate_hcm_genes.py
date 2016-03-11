import reactome_tools as rt
import find_novel_genes as ng
import pandas as pd
import numpy as np

def get_associated_genes_combined(c, genes):
    """ get all associated genes based on both pathway and location """
    # get entity ids associated with gene get
    entityIds = []
    for gene in genes:
        entityIds.extend(rt.get_entityids_from_entityname(c, gene))
    # get genes associated by pathway
    associatedGenes = rt.get_associated_genes(c, entityIds, 20)
    associatedGenes = [gene.split()[0] for gene in associatedGenes.name]
    allAssociatedGenes = pd.Series()
    # get genes associated by location
    for gene in genes:
        colocalAssociatedGenes = ng.check_location(c, gene, associatedGenes)
        allAssociatedGenes = allAssociatedGenes.append(pd.Series(colocalAssociatedGenes))
    return allAssociatedGenes

c = rt.get_cursor()

hcmGenes = np.loadtxt('../data/hcm_definitive.txt', str)
hcmAssoc = np.loadtxt('../data/hcm_associated.txt', str)

# folds for cross validation of hcm genes
splits = [range(4), range(4,8), range(8,13)]
splits = [[i] for i in range(13)]
for i, split in enumerate(splits):
    print 'split %d' % i 
    # hold out one set of genes
    associatedGenes = get_associated_genes_combined(c, np.delete(hcmGenes, split))
    # print results
    print '\t%d genes found:' % len(associatedGenes.unique()),
    print associatedGenes.unique()
    matchingGenes = [gene for gene in associatedGenes.unique() if gene in hcmGenes[split]]
    print '\t%d held out genes found:' % len(matchingGenes),
    print matchingGenes
    print '\n',

print 'all genes:'
associatedGenes = get_associated_genes_combined(c, hcmGenes)
print '\t%d genes found:' % len(associatedGenes.unique()),
print associatedGenes.unique()
matchingGenes = [gene for gene in associatedGenes.unique() if gene in hcmAssoc]
print '\t%d held out genes found:' % len(matchingGenes),
print matchingGenes
