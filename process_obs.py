import pandas as pd
import numpy as np


wban = 14739 #bos

def read_raw_obs(obsfile,dbfile=None,wban=14739):
    if dbfile:
        db = pd.DataFrame.from_csv(dbfile, index_col=0)
    else:
        db = pd.DataFrame()

    with open(obsfile,'r') as f:
        lines = f.readlines()
        head = lines[0]
        keepers = [head]
        for line in lines[1:]:
            if line.startswith(str(wban)):
                keepers.append(line)
    with open('temp','w') as f:
        for line in keepers:
            f.write(line)

    newdb = pd.DataFrame.from_csv('temp', index_col=1)
    
    outdb = pd.concat([db,newdb])
    print outdb
    if dbfile:
        outdb.to_csv(dbfile)
    else:
        outdb.to_csv('%s.db'%wban)
    return


read_raw_obs('data/obs/201001daily.txt',wban=wban)
read_raw_obs('data/obs/201002daily.txt','14739.db',wban=wban)
