from pathlib import Path

import num_solver as ns
import pandas as pd

"""
The data_fetcher package can apply to .csv files with valid declaration and data.
The file must has the following header in the first line:
    DATE, 
    EOD_OPTION_PRICE_ASK, 
    EOD_OPTION_PRICE_BID, 
    IVOL_LAST, 
    EOD_UNDERLYING_PRICE_ASK, 
    EOD_UNDERLYING_PRICE_BID.
And then the fetcher will get all continuous three days and return a list of DataBlocks.
"""


def fetch(file: Path):
    assert file.exists()
    all_data = pd.read_csv(file)