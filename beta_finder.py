from pathlib import Path
from eq_solver import data_fetcher as df
import numpy as np


blocks = df.fetch(Path('./resources/paper_data/p1.csv'))

output = open('./output/paper_data/p1.out', "w+")

grid = 5

for b in blocks:
    for beta in [0.01, 0.1, 1]:
        b.af_system(grid)
        A, f = b.af
        # sol = np.reshape(b.reg(grid, beta), (grid, grid))
        # output.write('{} solution with beta = {}:\n'.format(b.date, beta))
        # output.write(np.array2string(sol, max_line_width=np.inf, threshold=np.inf))
        # output.write("\n\n")
        # print('{} with {} finished'.format(b.date, beta))

output.close()
