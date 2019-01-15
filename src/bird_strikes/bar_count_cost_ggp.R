library(ggplot2)
library(RColorBrewer)

setwd("~/Projects/datasci-class/visualization/")

df <- read.csv("BirdStrikes.csv")
df.clean <- df[df$Origin.State != "N/A", ]

# We want to produce a single bar plot where each state is represented
# by a bar. The color of the bar indicates the number of bird hits and
# the length of the bar indicates the cost incurred as a result
strikes <- as.data.frame(table(df.clean$Origin.State))
names(strikes) <- c("state", "num_hits")
costs <- as.data.frame(aggregate(
  as.numeric(Cost..Total..) ~ Origin.State, data=df.clean, FUN="sum"))
names(costs) <- c("state", "cost")
comb.strikes.costs <- merge(strikes, costs, all=TRUE)
comb.strikes.costs <- comb.strikes.costs[
  rev(order(comb.strikes.costs$cost)), ]

# clean up N/A from merged data, and add a state.level field for
# sorting by state name for ggplot. If we use state, ggplot will
# plot with the Alpha list of states, we want it sorted by cost
comb.strikes.costs <- comb.strikes.costs[
  comb.strikes.costs$state != "N/A", ]
comb.strikes.costs <- transform(comb.strikes.costs, 
                                state.level=reorder(state, cost))
comb.strikes.costs <- transform(comb.strikes.costs, 
                                hit.level=cut(num_hits, 9))

# plot the data
ggplot(comb.strikes.costs, aes(x=state.level, y=cost, colour=hit.level)) + 
  geom_bar(width=0.5, stat="identity") + 
  coord_flip() +
  labs(title="Costs by State", x="", y="(Dollars)", fill="") +
  scale_colour_brewer(palette="Reds") +
  theme(legend.position="none")
  