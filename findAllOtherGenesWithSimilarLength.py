
import csv
import numpy as np
import os
import subprocess 


def get_HCM_gene_length(listofHCMgenes):
    """ gets the median length of all the HCM genes used"""
    os.chdir("/home/jess/gene")
    gene_length = []
    for gene in listofHCMgenes:
        filename = '%s.GENE.LENGTH.tab'%gene
        with open(filename) as f:
            reader = csv.reader(f, delimiter="\t")
            d = np.array(list(reader))
            a = []
            for x in range(1, (d.shape[0])):
                a.append(d[x][3])
            a=np.array(a).astype(np.float)
        median_gene_length = np.median(a,axis=0)
        gene_length.append([gene, median_gene_length])
    return gene_length


def find_all_genes_that_are_similar_length(gene):
    """ gets all the genes that are of similar length and outputs to file for use later in bootstrapping"""
    os.chdir("/home/jess/gene")    
    current_gene_name = gene[0]
    current_gene_length = gene[1]
    current_gene_min =  current_gene_length - 50
    current_gene_max = current_gene_length + 50
    mysql_statement = 'mysql --user=genome --host=genome-mysql.cse.ucsc.edu -A -D hg19 -e " select distinct name, chrom, txStart, txEnd, (txEnd - txStart) as length from refGene where (txEnd - txStart) >=%s and (txEnd - txStart) <=%s " > %s.current_gene_name.matches.tab' % (current_gene_min,current_gene_max,current_gene_name)
    print mysql_statement + "complete"
    subprocess.Popen(mysql_statement,shell=True)    


HCM_genes =['ACTC1','GLA','LAMP2', 'MYBPC3','MYH7','MYL2','MYL3','PRKAG2','TNNI3','TNNT2','TPM1','TNNC1','TTR']
print HCM_genes

HCM_gene_lengths=get_HCM_gene_length(HCM_genes)
for hcm_gene in HCM_gene_lengths:
    find_all_genes_that_are_similar_length(hcm_gene)



    
