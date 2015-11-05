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
    dist = weights[0]*np.abs(vals[0]-db[fields[0]].values)
    print dist
    if len(vals) == 1:
        return dist
    for val,field,w in zip(vals,fields,weights)[1:]:
        dd = w*np.abs(val-db[field].values)
        print dd
        dist += dd
    print dist
    return dist

def get_nearest_n(db, vals, fields, weights, n=100):
    if xx:
        db.drop(xx)
    dist = calc_dist(db, vals, fields, weights)
    return dist.argsort()[:n]

def get_nearest_n_plus(db, vals, fields, weights, n=100, xx=None):
    dist = calc_dist(db, vals, fields, weights)
    if xx:
        args = dist.argsort()[1:n+1]
    else:
        args = dist.argsort()[:n]
    return args, dist[args]


def get_field_near(db, near, field):
    return db[field][near].values

def get_weighted_estimate(db, field, vals, preds, weights, n=100, xx=None):
    near, dists = get_nearest_n_plus(db, vals, preds, weights, n=n,xx=xx)
    obs = get_field_near(db, near, field)
    est1 = obs*np.exp(-1*dists)
    est = np.sum(est1)/np.sum(np.exp(-1*dists))
    return est

def get_weighted_estimate_plus(db, field, vals, preds, weights, n=100,xx=None,
                               verbose=False):
    near, dists = get_nearest_n_plus(db, vals, preds, weights, n=n,xx=xx)
    if verbose:
        print tabview(db,near,dists,preds+[field])
    obs = get_field_near(db, near, field)
    weights = np.exp(-dists)
    est1 = obs*weights
    est = np.sum(est1)/np.sum(weights)
    pref = np.sum(weights)/(np.sum(weights)**2.-np.sum(weights**2.))
    #pref = 1/np.sum(weights)
    confidence = np.sum(weights*((obs-est)**2))*pref
    return est, confidence**0.5

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
        est = get_weighted_estimate(db, truth, vals, predictors, weights, n=n,
                                    xx=day)
        err.append(abs(est - true))
    pl.figure()
    pl.title(truth+' '+' '.join(predictors))
    pl.hist(err, bins=range(0,16))
    return err

def get_hist_mos(db, truth, models):
    err = []
    for day, true in zip(db.index,db[truth]):
        vals = [db[p][day] for p in models]
        if len(vals) > 1:
            est = np.mean(vals)
        else:
            est = vals[0]
        err.append(abs(est - true))
    pl.figure()
    pl.title('mos '+truth+' '+' '.join(models))
    pl.hist(err, bins=range(0,16))
    return err

def tabview(db,near,dists,fields):
    string = ' dist  '
    string += ' '.join([f.ljust(14) for f in fields])+'\n'
    for i,d in zip(near,dists):
        string += str(d).ljust(7)
        string +=  ' '.join([str(db[field][i]).ljust(14) for field in fields]) + '\n' 
    return string

if __name__=='__main__':
    three_panel('Tmax')
    three_panel('Tmin')

    errr = get_hist_weighted(db, 'OBS_Tmin', 
                             ['GFS_Tmin','NAM_Tmin'],
                             [1.,1.])

    get_hist_mos(db, 'OBS_Tmin', ['GFS_Tmin'])
    get_hist_mos(db, 'OBS_Tmin', ['NAM_Tmin'])
    get_hist_mos(db, 'OBS_Tmin', ['GFS_Tmin','NAM_Tmin'])


    get_hist_weighted(db, 'OBS_Tmin', 
                      ['GFS_Tmin','NAM_Tmin', 'GFS_windatmin', 'NAM_windatmin'],
                      [1.,1.,0.5,0.5])

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

    get_hist_mos(db, 'OBS_Tmax', ['GFS_Tmax'])
    get_hist_mos(db, 'OBS_Tmax', ['NAM_Tmax'])
    get_hist_mos(db, 'OBS_Tmax', ['GFS_Tmax','NAM_Tmax'])


    get_hist_weighted(db, 'OBS_Tmax', 
                      ['GFS_Tmax','NAM_Tmax', 'GFS_windatmax', 'NAM_windatmax'],
                      [1.,1.,0.5,0.5])

    get_hist_weighted(db, 'OBS_Tmax', 
                      ['GFS_Tmax','NAM_Tmax', 'GFS_windatmax', 'NAM_windatmax',
                       'GFS_dptatmax', 'NAM_dptatmax'],
                      [1.,1.,0.5,0.5,1.,1.])

    get_hist_weighted(db, 'OBS_Tmax', 
                      ['GFS_Tmax','NAM_Tmax', 'GFS_dptatmax', 'NAM_dptatmax'],
                      [1.,1.,.5,.5])

    get_hist_weighted(db, 'OBS_Tmax', 
                      ['GFS_Tmin','NAM_Tmin','GFS_Tmax','NAM_Tmax'],
                      [1.,1.,.5,.5])


    pl.show()
