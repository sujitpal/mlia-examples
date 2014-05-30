from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

from livestats import livestats
import math
import os.path

DATA_DIR = "/home/sujit/Projects/med_data/cms_gov/outpatient_claims"
EPSILON = 0.0001

def summary(stats):
    summary = {}
    summary["mean"] = stats.mean()
    summary["stdev"] = math.sqrt(stats.variance())
    q1, q2, q3 = [q[1] for q in stats.quantiles()]
    summary["q1"] = q1
    summary["q2"] = q2
    summary["q3"] = q3
    return summary    
    
def norm(x, mu, sigma):
    return (1 / (sigma * np.sqrt(2 * np.pi)) *
        np.exp(-(x - mu)**2 / (2 * sigma**2)))

lns = 0
fin = open(os.path.join(DATA_DIR, "clusters.txt"), 'rb')
stats = livestats.LiveStats([0.25, 0.5, 0.75])
xs = []
for line in fin:
#    if lns > 1000: break
    line = line.strip()
    lns += 1
    x = EPSILON if line == "nan" else float(line)
    x = math.log(x, math.e)
    xs.append(x)
    # add a mirror image to make it approximately normal
#    xs.append(-x)
    stats.add(x)
#    stats.add(-x)
fin.close()

# plot data for visualization
mu = stats.mean()
sigma = math.sqrt(stats.variance())
count, bins, ignored = plt.hist(xs, bins=100, normed=True)
plt.plot(bins, [norm(x, mu, sigma) for x in bins], linewidth=2, color='r')
max_y = 0.5
#max_y = 10

# mean +/- (2*sigma or 3*sigma)
lb2 = mu - (2 * sigma)
ub2 = mu + (2 * sigma)
lb3 = mu - (3 * sigma)
ub3 = mu + (3 * sigma)
plt.plot([lb2, lb2], [0, max_y], 'r--')
plt.plot([ub2, ub2], [0, max_y], 'r--')
plt.plot([lb3, lb3], [0, max_y], 'r-')
plt.plot([ub3, ub3], [0, max_y], 'r-')

# median based (interquartile range based outlier measure)
q1, q2, q3 = [q[1] for q in stats.quantiles()]
iqr = q3 - q1
lb2 = q1 - (1.5 * iqr)
ub2 = q3 + (1.5 * iqr)
lb3 = q1 - (3.0 * iqr)
ub3 = q3 + (3.0 * iqr)
plt.plot([lb2, lb2], [0, max_y], 'g--')
plt.plot([ub2, ub2], [0, max_y], 'g--')
plt.plot([lb3, lb3], [0, max_y], 'g-')
plt.plot([ub3, ub3], [0, max_y], 'g-')

print summary(stats)

plt.show()