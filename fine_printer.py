import pandas as pd


def fine_print(data_frame):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(data_frame)
