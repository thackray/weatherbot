
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

base = datetime(2015,8,1)
numdays = 365
dates = [base - timedelta(days=x) for x in range(0,numdays)]
print dates
