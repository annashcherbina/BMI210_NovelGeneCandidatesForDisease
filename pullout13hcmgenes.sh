




mysql --user=genome --host=genome-mysql.cse.ucsc.edu -A -D hg19 -e 'select X.geneSymbol,K.name as transcript, K.chrom,K.txEnd-K.txStart as transcriptLen from kgXref as X,knownGene as K where X.geneSymbol="ACTC1" and X.kgId=K.name'>ACTC1.GENE.LENGTH.tab
mysql --user=genome --host=genome-mysql.cse.ucsc.edu -A -D hg19 -e 'select X.geneSymbol,K.name as transcript, K.chrom,K.txEnd-K.txStart as transcriptLen from kgXref as X,knownGene as K where X.geneSymbol="GLA" and X.kgId=K.name'>GLA.GENE.LENGTH.tab
mysql --user=genome --host=genome-mysql.cse.ucsc.edu -A -D hg19 -e 'select X.geneSymbol,K.name as transcript, K.chrom,K.txEnd-K.txStart as transcriptLen from kgXref as X,knownGene as K where X.geneSymbol="LAMP2" and X.kgId=K.name'>LAMP2.GENE.LENGTH.tab
mysql --user=genome --host=genome-mysql.cse.ucsc.edu -A -D hg19 -e 'select X.geneSymbol,K.name as transcript, K.chrom,K.txEnd-K.txStart as transcriptLen from kgXref as X,knownGene as K where X.geneSymbol="MYBPC3" and X.kgId=K.name'>MYBPC3.GENE.LENGTH.tab
mysql --user=genome --host=genome-mysql.cse.ucsc.edu -A -D hg19 -e 'select X.geneSymbol,K.name as transcript, K.chrom,K.txEnd-K.txStart as transcriptLen from kgXref as X,knownGene as K where X.geneSymbol="MYH7" and X.kgId=K.name'>MYH7.GENE.LENGTH.tab
mysql --user=genome --host=genome-mysql.cse.ucsc.edu -A -D hg19 -e 'select X.geneSymbol,K.name as transcript, K.chrom,K.txEnd-K.txStart as transcriptLen from kgXref as X,knownGene as K where X.geneSymbol="MYL2" and X.kgId=K.name'>MYL2.GENE.LENGTH.tab
mysql --user=genome --host=genome-mysql.cse.ucsc.edu -A -D hg19 -e 'select X.geneSymbol,K.name as transcript, K.chrom,K.txEnd-K.txStart as transcriptLen from kgXref as X,knownGene as K where X.geneSymbol="MYL3" and X.kgId=K.name'>MYL3.GENE.LENGTH.tab
mysql --user=genome --host=genome-mysql.cse.ucsc.edu -A -D hg19 -e 'select X.geneSymbol,K.name as transcript, K.chrom,K.txEnd-K.txStart as transcriptLen from kgXref as X,knownGene as K where X.geneSymbol="PRKAG2" and X.kgId=K.name'>PRKAG2.GENE.LENGTH.tab
mysql --user=genome --host=genome-mysql.cse.ucsc.edu -A -D hg19 -e 'select X.geneSymbol,K.name as transcript, K.chrom,K.txEnd-K.txStart as transcriptLen from kgXref as X,knownGene as K where X.geneSymbol="TNNI3" and X.kgId=K.name'>TNNI3.GENE.LENGTH.tab
mysql --user=genome --host=genome-mysql.cse.ucsc.edu -A -D hg19 -e 'select X.geneSymbol,K.name as transcript, K.chrom,K.txEnd-K.txStart as transcriptLen from kgXref as X,knownGene as K where X.geneSymbol="TNNT2" and X.kgId=K.name'>TNNT2.GENE.LENGTH.tab
mysql --user=genome --host=genome-mysql.cse.ucsc.edu -A -D hg19 -e 'select X.geneSymbol,K.name as transcript, K.chrom,K.txEnd-K.txStart as transcriptLen from kgXref as X,knownGene as K where X.geneSymbol="TPM1" and X.kgId=K.name'>TPM1.GENE.LENGTH.tab
mysql --user=genome --host=genome-mysql.cse.ucsc.edu -A -D hg19 -e 'select X.geneSymbol,K.name as transcript, K.chrom,K.txEnd-K.txStart as transcriptLen from kgXref as X,knownGene as K where X.geneSymbol="TNNC1" and X.kgId=K.name'>TNNC1.GENE.LENGTH.tab
mysql --user=genome --host=genome-mysql.cse.ucsc.edu -A -D hg19 -e 'select X.geneSymbol,K.name as transcript, K.chrom,K.txEnd-K.txStart as transcriptLen from kgXref as X,knownGene as K where X.geneSymbol="TTR" and X.kgId=K.name'>TTR.GENE.LENGTH.tab




