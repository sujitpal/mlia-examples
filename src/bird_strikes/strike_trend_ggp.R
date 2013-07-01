library(ggplot2)
library(RColorBrewer)

setwd("~/Projects/datasci-class/visualization/")

df <- read.csv("BirdStrikes.csv")
df.clean <- df[df$Origin.State != "N/A", ]

# draw line chart of number of bird hits by flight date.
# Convert flight date to Date so we can sort
hit.dates <- as.data.frame(table(df$FlightDate))
names(hit.dates) <- c("flight_date", "num_hits")
hit.dates$flight_date <- as.Date(hit.dates$flight_date, 
                                 format="%m/%d/%Y %H:%M")

# Compute trend line and plot
trend <- lm(hit.dates$num_hits ~ hit.dates$flight_date)
trend.coeffs <- as.array(coef(trend))

# graph the number of hits over date
ggplot(data=hit.dates, aes(x=flight_date, y=num_hits, group=1)) + 
  geom_line() +
  labs(title="Bird Strikes by Date", x="Flight Date", y="#-hits") +
  geom_abline(intercept=trend.coeffs[[1]], slope=trend.coeffs[[2]], 
              color="red", size=2)

