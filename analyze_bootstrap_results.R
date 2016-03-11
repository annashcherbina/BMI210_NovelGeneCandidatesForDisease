
mydata <- read.table("results.huB1FD55",fill = TRUE,sep=" ")


results <- matrix(0,nrow=dim(mydata)[1],ncol = 4)
for (i in 1: dim(mydata)[1]){
    tabs=lapply(strsplit(paste(mydata[i,]),"\t"), table)
    out=data.frame(item=names(unlist(tabs)),count=unlist(tabs)[],
                   stringsAsFactors=FALSE)
    rownames(out)=c()
    #Match number:
    results[i,1]<-out$item[1]
    #Match target:
    if(length(out$count[which(out$item=="target")])==0){
        results[i,2]<-0
    }else{
        results[i,2]<-out$count[which(out$item=="target")]
    }
    #Match Association:
    if(length(out$count[which(out$item=="associated")])==0){
        results[i,3]<-0
    }else{
    results[i,3]<-out$count[which(out$item=="associated")]
    }
    #Match RSID:
    if(length(results[i,4]<-dim(out[grep("rs",out$item),])[1])==0){
        results[i,4]<-0
    }else{
        results[i,4]<-dim(out[grep("rs",out$item),])[1]
        }
    
    print(out)
}


colnames(results)<-c('iter','target','associated','rsID')


final <- matrix(NA,nrow=1000,ncol = 4)
for(i in 1:1000){
    if(length(which(results[,1]==i-1))==0){
        next
    }
    r_subset<-results[which(results[,1]==i-1),]
    r_subset<-as.data.frame(r_subset)
    if(dim(r_subset)[2]==1){
        final[i,1]<- as.numeric(t(r_subset)[1])+1
        final[i,2:4]<-t(r_subset)[2:4]
    }else{
        X <- apply(r_subset, 2, as.numeric)
        final[i,1]<-i
        final[i,2:4]<-colSums(X)[2:4]
    }
}


#NA:
    sum(is.na(final[,1]))
#NA removed:
final_noNA <-final[!is.na(final[,1]),]

sum(as.numeric(final_noNA[,2]),na.rm = T)/(1000-sum(is.na(final[,1])))
sum(as.numeric(final_noNA[,3]),na.rm = T)/(1000-sum(is.na(final[,1])))
sum(as.numeric(final_noNA[,4]),na.rm = T)/(1000-sum(is.na(final[,1])))



