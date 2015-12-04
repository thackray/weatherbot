Tmax_config = {'confidence_intervals':[2.,0.2,0.02],
               'predictors':['NAM_Tmax','NAM_cloudcatatmax'],
               'weights':[1.,999.],
               }
total_config = {'forecast_quantities':['Tmax'],
                'Tmax':Tmax_config,
                }

class Weatherbot(object):
    def __init__(self, station=None,configfile=None,configdict=None):
        self.station = station
        self.configfile = configfile
        self.configdict = configdict
        return
    def deliver_forecast(self):
        pass
    def estimate_quantity(self,field):
        return estimate, variance, confidence
    def set_station(self, station):
        self.station = station
                
    def get_config(self, configfile=None):
        """read parameters for estimation from file
        include what should be forecast and weights etc. to use
        parameters for each quantity predicted:
        - confidence levels: e.g. [2,0.2,0.02]
        - predictors: e.g. [Tmax, cloudcategory, datecategory]
        - weights: e.g. [1,999,999]"""
        pass
    
