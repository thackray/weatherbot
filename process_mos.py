import pandas as pd
import numpy as np
from datetime import datetime, timedelta

aday = timedelta(days=1)

def process_chunk(chunk):
    nx = []
    T = []
    dpt = []
    cld = []
    wdr = []
    wsp = []

    for line in chunk:
        sline = line.split(',')
        aa = sline[4]
        try: nx.append(float(aa))
        except: pass
        T.append(float(sline[5]))
        dpt.append(float(sline[6]))
        cld.append(7)
        wdr.append(float(sline[8]))
        wsp.append(float(sline[9]))

    fdate = datetime.strptime(sline[2][:10],'%Y-%m-%d')
    Tmin = min(T+nx)
    mindex = T.index(min(T))
    Tmax = max(T+nx)
    maxdex = T.index(max(T))
    avgwind = np.mean(wsp)
    windatmin =  wsp[mindex]
    windatmax = wsp[maxdex]
    diratmin = wdr[mindex]
    diratmax = wdr[maxdex]
    avgdpt = np.mean(dpt)
    dptatmin = dpt[mindex]
    dptatmax = dpt[maxdex]
    
    return  [fdate, Tmin, Tmax, avgwind, windatmin, windatmax,
              diratmin, diratmax, avgdpt, dptatmin, dptatmax]


    

def read_raw_mos(mosfile,model='GFS'):
    with open(mosfile, 'r') as f:
        moslines = f.readlines()
    moslines = moslines[1:]
    
    interval = 21
    six1,six2 = 4,12
    linesleft = len(moslines)
    newdblines = []

    i = 0
    while linesleft > interval:
        chunk = moslines[i+six1:i+six2]
        newdbline  = process_chunk(chunk)
        print newdbline
        newdblines.append(newdbline)
        i += interval
        linesleft -= interval

    db = np.array(newdblines)
    cols = ['fdate', 'Tmin', 'Tmax', 'avgwind', 'windatmin', 'windatmax',
            'diratmin', 'diratmax', 'avgdpt', 'dptatmin', 'dptatmax']

    cols = [cols[0]]+[model+'_'+c for c in cols[1:]]

    DF = pd.DataFrame(data=db,columns=cols)
    DF.to_csv('data/'+mosfile[:4]+'_'+model+'.csv')
    
read_raw_mos('KBOS_gfs12z.csv',model='GFS')
read_raw_mos('KBOS_nam12z.csv',model='NAM')
        
        

