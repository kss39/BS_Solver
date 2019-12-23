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
    """
    Fetchs the file as data and convert to DataBlocks.
    This method will assume that the file is valid.
    :param file: the path to the file
    :return: a list of DataBlocks
    """
    assert file.exists()
    all_data = pd.read_csv(file)
    cols = all_data.columns

    loc_ua = cols.get_loc('EOD_OPTION_PRICE_ASK')
    loc_ub = cols.get_loc('EOD_OPTION_PRICE_BID')
    loc_ivol = cols.get_loc('IVOL_LAST')
    loc_sa = cols.get_loc('EOD_UNDERLYING_PRICE_ASK')
    loc_sb = cols.get_loc('EOD_UNDERLYING_PRICE_BID')

    output = []
    for (_, day0), (_, day1), (_, day2) in zip(*[all_data.iterrows()]*3):
        u_a = (day0[loc_ua], day1[loc_ua], day2[loc_ua])
        u_b = (day0[loc_ub], day1[loc_ub], day2[loc_ub])
        ivol = (day0[loc_ivol], day1[loc_ivol], day2[loc_ivol])
        s_a = day2[loc_sa]
        s_b = day2[loc_sb]
        block = ns.DataBlock(day2['DATE'], u_a, u_b, ivol, s_a, s_b)
        output.append(block)
    return output
