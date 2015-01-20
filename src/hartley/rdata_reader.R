setwd("/home/sujit/Projects/mlia-examples/data/hartley")
dat <- dget("patchesHartley2.rdat")

y <- sapply(dat, function(x) x$Y)
write.table(y, file="y.csv", row.names=FALSE, col.names=FALSE)

Xgray <- matrix(nrow=length(dat), ncol=121)
Xmedian <- matrix(nrow=length(dat), ncol=121)
for (i in 1:length(dat)) {
  Xgray[i, ] = as.vector(dat[[i]]$gray)
  Xmedian[i, ] = as.vector(dat[[i]]$median)
}
write.table(Xgray, file="Xgray.csv", row.names=FALSE, col.names=FALSE)
write.table(Xmedian, file="Xmedian.csv", row.names=FALSE, col.names=FALSE)
