import logging
import pandas
from typing import Callable, Union


def detect_header_and_indices(path: str) -> tuple:
    """Detect if the csv in `path` has header and columns, returning in the Pandas format. It only works if the first header column or first index line are strings. Numeric values will be considered as data.
    Args:
        path (str): The path to the csv file.
    Returns:
        tuple: (index_col, header), where both can be `None` (not found) or `0` (first line/column).
    """
    def _is_numeric(string: str) -> bool:
        try:
            float(string)
        except ValueError:
            return False
        return True
    df_short = pandas.read_csv(
        path, sep=None, engine='python', header=None, nrows=2, usecols=[0, 1])
    first_row_is_header = not _is_numeric(df_short.iloc[0, 1])
    header = 0 if first_row_is_header else None
    if first_row_is_header and (str(df_short.iloc[0, 0]) in "0" or str(df_short.iloc[0, 0]) == 'nan' or float(df_short.iloc[0, 0]) == 0.0):
        # when the header were detected and the [0, 0] position is
        # either empty or 0, it'll be considered an index column.
        index_col = 0
    else:
        first_column_is_index = not _is_numeric(df_short.iloc[1, 0])
        index_col = 0 if first_column_is_index else None
    return index_col, header


def load_matrix(path: str, usecols: Union[list, Callable, None] = None) -> pandas.DataFrame:
    index_col, header = detect_header_and_indices(path)
    return pandas.read_csv(path, sep=None, engine='python', header=header, index_col=index_col, usecols=usecols)
