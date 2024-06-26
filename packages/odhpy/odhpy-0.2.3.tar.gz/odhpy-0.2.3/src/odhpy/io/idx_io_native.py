import os
import pandas as pd
import uuid
import shutil
import subprocess
from odhpy import utils
from .csv_io import *



def read_idx(filename) -> pd.DataFrame:
    """_summary_

    Args:
        filename (_type_): Name of the IDX file.

    Returns:
        pd.DataFrame: _description_
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File does not exist: {filename}")
    # Read ".idx" file
    with open(filename, 'r') as f:
        # Skip line
        stmp = f.readline()
        # Start date, end date, date interval
        stmp = f.readline().split()
        date_start = pd.to_datetime(stmp[0], dayfirst=True)
        date_end = pd.to_datetime(stmp[1], dayfirst=True)
        date_flag = int(stmp[2])
        nseries = 0
        snames = []
        for line in f:
            sfile = line[0:13].strip()
            sdesc = line[13:54].strip()
            sname = f"{nseries + 1}>{sfile}>{sdesc}"
            snames.append(sname)
            nseries += 1
    # Read ".out" file
    out_filename = filename.lower().replace('.idx', '.out')
    if not os.path.exists(out_filename):
        raise FileNotFoundError(f"File does not exist: {out_filename}")
    # 4-byte reals
    b_types = [(s, 'f4') for s in snames]
    # Skip first record
    b_offset = nseries * 4
    b_data = np.fromfile(out_filename, dtype=np.dtype(b_types), offset=b_offset)
    if date_flag == 0:
        daily_date_values = utils.datetime_functions.get_dates(date_start, end_date=date_end, include_end_date=True)
        df = pd.DataFrame.from_records(b_data, index=daily_date_values)
        df.columns = snames
    elif date_flag == 1:
        raise NotImplementedError("Monthly data not yet supported")
    elif date_flag == 3:
        raise NotImplementedError("Annual data not yet supported")
    else:
        raise ValueError(f"Unsupported date interval: {date_flag}")
    return df



def write_idx_native(df, filename):
    raise NotImplementedError("Native implementation for writing IDX files is not yet supported")
