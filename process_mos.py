import pandas as pd
import numpy as np

def read_raw_mos(mosfile,dbfile=None):
    if dbfile:
        db = pd.DataFrame.from_csv(dbfile, index_col=0)
    else:
        db = pd.DataFrame()
