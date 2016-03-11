

import csv
import os
import subprocess 
from subprocess import call
from numpy import genfromtxt
import numpy as np
import argparse
import sys
from reactome_tools_JT import *
from Params import *
from find_novel_genes_JT import *

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

os.chdir("/home/jess/gene")
matched_gene_filename = 'total.genes.tab'
with open(matched_gene_filename) as f:
    reader = csv.reader(f, delimiter="\t")
    matched_genes = np.array(list(reader))

lookup_gene_filename = 'kgXref_geneSymbol'
lookup = {}

f = open(lookup_gene_filename)
for line in iter(f):
    currentLine = line.split("\t")
    if len(currentLine)>=3:
        if currentLine[2]== '\n':
            next
        else:
            lookup[currentLine[2].rstrip('\n')]=currentLine[1].rstrip('\n')
            #lookup[currentLine[1].rstrip('n')]=currentLine[2].rstrip('\n')


#bootstrap_iter=1
#subject='huB1FD55'
#subject='huED0F40'
subject='huA9D22A'
disease="Hypertrophic"
filterByCellularLocation=True 

#outf=open('/home/jess/results/results.'+str(subject),'a')
with open('/home/jess/results/results.'+str(subject), "a") as myfile:
    myfile.write("appended text")

db,c=get_cursor()


for bootstrap_iter in range(0, 999):
    print bootstrap_iter
    print bootstrap_iter
    print bootstrap_iter
    random_genes = []
    count = 0
    while (count < 13):
        sampleIdx = np.random.choice(matched_genes.shape[0], 1,replace=True)
        selected_genes = matched_genes[sampleIdx]
        lookup_results = lookup.get(selected_genes[0][0],"NA")
        if lookup_results == "NA":
            print 'Sorry try again'
        else:
            random_genes.append(lookup_results)
            print 'The count is:', count
            count = count + 1
    genes=random_genes
    print "subject:"+str(subject)
    print "disease:"+str(disease)
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
    print "associated genes first pass:"+str(associated_genes)
    entityIds=[]
    for gene in genes:
        try:
            entityIds.extend(get_entityids_from_entityname(c, gene))
        except:
            continue
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
    with open('/home/jess/results/results.'+str(subject), "a") as myfile:
        for gene in target_hits:
            if len(target_hits[gene])>0:
                print "yes"
                myfile.write(str(bootstrap_iter)+'\ttarget\t'+gene+'\t'+'\t'.join(target_hits[gene])+'\n')
        for gene in associated_hits:
            if len(associated_hits[gene])>0:
                print "yes"
                myfile.write(str(bootstrap_iter)+'\tassociated\t'+gene+'\t'+'\t'.join(associated_hits[gene])+'\n')
        


disconnect(db,c)


