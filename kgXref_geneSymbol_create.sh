
~UCSC->Table->clade(Mammal)->genome(Human)->assembly(GRch37/hg19)->group(Genes and Gene Prediction Tracks)->track(RefSeq Genes)->table(kgXref)->output format(selected fields from primary and related tables)->get output->select "kgID" and "geneSymbol", than get output.
You'll get a file contains UCSC gene ID vs. symbol. Use this file to replace the UCSC gene ID with symbol in your refgene file.
