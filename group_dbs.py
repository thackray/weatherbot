import pandas as pd
import sys
from datetime import datetime

station = sys.argv[1]

D = pd.DataFrame.from_csv('data/%s_NAM.csv'%station)
D2 = pd.DataFrame.from_csv('data/%s_GFS.csv'%station)
D3 = pd.DataFrame.from_csv('data/%s_OBS.csv'%station)
D.index = [dd[:10] for dd in D['fdate']]
D2.index = [dd[:10] for dd in D2['fdate']]
D3['fdate'] = [str(dd)[:10] for dd in D3.index]
D3.index = [dd[:10] for dd in D3['fdate']]

#print D2
#D.merge(D2,on='fdate', how='outer')
#print D
#D.merge(D3,on='fdate', how='outer')
#D = pd.concat([D,D2],join='outer',ignore_index=True)
D = pd.merge(left=D,right=D2,left_on='fdate',right_on='fdate')
D = pd.merge(left=D,right=D3,left_on='fdate',right_on='fdate')

D.to_csv('data/%s.db'%station)
