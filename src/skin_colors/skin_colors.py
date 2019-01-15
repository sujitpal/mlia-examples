from operator import itemgetter
from random import random
import math
import matplotlib.pyplot as plt
import nltk
import numpy as np

def person():
    alleles = []
    for allele in ['a','b','c']:
        pairs = []
        for pair in range(2):
            pairs.append(allele if random() <= 0.5 else allele.upper())
        alleles.append("".join(sorted(pairs)))
    return alleles

def shuffle_and_choose(counts):
    shuffled = [x[0] for x in sorted(enumerate([random() for i in 
                range(len(counts))]), key=itemgetter(1))]
    return counts[shuffled[0]]

def compute_mating_likelihood(left, right):
    left_dominant = get_num_dominant(left)
    right_dominant = get_num_dominant(right)
    diff = abs(left_dominant - right_dominant)
    return math.exp(-diff)

def mate(left, right):
    mated_alleles = []
    for i in range(3):
        child_pairs = []
        for lp in left[i]:
            for rp in right[i]:
                child_pairs.append("".join(sorted([lp, rp])))
        mated_alleles.append(shuffle_and_choose(child_pairs))
    return mated_alleles

def get_num_dominant(allele):
    return len([c for c in "".join(allele) if c == c.upper()])    
        
def produce_next_generation(curr_gen, region_filter=None):
    next_gen = []
    males = curr_gen[:len(curr_gen)/2]
    females = curr_gen[len(curr_gen)/2:]
    i = 0
    while i < len(curr_gen):
        mptr = int(random() * len(males))
        fptr = int(random() * len(females))
        offspring = mate(males[mptr], females[fptr])
        if region_filter is not None:
            num_dominant = get_num_dominant(offspring)
            if not num_dominant in region_filter:
                if random() > 0.1:
                    continue
        next_gen.append(offspring)
        i = i + 1
    return next_gen
        
SKIN_COLORS = {
  6: 0x111111, 5: 0x6B0000, 4: 0x7B3812, 3: 0xAB671D, 
  2: 0xE0AD87, 1: 0xFDDACA, 0: 0xFEF2DF 
};

def get_color_distrib(curr_gen):
    color_dist = {k:0 for k in SKIN_COLORS.keys()}
    for alleles in curr_gen:
        num_dominant = get_num_dominant(alleles)
        color_dist[num_dominant] = color_dist[num_dominant] + 1
    dist_values = []
    for k in sorted(list(color_dist.keys())):
        dist_values.append(color_dist[k])
    return np.array(dist_values)

def plot_population_chart(color_pop, gen_title):
    xs = [str(hex(SKIN_COLORS[x])).replace("0x", "#") for x in range(7)]
    plt.bar(range(len(xs)), color_pop, color=xs)
    plt.xlabel("Skin Colors")
    plt.ylabel("Frequency")
    plt.xticks([])
    plt.title("Skin Color Distribution: %s" % (gen_title))
    plt.show()

def plot_population_drift(drift_data, title):
    generations = range(drift_data.shape[1])
    xs = range(drift_data.shape[0])
    colors = [str(hex(SKIN_COLORS[x])).replace("0x", "#") for x in xs]
    plt.stackplot(generations, drift_data, baseline="zero", colors=colors)
    plt.xlabel("Generations")
    plt.ylabel("Frequency")
    plt.title("Phenotype Drift:%s" % (title))
    plt.show()

     
# create first generation randomly of all possible genotypes, mate random
# random individuals in each generation to produce offspring over 1000 
# generations
num_generations = 100

drift_data = np.zeros((len(SKIN_COLORS), num_generations + 1))
curr_gen = [person() for i in range(2000)]
drift_data[:, 0] = get_color_distrib(curr_gen)
plot_population_chart(drift_data[:, 0], "Initial")

for i in range(num_generations):
    next_gen = produce_next_generation(curr_gen)
    drift_data[:, i+1] = get_color_distrib(next_gen)
    curr_gen = next_gen
    
plot_population_chart(drift_data[:, num_generations], "Final")    

print drift_data[:, num_generations]

plot_population_drift(drift_data, "No Dispersion")

# disperse to different regions (in each region, trigrams of skin-color 
# are possible, others are not possible due to natural adaptation)
regions = [x for x in nltk.trigrams(range(7))]
for i in range(len(regions)):
    drift_data = np.zeros((len(SKIN_COLORS), num_generations + 1))
    curr_gen = [person() for x in range(2000)]
    for j in range(num_generations):
        next_gen = produce_next_generation(curr_gen, region_filter=set(regions[i]))
        drift_data[:, j+1] = get_color_distrib(next_gen)
        curr_gen = next_gen
    plot_population_drift(drift_data, "Dispersion, Region %d" % (i+1))



    

