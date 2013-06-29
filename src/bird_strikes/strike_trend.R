df <- read.csv("BirdStrikes.csv");

#par(mfrow=c(2,1))

# find counts by flight date
fdds <- as.data.frame(table(df$FlightDate))
fdds$Var1 <- as.Date(fdds$Var1, format="%m/%d/%Y %H:%M")
fdds.sorted <- fdds[with(fdds, order(Var1)), ]
plot(fdds.sorted$Var1, fdds.sorted$Freq, type="l",
     xlab="Flight Date", ylab="Bird Strikes", 
     main="Bird Strikes (daily)")
# compute trend line and place
model <- lm(fdds.sorted$Freq ~ fdds.sorted$Var1)
abline(model, col="red", lwd=4)

# roll up by month to generate trend line. We want to stay on
# the same scale so we rollup all dates to the first of the
# corresponding month
df.rollup <- df
df.rollup$FlightDate <- as.Date(format(as.Date(
  df$FlightDate, format="%m/%d/%Y %H:%M"), "%Y-%m-01"))
roldf <- as.data.frame(table(df.rollup$FlightDate))
# scale the summed frequency down to day (ie 1/30)
roldf$Var1 <- as.Date(roldf$Var1)
roldf$Freq <- roldf$Freq / 30
# sort by date
roldf.sorted <- roldf[with(roldf, order(Var1)), ]
plot(roldf.sorted$Var1, roldf.sorted$Freq, type="l",
     xlab="Flight Date", ylab="Bird Strikes", 
     main="Bird Strikes (monthly)")
# compute trend line and place
model <- lm(roldf.sorted$Freq ~ roldf.sorted$Var1)
abline(model, col="red", lwd=4)

# reset
#par(mfrow=c(1,1))
