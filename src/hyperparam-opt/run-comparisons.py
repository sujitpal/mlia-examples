# -*- coding: utf-8 -*-
from __future__ import division, print_function
import numpy as np
import operator

def build_terrain(terrain_sz, nbr_hills):
    terrain = np.zeros((terrain_sz, terrain_sz), dtype="float")
    for iter in range(nbr_hills):
        r = int(np.random.uniform(0, 0.2 * terrain_sz))
        xc, yc = np.random.randint(0, terrain_sz - 1, 2)
        z = 0
        xmin, xmax = int(max(xc - r, 0)), int(min(xc + r, terrain_sz))
        ymin, ymax = int(max(yc - r, 0)), int(min(yc + r, terrain_sz))
        for x in range(xmin, xmax):
            for y in range(ymin, ymax):
                z = (r ** 2) - ((x - xc) ** 2 + (y - yc) ** 2)
                if z > 0: 
                    terrain[x, y] += z
    # normalize to unit height
    zmin = np.min(terrain)
    terrain -= zmin
    zmax = np.max(terrain)
    terrain /= zmax                    
    # smooth the terrain by squaring the z values
    terrain = np.power(terrain, 2)
    # multiply by 255 so terrain can be visualized as grayscale image
    terrain = terrain * 255
    terrain = terrain.astype("uint8")
    # convert mountains to valleys since stochastic gradient DESCENT
    terrain = 255 - terrain    
    return terrain

def best_grid_search(terrain_sz, nbr_searches_per_dim):
    zvals, xvals, yvals = [], [], []
    for x in np.linspace(0, terrain_sz - 1, nbr_searches_per_dim):
        for y in np.linspace(0, terrain_sz - 1, nbr_searches_per_dim):
            xi, yi = int(x), int(y)
            xvals.append(xi)
            yvals.append(yi)
            zvals.append(terrain[xi, yi])
    grid_best = min(zvals)
    return grid_best

def best_random_search(terrain_sz, nbr_searches):
    xvals, yvals, zvals = [], [], []
    for i in range(nbr_searches):
        x = np.random.randint(0, terrain_sz, 1)[0]
        y = np.random.randint(0, terrain_sz, 1)[0]
        xvals.append(x)
        yvals.append(y)
        zvals.append(terrain[x, y])
    rand_best = min(zvals)
    return rand_best

def cooling_schedule(nbr_batches, curr_batch):
    return (nbr_batches - curr_batch) / nbr_batches

def best_batch_random_search(terrain_sz, nbr_batches, 
                             nbr_searches_per_batch,
                             nbr_winners):
    results, winners = [], []
    for bid in range(nbr_batches):
        # compute window size
        window_size = int(0.25 * terrain_sz * 
            cooling_schedule(nbr_searches_per_batch, bid))
        # jitter the winners and add their values to results
        # at any point we will only keep the top 2 global winners
        for x, y, _, _ in winners:
            if x < terrain_sz // 2:
                # left of center
                xleft = max(x - window_size // 2, 0)
                xright = xleft + window_size
            else:
                # right of center
                xright = min(x + window_size // 2, terrain_sz)
                xleft = xright - window_size
            if y < terrain_sz // 2:
                # bottom half
                ybot = max(y - window_size // 2, 0)
                ytop = ybot + window_size
            else:
                # top half
                ytop = min(y + window_size // 2, 0)
                ybot = ytop - window_size
            xnew = np.random.randint(xleft, xright, 1)[0]
            ynew = np.random.randint(ybot, ytop, 1)[0]
            znew = terrain[xnew, ynew]
            results.append((xnew, ynew, znew, bid))
        # add remaining random points
        for i in range(nbr_searches_per_batch - len(winners)):
            x = np.random.randint(0, terrain_sz, 1)[0]
            y = np.random.randint(0, terrain_sz, 1)[0]
            z = terrain[x, y]
            results.append((x, y, z, bid))
        # find the top 2 global winners
        winners = sorted(results, key=operator.itemgetter(2))[0:nbr_winners]
    batched_best = winners[0][2]
    return batched_best


########################## main ##########################

TERRAIN_SIZE = 1024
NUM_HILLS = 200

NUM_TRIALS = 1000
NUM_SEARCHES_PER_DIM = 5
NUM_WINNERS = 2

nbr_random_wins = 0
nbr_brand_wins = 0
for i in range(NUM_TRIALS):
    terrain = build_terrain(TERRAIN_SIZE, NUM_HILLS)
    grid_result = best_grid_search(TERRAIN_SIZE, NUM_SEARCHES_PER_DIM)
    random_result = best_random_search(TERRAIN_SIZE,
                                       NUM_SEARCHES_PER_DIM**2)
    batch_result = best_batch_random_search(TERRAIN_SIZE,
                                            NUM_SEARCHES_PER_DIM,
                                            NUM_SEARCHES_PER_DIM,
                                            NUM_WINNERS)
    print(grid_result, random_result, batch_result)
    if random_result < grid_result:
        nbr_random_wins += 1
    if batch_result < grid_result:
        nbr_brand_wins += 1

print("# times random search wins: {:d}".format(nbr_random_wins))
print("# times batch random search wins: {:d}".format(nbr_brand_wins))
