df <- read.csv("BirdStrikes.csv");
# we want to roll up by YYYYMM, so we convert the FlightDate to that
df$FlightDate <- as.numeric(format(as.Date(df$FlightDate, 
                            format="%m/%d/%Y %H:%M"), "%Y%m"))
# subset and roll up counts for each impact type
impact.types <- as.data.frame(table(df$Effect..Impact.to.flight))
# we visually figure out the ymin and ymax values for all impact types
ylimits <- c(0, 60)
i <- 1
colors <- palette()
for (impact.type in impact.types$Var1) {
  if (nchar(impact.type) > 0 &
      impact.type != "None" &
      impact.type != "Other") {
    df.subset <- df[as.character(df$Effect..Impact.to.flight) == impact.type, ]
    df.count <- as.data.frame(table(df.subset$FlightDate))
    if (i == 1) {
      print(paste("in plot:", impact.type, colors[i], min(df.count$Freq), max(df.count$Freq)))
      plot(as.numeric(df.count$Var1),
           df.count$Freq, type="l",
           col=colors[i], xaxt="n",
          xlab="Time", ylab="#-impacts",
          ylim=ylimits,
          main="Impact Types over Time")
    } else {
      print(paste("in line:", impact.type, colors[i], min(df.count$Freq), max(df.count$Freq)))
      lines(as.numeric(df.count$Var1), 
            df.count$Freq,
            col=colors[i])
    }
    
    i <- i + 1
  }
}
x.at <- c(1, 20)
x.labels <- c("2000-01", "2001-08")
axis(1, at=x.at, labels=x.labels, las=0)
legend("topright", c("AT", "ES", "PL"), 
       fill=c(colors[1], colors[2], colors[3]), horiz=TRUE)
