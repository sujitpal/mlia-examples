df <- read.csv("BirdStrikes.csv");
# preprocess and sort data by flight date
df$FlightDate <- as.numeric(
  as.Date(df$FlightDate, format="%m/%d/%Y %H:%M") -
  as.Date("1970-01-01", format="%Y-%m-%d"))
df$Effect..Impact.to.flight <- as.factor(df$Effect..Impact.to.flight)
df.sorted <- df[with(df, order(FlightDate)), ]
# find limits for graphing
ylim.min <- min(as.numeric(df.sorted$Effect..Impact.to.flight))
ylim.max <- max(as.numeric(df.sorted$Effect..Impact.to.flight))
xlim.min <- min(df$FlightDate)
xlim.max <- max(df$FlightDate)
xlim.cent <- (xlim.min + xlim.max) / 2
# colors for graphing
colors <- palette()
idf <- as.data.frame(table(df.sorted$Effect..Impact.to.flight))
i <- 1
leg.txt <- c()
leg.cols <- c()
for (impact.str in idf$Var1) {
  df.subset <- df.sorted[df.sorted$Effect..Impact.to.flight == impact.str, ]
  if (i == 1) {
    print(paste("in plot:", impact.str, colors[i]))
    plot(df.subset$FlightDate, 
         df.subset$Effect..Impact.to.flight, 
         col=colors[i], xaxt="n", yaxt="n",
         xlab="Time", ylab="Impact Type",
         ylim=c(ylim.min, ylim.max), xlim=c(xlim.min, xlim.max),
         main="Impact Types over Time")
  } else {
    print(paste("in line:", impact.str, colors[i]))
    points(df.subset$FlightDate, 
           df.subset$Effect..Impact.to.flight,
           col=colors[i])
  }
  leg.cols <- cbind(leg.cols, colors[i])
  leg.txt <- cbind(leg.txt, impact.str)
  i <- i + 1
}
x.at <- c(xlim.min, xlim.cent, xlim.max)
x.labels <- as.Date("1970-01-01") + x.at
axis(1, at=x.at, labels=x.labels, las=0)
axis(2, at=c(1,2,3,4,5,6), labels=c("UK", "AT", "ES", "NO", "OT", "PL"), las=2, cex=0.5)