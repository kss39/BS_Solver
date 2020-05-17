import numpy as np
from pathlib import Path
from eq_solver import data_fetcher as df
from eq_solver import num_solver as ns


blocks = df.fetch(Path('./resources/paper_data/p1.csv'))

output = open('./output/paper_data/p1_new.out', "w+")

beta = 0.01
grid = 20

for b in blocks:
    b.af_system(grid)
    A, f = b.af
    res = ns.tikhonov(A, f, beta)
    res = res.reshape((grid, grid))
    output.write('{} solution with (grid = {}, beta = {}):\n'.format(b.date, grid, beta))
    output.write(np.array2string(res, max_line_width=np.inf, threshold=np.inf))
    output.write("\n\n")
    print('{} with (grid = {}, beta = {}) finished'.format(b.date, grid, beta))

output.close()
