import math
import pandas as pd
import numpy as np
import glob
from pathlib import Path
from eq_solver import num_solver as ns

grid = 20
beta = 0.001
folder = "./resources/531data"
output_folder = "./output/531data"


def process_csv_file(file):
    df = pd.read_csv(file).T
    output_dictionary = {'option_name': [], 'grid_count': [], 'beta':[], 'date': [], 'minimizer':[]}
    output_dt = pd.DataFrame(output_dictionary)
    max_column = df.columns.stop
    for option_index in range(2, max_column, 7):
        option_name = df[option_index][0]
        day_count = len(df[option_index])
        for i in range(2, day_count - 2):
            today = df.iat[i+2, option_index]
            data_block = df.iloc[i:i+3, option_index+1:option_index+6]
            try:
                data_block = data_block.apply(pd.to_numeric)
                # Then the 3-day data is good for us
                option_ask = data_block.iloc[:, 1].values
                option_bid = data_block.iloc[:, 2].values
                volatility = data_block.iloc[:, 0].values
                stock_ask = math.ceil(data_block.iat[2, 3] * 100) / 100
                stock_bid = math.floor(data_block.iat[2, 4] * 100) / 100
                if stock_ask == stock_bid:
                    break
                input_data = ns.DataBlock(today=today, option_ask=option_ask, option_bid=option_bid, volatility=volatility, stock_ask=stock_ask, stock_bid=stock_bid)
                input_data.af_system(grid)
                A, f = input_data.af
                res = ns.tikhonov(A, f, beta)
                row = {'option_name': option_name, 'grid_count': grid, 'beta': beta, 'date': today, 'minimizer': np.array2string(res, max_line_width=np.inf, threshold=np.inf)}
                output_dt = output_dt.append(row, ignore_index=True)
            except ValueError as _:
                pass
            except np.linalg.LinAlgError as _:
                pass
        print(f'Solved {option_name}')
    filename = Path(file).stem
    output_file = f'{output_folder}/{filename}_out.csv'
    output_dt.to_csv(f'{output_folder}/{filename}_out.csv')

for file in glob.glob(f'{folder}/p1.csv'):
    print('Processing', file, ': ')
    process_csv_file(file)
