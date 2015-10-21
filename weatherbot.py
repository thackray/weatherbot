
# datatype for sorting etc.
# mysql?
# info: forecast: lead time, Tmax, Tmin, windmin, windmax, winddir, clouds, precip
#       obs: Tmax, Tmin, windmax, precip
# data frame: date, obs_Tmax, obs_Tmin, obs_wind, obs_precip, NAM_XXz_Tmax, NAM_XXz_Tmin, NAM_XXz_wind, NAM_XXz_winddir, NAM_XXz_precip, 
#                   GFS_XXz_Tmax, ...
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from data_diags import get_weighted_estimate
import sys


station = sys.argv[1]

dbfile = 'data/%s.db'%station

db = pd.read_csv(dbfile, index_col=0, na_values='')

mask = np.isnan(db['OBS_Tmax'])+np.isnan(db['OBS_Tmin'])
#mask = np.logical_not(mask)
arr = np.where(mask)
db['GFS_diratmax'] = np.cos(db['GFS_diratmax']*np.pi/180.)
db['NAM_diratmax'] = np.cos(db['NAM_diratmax']*np.pi/180.)

for aa in arr:
    db = db.drop(aa)

vals = [70,68,6,7,48,48]
fields = ['GFS_Tmax','NAM_Tmax', 'GFS_windatmax', 'NAM_windatmax',
          'GFS_dptatmax', 'NAM_dptatmax']
high = get_weighted_estimate(db, 'OBS_Tmax', vals, fields, 
                             weights = [1., 1., 0.5, 0.5, 1., 1.])

vals = [51,52,3,2,47,48]
fields = ['GFS_Tmin','NAM_Tmin', 'GFS_windatmin', 'NAM_windatmin',
          'GFS_dptatmin', 'NAM_dptatmin']

low = get_weighted_estimate(db, 'OBS_Tmin', vals, fields, 
                             weights = [1., 1., 0.5, 0.5, 1., 1.])

print high, low
