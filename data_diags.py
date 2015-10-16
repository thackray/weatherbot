import pandas as pd
import sys
import pylab as pl
import numpy as np
import numpy.ma as ma
from scipy.stats import linregress

station = sys.argv[1]

dbfile = 'data/%s.db'%station

db = pd.read_csv(dbfile, index_col=0, na_values='')

mask = np.isnan(db['OBS_Tmax'])+np.isnan(db['OBS_Tmin'])
#mask = np.logical_not(mask)
arr = np.where(mask)
db['GFS_diratmax'] = np.cos(db['GFS_diratmax']*np.pi/180.)
db['NAM_diratmax'] = np.cos(db['NAM_diratmax']*np.pi/180.)

#print arr
for aa in arr:
    db = db.drop(aa)

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

def get_nearest_n_plus(db, vals, fields, weights, n=100):
    dist = calc_dist(db, vals, fields, weights)
    args = dist.argsort()[:n].values
    return args, dist[args]


def get_field_near(db, near, field):
    return db[field][near].values

def get_weighted_estimate(db, field, vals, preds, weights, n=100):
    near, dists = get_nearest_n_plus(db, vals, preds, weights, n=n)
    obs = get_field_near(db, near, field)
    est1 = obs*np.exp(-dists)
    est = np.sum(est1)/np.sum(np.exp(-dists))
    return est

def get_median_estimate(db, field, vals, preds, weights, n=100):
    near = get_nearest_n(db, vals, preds, weights, n=n)
    obs = get_field_near(db, near, field)
    return np.median(obs)

def get_hist(db, truth, predictors, weights, n=30):
    err = []
    for day, true in zip(db.index,db[truth]):
        vals = [db[p][day] for p in predictors]
        est = get_median_estimate(db, truth, vals, predictors, weights, n=n)
        err.append(abs(est - true))
    pl.figure()
    pl.title(' '.join(predictors))
    pl.hist(err, bins=range(0,16))

def get_hist_weighted(db, truth, predictors, weights, n=30):
    err = []
    for day, true in zip(db.index,db[truth]):
        vals = [db[p][day] for p in predictors]
        est = get_weighted_estimate(db, truth, vals, predictors, weights, n=n)
        err.append(abs(est - true))
    pl.figure()
    pl.title(' '.join(predictors))
    pl.hist(err, bins=range(0,16))
    return err


three_panel('Tmax')
three_panel('Tmin')

get_hist_weighted(db, 'OBS_Tmin', 
         ['GFS_Tmin','NAM_Tmin', 'GFS_windatmin', 'NAM_windatmin'],
         [1.,1.,0.5,0.5])

errr = get_hist_weighted(db, 'OBS_Tmin', 
         ['GFS_Tmin','NAM_Tmin'],
         [1.,1.])

get_hist_weighted(db, 'OBS_Tmin', 
         ['GFS_Tmin','NAM_Tmin', 'GFS_windatmin', 'NAM_windatmin',
          'GFS_dptatmin', 'NAM_dptatmin'],
         [1.,1.,0.5,0.5,1.,1.])

get_hist_weighted(db, 'OBS_Tmin', 
                  ['GFS_Tmin','NAM_Tmin', 'GFS_dptatmin', 'NAM_dptatmin'],
                  [1.,1.,.5,.5])

get_hist_weighted(db, 'OBS_Tmin', 
                  ['GFS_Tmin','NAM_Tmin','GFS_Tmax','NAM_Tmax'],
                  [1.,1.,.5,.5])

get_hist_weighted(db, 'OBS_Tmax', 
         ['GFS_Tmax','NAM_Tmax'],
         [1.,1.])

pl.show()
