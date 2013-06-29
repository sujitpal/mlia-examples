library(maps)
library(RColorBrewer)

df <- read.csv("BirdStrikes.csv");
df.clean <- df[df$Origin.State != "N/A", ]

bsdf <- as.data.frame(table(df.clean$Origin.State))
bsdf$Var1 = tolower(bsdf$Var1)
maxfreq <- max(bsdf$Freq)
usa <- map("state", fill=FALSE)

palette <- brewer.pal(9, "Blues")
name.idxs <- match.map(usa, bsdf$Var1, exact=FALSE)
print(name.idx)
freqs <- as.array(bsdf$Freq)
colors <- c()
for (i in 1:length(usa$names)) {
  stname <- strsplit(usa$names[i], ':')[[1]][1]
  freq <- bsdf[bsdf$Var1 == stname, ]$Freq
  if (length(freq) > 0) {
    col.idx <- round(9 * freq / maxfreq)
    if (col.idx == 0) col.idx = 1
    color <- palette[col.idx]
    colors <- cbind(colors, color)
    print(paste(usa$names[i], stname, freq, col.idx, color))
  } else {
    color <- palette[1]
    colors <- cbind(colors, color)
    print(paste(usa$names[i], stname, freq, col.idx, color))
  }
}
usa <- map("state", fill=TRUE, col=colors)
title("States by Strike Count")
leg.txt <- c("Low", "Avg", "High")
leg.cols <- c(palette[1], palette[5], palette[9])
legend("bottomright", horiz=FALSE, leg.txt, fill=leg.cols)
