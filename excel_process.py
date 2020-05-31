import pandas as pd
import numpy as np
import glob
from eq_solver import num_solver as ns


folder = "./resources/530data"
output_folder = "./output/530data"

for file in glob.glob(f'{folder}/*.xlsx'):
    print(file)


def process_excel_file(file):
    df = pd.open_excel(file).T
    max_column = df.columns.stop
    for option_index in range(2, max_column, step=7):
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
                # TODO: solve this. LAST PRICE???
                stock_ask = data_block.iat[2, 3]
                stock_bid = data_block.iat[2, 4]
                input_data = ns.DataBlock(today=today, option_ask=option_ask, option_bid=option_bid, volatility=volatility, stock_ask=stock_ask, stock_bid=stock_bid)
                # TODO: Solve the dataform
            except ValueError as _:
                break
