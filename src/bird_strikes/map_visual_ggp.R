library(maps)
library(ggplot2)
library(RColorBrewer)

setwd("~/Projects/datasci-class/visualization/")

df <- read.csv("BirdStrikes.csv")
df.clean <- df[df$Origin.State != "N/A", ]

usa.map <- map_data("state")

# produce a data frame (region, val) where region is the 
# lowercased state name and val is the number of bird hits.
# We want to merge it with usa.map$region
hits.by.state <- as.data.frame(table(df.clean$Origin.State))
names(hits.by.state) <- c("region", "val")
total.hits <- sum(hits.by.state$val)
hits.by.state$region <- tolower(hits.by.state$region)

# merge the bird strike data in
usa.map.with.hits <- merge(usa.map, hits.by.state, by="region", all=TRUE)
usa.map.with.hits <- usa.map.with.hits[order(usa.map.with.hits$order), ]

# plot the data
colors <- brewer.pal(9, "Reds")
(qplot(long, lat, data=usa.map.with.hits, geom="polygon", 
       group=group, fill=val)) +
  theme_bw() +
  labs(title="States by Strike Count", x="", y="", fill="") + 
  scale_fill_gradient(low=colors[1], high=colors[9]) +
  theme(legend.position="bottom", legend.direction="horizontal")
