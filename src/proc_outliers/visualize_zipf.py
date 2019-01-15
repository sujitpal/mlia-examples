from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

from livestats import livestats
import os.path

DATA_DIR = "/home/sujit/Projects/med_data/cms_gov/outpatient_claims"
EPSILON = 0.0001

def compute_cutoff(level, cys):
    for i in range(len(cys), 0, -1):
        if cys[i-1] < level:
            return i
    return -1    
    
lns = 0
fin = open(os.path.join(DATA_DIR, "clusters.txt"), 'rb')
stats = livestats.LiveStats([0.25, 0.5, 0.75])
xs = []
for line in fin:
#    if lns > 1000: break
    line = line.strip()
    lns += 1
    x = EPSILON if line == "nan" else float(line)
    xs.append(x)
fin.close()

counts, bins, ignored = plt.hist(xs, bins=100)
cumsums = np.cumsum(counts)
plt.plot(bins[:-1], cumsums, color='red')

max_cy = len(xs)
strong_xcut = compute_cutoff(0.99 * max_cy, cumsums) / len(bins)
mild_xcut = compute_cutoff(0.95 * max_cy, cumsums) / len(bins)

print (strong_xcut, mild_xcut)

plt.plot([strong_xcut, strong_xcut], [0, max_cy], 'g-')
plt.plot([mild_xcut, mild_xcut], [0, max_cy], 'g--')

plt.show()