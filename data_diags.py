import pandas as pd
import sys
import pylab as pl
import numpy as np
import numpy.ma as ma
from scipy.stats import linregress

station = sys.argv[1]

dbfile = 'data/%s.db'%station

db = pd.read_csv(dbfile, index_col=0, na_values='')

def scat(xx,yy,newfig=True):
    if newfig:
        pl.figure()
    pl.scatter(db[xx],db[yy])
    pl.xlim(min(min(db[xx]),min(db[yy])),max(max(db[xx]),max(db[yy])))
    pl.ylim(min(min(db[xx]),min(db[yy])),max(max(db[xx]),max(db[yy])))
    pl.xlabel(xx,fontsize=20)
    pl.ylabel(yy,fontsize=20)
    mask = np.isnan(db[xx])+np.isnan(db[yy])
    mask = np.logical_not(mask)
    arr = np.where(mask)
    m,yint,r,p,e = linregress(np.array(db[xx])[arr],
                              np.array(db[yy])[arr])
    pl.plot(db[xx], db[xx]*m+yint, lw=3, color='k',
            label='slope = %.2f  yint = %.2f'%(m,yint))
    pl.plot(np.arange(min(db[xx]),max(db[xx])),
            np.arange(min(db[xx]),max(db[xx])),
            'k--',lw=3)
    pl.legend(loc='upper left')
    
def histy(true, vals, field, newfig=True):
    if newfig:
        pl.figure()
    pl.hist(vals, bins=max(vals)-min(vals))
    pl.axvline(true)
    pl.xlabel(field, fontsize=20)

def three_panel(var):
    pl.figure()
    pl.subplot(221)
    scat('NAM_%s'%var,'GFS_%s'%var,newfig=False)
    pl.subplot(222)
    scat('GFS_%s'%var,'OBS_%s'%var,newfig=False)
    pl.subplot(223)
    scat('NAM_%s'%var,'OBS_%s'%var,newfig=False)
    
def calc_dist(db, vals, fields, weights):
    dist = weights[0]*np.abs(vals[0]-db[fields[0]])
    if len(vals) == 1:
        return dist
    for val,field,w in zip(vals,fields,weights)[1:]:
        dist += w*np.abs(val-db[field])
    return dist

def get_nearest_n(db, vals, fields, weights, n=100):
    dist = calc_dist(db, vals, fields, weights)
    return dist.argsort()[:n].values

def get_field_near(db, near, field):
    return db[field][near].values

#three_panel('Tmax')
#three_panel('Tmin')

err = []
for day, true in enumerate(db['OBS_Tmax']):
    near = get_nearest_n(db, 
                         [db['GFS_Tmax'][day],db['NAM_Tmax'][day]],
                         ['GFS_Tmax','NAM_Tmax'], 
                         [1.,1.], n=100)
    obs = get_field_near(db, near, 'OBS_Tmax')
    err.append(abs(np.median(obs) - true))

print err
                         
pl.figure()
pl.hist(err)

pl.show()
