import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

wban = '12842'
station = 'KTPA'
iii = 0
def read_raw_obs(obsfile,wban=14739,station='KBOS'):
    global iii
    dbfile = 'data/%s_OBS.csv'%station
    if os.path.exists(dbfile):
        db = pd.DataFrame.from_csv(dbfile, index_col=0)
    else:
        db = pd.DataFrame()

    with open(obsfile,'r') as f:
        lines = f.readlines()
        head = lines[0]
        keepers = [',fdate,OBS_maxwind,OBS_Tmax,OBS_Tmin,OBS_precip\n']
        for line in lines[1:]:
            ll = line.split(',')
            if ll[0] in [str(wban)]:
                fdate1 = ll[1][:4]+'-'+ll[1][4:6]+'-'+ll[1][6:]
                fdatetime = datetime.strptime(fdate1,'%Y-%m-%d')
                fdate = (fdatetime-timedelta(days=1)).strftime('%Y-%m-%d')
                keepers.append(','.join([str(iii),fdate,
                                         ll[-4].replace('M','NaN'),
                                         ll[2].replace('M','NaN'),
                                         ll[4].replace('M','NaN'),
                                         ll[30].replace('M','NaN')])+'\n')
                iii += 1
    with open('temp','w') as f:
        for line in keepers:
            f.write(line)

    newdb = pd.DataFrame.from_csv('temp', index_col=0)
    
    outdb = pd.concat([db,newdb])
#    print outdb
    outdb.to_csv(dbfile)
    return

dircont = os.listdir('data/obs')
dircont.sort()
for eachfile in dircont:
    if eachfile.endswith('daily.txt'):
        print eachfile
        read_raw_obs('data/obs/%s'%eachfile, wban=wban,station=station)
