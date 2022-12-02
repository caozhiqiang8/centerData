from functools import reduce
import pandas as pd


def df_merge(on,how,df):

    data = reduce(lambda left, right: pd.merge(left, right, on=on, how=how), df)
    data = data.fillna(0)
    return data
