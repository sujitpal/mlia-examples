df <- read.csv("BirdStrikes.csv");
df.clean <- df[df$Origin.State != "N/A", ];
# calculate counts of bird hits by Origin.State
bsdf <- as.data.frame(table(df.clean$Origin.State))
bsdf.sorted <- bsdf[with(bsdf, order(-Freq)), ]
bar <- barplot(height=bsdf.sorted$Freq, horiz=FALSE, beside=TRUE, 
               width=c(2,2), space=0.5, xaxt="n",
               col=palette())
text(bar, par("usr")[3], labels=bsdf.sorted$Var1, srt=45, 
     adj=c(1.1, 1.1), xpd=TRUE, cex=0.5)
# calculate sum of costs incurred by Origin.State
cidf <- aggregate(as.numeric(Cost..Total..) ~ Origin.State, 
                  data=df.clean, FUN="sum")
names(cidf) <- c("state", "cost")
cidf.sorted <- cidf[with(cidf, order(-cost)), ]
bar2 <- barplot(height=cidf.sorted$cost, horiz=FALSE, beside=TRUE,
                width=c(2,2), space=0.5, xaxt="n",
                col=palette())
text(bar2, par("usr")[3], labels=cidf.sorted$state, srt=45, 
     adj=c(1.1, 1.1), xpd=TRUE, cex=0.5)