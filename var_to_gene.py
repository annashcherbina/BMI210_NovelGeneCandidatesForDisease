import sys 
#map variant to nearest gene and indicate if variant is actually in the gene
genes=open('genes.gtf','r').read().split('\n')
while '' in genes:
    genes.remove('')
binsize=100000
gene_dict=dict()
valid_opts=['start_codon','stop_codon']

for line in genes:
    tokens=line.split('\t')
    if tokens[2] in valid_opts:
        chrom=tokens[0]
        if chrom not in gene_dict:
            gene_dict[chrom]=dict()
        startpos=int(tokens[3])
        endpos=int(tokens[4])
        curbin=startpos/binsize
        gene=tokens[8].split(';')[0].replace('\"','').replace('gene_id ','')
        #print gene
        if curbin not in gene_dict[chrom]:
            gene_dict[chrom][curbin]=dict()
        if gene not in gene_dict[chrom][curbin]:
            gene_dict[chrom][curbin][gene]=[0,0]
        if tokens[2]=='start_codon':
            gene_dict[chrom][curbin][gene][0]=startpos
        else:
           gene_dict[chrom][curbin][gene][1]=endpos
print "built gene dict!"
variants=open(sys.argv[1],'r').read().replace('\r\n','\n').split('\n')
while '' in variants:
    variants.remove('')
print "read in variant file!" 
outf=open(sys.argv[1]+".ANNOTATED",'w')
counter=0
total=str(len(variants))
is23me=False 
for line in variants:
    counter+=1
    if counter%10000==0:
        print str(counter)+'/'+total 
    if line.startswith('#'):
        continue 
    tokens=line.split('\t')
    print str(tokens) 
    #23&Me format
    if ((is23me) or (tokens[0].startswith('rs'))):
        is23me=True 
        rsid=tokens[0]
        chrom=tokens[1]
        pos=int(tokens[2])
        a1=tokens[3][0]
        a2=a1
        if len(tokens[3])>1: 
            a2=tokens[3][1]
    #Complete genomics format 
    else:
        chrom=tokens[0].replace('chr','')
        pos=int(tokens[3])
        alleles=tokens[8].split(';')[0].replace('alleles ','')
        #print str(alleles)
        if len(alleles)==1:
            a1=alleles[0]
            a2=alleles[0]
        else:
            a2=alleles[2] 
        rsid=""
        if len(tokens[8].split(';'))>2: 
            rsid=tokens[8].split(';')[1].split(':')[-1]
    #get the nearest gene
    if chrom not in gene_dict:
        continue 
    curbin=pos/binsize
    nearest_gene=None
    ingene=False
    min_dist=float("inf") 
    for b in [curbin-1,curbin,curbin+1]:
        if b in gene_dict[chrom]:
            candidates=gene_dict[chrom][b]
            for c in candidates:
                c_start=candidates[c][0]
                if abs(c_start-pos)<min_dist:
                    c_end=candidates[c][1] 
                    min_dist=abs(c_start-pos)
                    nearest_gene=c
                    if ((c_start <= pos)  and (c_end >= pos)):
                        ingene=True
    #write the annotations
    if nearest_gene!=None:
        #we only care about near-gene variants! 
        outf.write(chrom+'\t'+str(pos)+'\t'+a1+'\t'+a2+'\t'+rsid+'\t'+nearest_gene+'\t'+str(min_dist)+'\t'+str(ingene)+'\n')
        
        
