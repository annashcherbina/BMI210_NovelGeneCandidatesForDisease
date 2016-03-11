import sys 
import MySQLdb as mdb
import pandas as pd
from reactome_tools_JT import * 
from Params import * 

def get_cursor():
    """ gets MySQLdb cursor to access database """
    db = mdb.connect('bmi210project.czxrvyi7olca.us-west-1.rds.amazonaws.com', 'bmi210project', 'bmi210project', 'bmi210project', 3306)
    return db, db.cursor()

def disconnect(db,c): 
    db.commit() 
    c.close() 
    db.close() 
    
def parseArgs(): 
    subject=None 
    disease=None 
    genes=None 
    helparg=False 
    filterByCellularLocation=False 
    for i in range(len(sys.argv)): 
        if sys.argv[i]=="-subject": 
            subject=sys.argv[i+1] 
        elif sys.argv[i]=="-disease": 
            disease=sys.argv[i+1] 
        elif sys.argv[i]=="-genes": 
            genes=[] 
            for j in range(i+1,len(sys.argv)): 
                if not sys.argv[j].startswith('-'):
                    genes.append(sys.argv[j])  
        elif sys.argv[i] in ['-help','--help','-h','--h']: 
            helparg=True 
        elif sys.argv[i]=='-filterByCellularLocation': 
            filterByCellularLocation=True 
    return subject,disease,genes,helparg,filterByCellularLocation

#query the database to get a list of genes known to be associated with our disease of interest 
def getKnownTargetGenes(c,disease): 
    c.execute('select disease_id from diseases where disease_name like "%'+disease+'%";')
    disease_ids=c.fetchall() 
    if len(disease_ids)==0: 
        return [] 
    disease_ids=[i[0] for i in disease_ids]; 
    #print "disease_ids:"+str(disease_ids)
    #get associated genes 
    genes=set([]) 
    for disease_id in disease_ids: 
        c.execute('select gene from gene_disease where disease_id=%i;'%(disease_id))
        hits=c.fetchall() 
        if hits!=None: 
            genes=genes.union(set([i[0] for i in hits]))
        c.execute('select variant_id from variant_disease where disease_id=%i;'%(disease_id))
        variants=c.fetchall() 
        if len(hits)>0: 
            variants=[i[0] for i in variants] 
            for variant_id in variants: 
                c.execute('select variant_gene from variants where variant_id=%i;'%(variant_id))
                hit=c.fetchone()[0] 
                genes.add(hit) 
        #get associated variants, from the associated variants, expand the list of associated genes 
    return list(genes) 


def get_subject_variants_for_one_gene(c,subject,gene): 
    #1 get subject id 
    c.execute('select genome_id from genomes where global_human_id like \'%s\' limit 1;'%(subject))
    subject_id=c.fetchone()[0] 
    #2 get variants that have been observed in PGP for this gene 
    c.execute('select variant_id from variants where variant_gene like \'%s\';'%(gene)) 
    gene_variant_ids=c.fetchall() 
    gene_variant_ids=set([i[0] for i in gene_variant_ids]) 
    #3 does subject have any variants in this gene? 
    c.execute('select variant_id from variant_genome where genome_id=%i;'%(subject_id))
    subject_variant_ids=c.fetchall()
    subject_variant_ids=set([i[0] for i in subject_variant_ids]) 
    common_ids=gene_variant_ids.intersection(subject_variant_ids) 
    #4. get the rsid
    hits=[] 
    for cur_id in common_ids: 
        c.execute('select variant_rsid from variants where variant_id=%i limit 1;'%(cur_id))
        hit=c.fetchone()[0] 
        #5. check whether the variant is rare (maf < maf_threshold); if maf is unknown, we'll tentatively accept the variant
        accept=False 
        c.execute('select f from variant_frequency where rsid=%i limit 1;'%(hit)) 
        maf=c.fetchone()
        #print "maf:"+str(maf) 
        if maf==None:  
            accept=True 
        elif maf[0]<maf_threshold: 
            accept=True 
        if accept: 
            hits.append('rs'+str(hit)) 
    return hits 

def check_location(c,gene,associated_genes): 
    surviving_genes=[] 
    #get the cellular location for the gene 
    c.execute('select location from GO_cellular_component where genes like \'%s\';'%(gene))
    current_location=c.fetchone() 
    #print "target gene location:"+str(current_location) 
    if current_location==None: 
        return associated_genes #we don't have a known location for the gene of interest and therefor we cannot filter the associated genes 
    current_location=current_location[0] 
    for gene in associated_genes:
        c.execute('select location from GO_cellular_component where genes like \'%s\';'%(gene)) 
        associated_gene_location=c.fetchone()
        #print "associated gene location:"+str(associated_gene_location) 
        if associated_gene_location==None: 
            surviving_genes.append(gene) 
        else: 
            associated_gene_location=associated_gene_location[0] 
            if current_location==associated_gene_location: 
                surviving_genes.append(gene) 
    return surviving_genes 

        

def main(): 
    db,c=get_cursor() 
    subject,disease,genes,helparg,filterByCellularLocation=parseArgs() 
    if((subject==None) or (disease==None) or (helparg==True)): 
        print "Usage:"
        print "python find_novel_genes.py -subject <subject_name> -disease <subject disease> -genes [list of genes, optional] -filterByCellularLocation [optional, only variants in the same cellular location will be returned]" 
        exit() 

    print "subject:"+str(subject) 
    print "disease:"+str(disease) 

    #The user did not specify a set of genes to check, query the database for genes that are known to be associated with the disease 
    if genes==None: 
       genes=getKnownTargetGenes(c,disease) 
    print "target genes:"+str(genes) 
    associated_genes=[] 
    for gene in genes:
        try:
            entityIds=get_entityids_from_entityname(c,gene)
            associated_genes_current=get_associated_genes(c,entityIds)['name'].values.tolist() 
            associated_genes_current=[i.split(' ')[0] for i in associated_genes_current] 
            associated_genes_current=[i.split('(')[0] for i in associated_genes_current]
            if filterByCellularLocation==True: 
                associated_genes_current=check_location(c,gene,associated_genes_current) 
            associated_genes=associated_genes+associated_genes_current
        except: 
            continue 
    associated_genes=set(associated_genes)
    #print "associated genes first pass:"+str(associated_genes) 
    entityIds=[] 
    for gene in genes: 
        entityIds.extend(get_entityids_from_entityname(c, gene))
    associated_genes_final=get_associated_genes(c,entityIds)['name'].values.tolist() 
    associated_genes_final=[i.split(' ')[0] for i in associated_genes_final] 
    associated_genes_final=[i.split('(')[0] for i in associated_genes_final]
    associated_genes_final=set(associated_genes_final) 
    associated_genes=associated_genes.intersection(associated_genes_final) 
    print "associated genes:"+str(associated_genes) 
    target_hits=dict() 
    associated_hits=dict() 
    for gene in genes:
        target_hits[gene]=get_subject_variants_for_one_gene(c,subject,gene)
    for gene in associated_genes: 
        associated_hits[gene]=get_subject_variants_for_one_gene(c,subject,gene) 
    outf=open('results.'+str(subject),'w') 
    for gene in target_hits: 
        if len(target_hits[gene])>0: 
            outf.write('target\t'+gene+'\t'+'\t'.join(target_hits[gene])+'\n')
    for gene in associated_hits: 
        if len(associated_hits[gene])>0: 
            outf.write('associated\t'+gene+'\t'+'\t'.join(associated_hits[gene])+'\n')
    disconnect(db,c) 

if __name__=='__main__': 
    main() 
