data<-read.delim("c5.cc.v5.1.symbols.gmt.txt", header=F)
data.export<-as.data.frame(matrix(data=NA, nrow=0, ncol=2))
for (i in 1:nrow(data)){
	list1<-as.character(unlist(data[i,3:ncol(data)]))
	list2<-list1[list1!=""]
	data.new<-as.data.frame(matrix(data=NA, nrow=length(list2), ncol=2))
	data.new$V1<-data[i,1]
	data.new$V2<-list2
	data.export<-rbind(data.export, data.new)
	print(i)
}
write.table(data.export, file="c5.cc.v5.1.symbols.gmt.1-1.txt", quote=FALSE, row.names=FALSE, col.names=FALSE, sep="\t")
save(list=ls(), file="todo.rda")
