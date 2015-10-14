import pandas as pd
import numpy as np
import os

wban = 14739 #bos
station = 'KBOS'
def read_raw_obs(obsfile,wban=14739,station='KBOS'):
    dbfile = 'data/%s_OBS.csv'%station
    if os.path.exists(dbfile):
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
#    print outdb
    outdb.to_csv(dbfile)
    return


for eachfile in os.listdir('data/obs'):
    if eachfile.endswith('daily.txt'):
        print eachfile
        read_raw_obs('data/obs/%s'%eachfile, wban=wban,station=station)
