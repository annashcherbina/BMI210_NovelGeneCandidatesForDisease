import sys 
import MySQLdb as mdb
import pandas as pd

def get_cursor():
    """ gets MySQLdb cursor to access database """
    db = mdb.connect('bmi210project.czxrvyi7olca.us-west-1.rds.amazonaws.com', 'bmi210project', 'bmi210project', 'bmi210project', 3306)
    return db, db.cursor()
def disconnect(db,c): 
    db.commit() 
    c.close() 
    db.close() 

def load_GO_data(c): 
    data=open('c5.cc.v5.1.symbols.gmt.1-1.txt').read().split('\n') 
    while '' in data: 
        data.remove('') 
    for i in range(len(data)): 
        cur_id=i+1
        tokens=data[i].split('\t') 
        cur_loc=tokens[0] 
        cur_gene=tokens[1] 
        c.execute('insert into GO_cellular_component (location,genes,id) VALUES(\'%s\',\'%s\',%i);'% (cur_loc,cur_gene,cur_id)); 

def load_subject_disease(c): 
    data=open('subject_to_disease.csv','r').read().split('\n') 
    cur_id=0
    while '' in data: 
        data.remove('') 
    for line in data: 
        tokens=line.split(',') 
        subject=tokens[0] 
        if len(tokens)>1: 
            #get subject id 
            subject_id_query=c.execute("select genome_id from genomes where global_human_id like \'%s\';"%(subject))
            subject_id=c.fetchall()
            print "subject_id:"+str(subject_id) +"line:"+str(line) 
            if len(subject_id)==0: 
                continue 
            subject_id=subject_id[0][0] 
            diseases=tokens[1::] 
            for disease in diseases: 
                #get disease id 
                disease='%'+disease+'%' 
                disease_id_query=c.execute("select disease_id from diseases where disease_name like \'%s\';"%(disease))
                disease_id=c.fetchall()
                print "disease id:"+str(disease_id)+ "disease:"+str(disease) 
                if len(disease_id)==0: 
                    continue 
                for d in disease_id: 
                    curd=d[0] 
                    print str(curd) 
                    #link the subject to their disease 
                    cur_id+=1 
                    c.execute('insert into genome_to_disease (id,genome_id,disease_id) values(%i,%i,%i);' %(cur_id,subject_id,curd)) 

def load_subject_metadata(c): 
    data=open('subject_metadata.csv','r').read().split('\n') 
    while '' in data: 
        data.remove('') 
    for line in data: 
        try:
            tokens=line.split(',') 
            #print str(tokens) 
            subject=tokens[0] 
            age=tokens[1]
            if age == "": 
                age=-1 
            else: 
                age=int(age) 
                if age > 90: 
                    age=2016-age 
            healthy=tokens[2] 
            if healthy=="": 
                healty=1
            else: 
                healthy=bool(healthy)
            sex=str(tokens[3]) 
            race=tokens[4] 
            c.execute('update genomes set age=%i,sex=\'%s\',ethnicity=\'%s\',healthy=%i where global_human_id like \'%s\';'%(age,sex,race,healthy,subject)); 
        except: 
            print line 

def load_subject_variants(c,subject_file,subject,start_line,end_line):
    c.execute('select genome_id from genomes where global_human_id like \'%s\';'%(subject))
    genome_id=c.fetchone()[0] 
    data=open(subject_file,'r').read().split('\n')
    while '' in data: 
        data.remove('') 
    counter=0 
    total=str(len(data))
    mappings=[] 
    for line in data[start_line:end_line]: 
        counter+=1
        if counter%1000==0: 
            print str(counter) + '\t'+total 
        tokens=line.split('\t') 
        chrom="chr"+tokens[0] 
        pos=int(tokens[1]) 
        a1=tokens[2] 
        a2=tokens[3] 
        try:
            rs=int(tokens[4][2::]) 
        except: 
            rs=None #for now, ignore variants that are not in dbSNP ! 
            continue 
        gene=tokens[5]
        #1. is the variant in the database?         
        c.execute('select variant_id from variants where variant_rsid=%i limit 1;'%(rs)); 
        varhit=c.fetchone() 
        if varhit!=None: 
            varid=varhit[0] 
        else: 
            c.execute('insert into variants (variant_gene,variant_rsid) values(\'%s\',%i);'%(gene,rs)); 
            varid=c.lastrowid 
        mappings.append(tuple([genome_id,varid]))
        #check by chromosome & position if the variant exists 
        '''#TODO for the final submission
        c.execute('select * from variant_locations where chr like \'%s\' and chr_pos=%i limit 1;'%(chrom,pos))
        hits=c.fetchone()
        if hits==None: 
            c.execute('insert into variant_locations(chr,chr_pos,rsid,variant_id,inGene) values(\'%s\',%i,%i,%i,%r);'%(chrom,pos,rs,varid,ingene))
        elif hits[-1]==None:
            try:
                c.execute('update variant_locations set variant_id=%i;'%(varid))
            except: 
                print line 
                continue 
        '''
    outf=open('mappings.backup'+str(start_line)+"."+str(end_line),'w') 
    for m in mappings: 
        outf.write('\t'.join([str(i) for i in m])+'\n')
    

def main():
    db,c = get_cursor()
    #load_GO_data(c)
    #load_subject_metadata(c)
    #load_subject_disease(c) 
    start_line=int(sys.argv[1]) 
    end_line=int(sys.argv[2]) 
    for s in [ 'genomes/huED0F40.snps.filtered.ANNOTATED']: #['genomes/huB1FD55.snps.filtered.ANNOTATED']:#'genomes/huED0F40.snps.filtered.ANNOTATED']:#  'genomes/huA9D22A.snps.ANNOTATED']: 
        subject=s.split('/')[1].split('.')[0] 
        load_subject_variants(c,s,subject,start_line,end_line)
    disconnect(db,c) 

    

if __name__ == '__main__':
    main()
