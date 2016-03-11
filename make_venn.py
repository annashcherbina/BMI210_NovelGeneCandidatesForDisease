#generates a venn diagram across the 3 ontologies 
import sys 
import MySQLdb as mdb


def get_cursor():
    """ gets MySQLdb cursor to access database """
    db = mdb.connect('bmi210project.czxrvyi7olca.us-west-1.rds.amazonaws.com', 'bmi210project', 'bmi210project', 'bmi210project', 3306)
    return db, db.cursor()

def disconnect(db,c): 
    db.commit() 
    c.close() 
    db.close() 


def main():
    db,c = get_cursor()
    c.execute('select distinct variant_gene from variants;')
    #PGP 
    pgp_genes=c.fetchall() 
    pgp_genes=[i[0] for i in pgp_genes] 
    #GO 
    c.execute('select genes from GO_cellular_component;') 
    go_genes=c.fetchall() 
    go_genes=[i[0] for i in go_genes] 
    #REACTOME 
    c.execute('select displayName from PhysicalEntity where species like \'Homo sapiens\' and class like \'EntityWithAccessionedSequence\';')
    reactome_genes=c.fetchall() 
    reactome_genes=[i[0].split(' ')[0] for i in reactome_genes]
    
    #generate venn diagram of the gene sets 
    pgp_genes=set(pgp_genes) 
    go_genes=set(go_genes) 
    reactome_genes=set(reactome_genes) 
    all3=(pgp_genes.intersection(go_genes)).intersection(reactome_genes) 
    go_pgp=(pgp_genes.intersection(go_genes))-reactome_genes 
    go_reactome=(go_genes.intersection(reactome_genes))-pgp_genes 
    pgp_reactome=(pgp_genes.intersection(reactome_genes))-go_genes 
    go_only=(go_genes-pgp_genes)-reactome_genes
    reactome_only=reactome_genes - go_genes - pgp_genes 
    pgp_only=pgp_genes - go_genes - reactome_genes 
    print "all3:"+str(len(all3)) 
    print "go_pgp:"+str(len(go_pgp))
    print "go_reactome:"+str(len(go_reactome))
    print "pgp_reactome:"+str(len(pgp_reactome)) 
    print "go_only:"+str(len(go_only))
    print "reactome_only:"+str(len(reactome_only))
    print "pgp_only:"+str(len(pgp_only)) 
    disconnect(db,c) 

    

if __name__ == '__main__':
    main()
