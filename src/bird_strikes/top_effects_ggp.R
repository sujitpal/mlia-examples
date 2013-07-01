library(ggplot2)
library(reshape2)
library(RColorBrewer)
library(scales)

setwd("~/Projects/datasci-class/visualization/")

df <- read.csv("BirdStrikes.csv")
df.clean <- df[df$Origin.State != "N/A", ]
# roll up flight dates to nearest month. We do this by replacing all
# flight dates to the first of the month, then computing the number
# of days since the epoch (1970-01-01).
df.clean$FlightDate <- as.numeric(as.Date(
  format(as.Date(df.clean$FlightDate, format="%m/%d/%Y %H:%M"), 
  "%Y-%m-01")) - as.Date("1970-01-01"))

# Populate a table whose rows are flight dates and whose columns
# are each category of bird strike impact.
flight.dates <- unique(df.clean$FlightDate)
flight.dates <- flight.dates[order(flight.dates)]
effects <- unique(df.clean$Effect..Impact.to.flight)

# build up the data frame for plotting.
plot.df <- data.frame()
for (flight.date in flight.dates) {
  df.filter <- df.clean[df.clean$FlightDate == flight.date, ]
  counts <- table(df.filter$Effect..Impact.to.flight)
  row <- c(flight.date)
  for (effect in effects) {
    if (nchar(effect) > 0) {
      effect.count <- counts[effect]
      row <- cbind(row, effect.count)
    }
  }
  plot.df <- rbind(plot.df, row)
}
names(plot.df) <- c("flight_date", "NO", "PL", "AT", "OT", "ES")

# graph the number of hits over date. We restrict it to (PL, AT, ES)
# because the others seem unimportant.
plot.df.melted <- melt(plot.df, 
  id="flight_date", measure=c("PL", "AT", "ES"))
# convert the number of days since epoch back to actual dates for 
# graphing
plot.df.melted$flight_date <- as.POSIXct(
  plot.df.melted$flight_date * 86400, origin="1970-01-01")
ggplot(plot.df.melted, 
  aes(x=flight_date, y=value, colour=variable)) +
  labs(title="Impact Types over Time", x="Flight Date", y="#-impacts") +
  theme(legend.position="bottom") +
  geom_line(stat="identity")
