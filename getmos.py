from urllib2 import urlopen
import sys
from numpy import nan


def getint(string):
    try:
        x = int(string)
    except ValueError:
        x = nan
    return x


def parse_mos(moslines, model):
    time = moslines[3].split()
    i6 = []
    i = 0
    while len(i6)<2:
        if time[i] == '06':
            i6.append(i)
        i += 1
#    print i6
#    print moslines
    nx = [getint(x) for x in moslines[4].split()]
    nx = nx[1:3]
    T = [getint(x) for x in moslines[5].split()[i6[0]:i6[1]+1]]
    low = min(min(T),min(nx))
    high = max(max(T),max(nx))
    ilow = T.index(min(T))
    ihigh = T.index(max(T))
    dpt = [getint(x) for x in moslines[6].split()[i6[0]:i6[1]+1]]
    dptatmin = dpt[ilow]
    dptatmax = dpt[ihigh]
    cld = moslines[7].split()[i6[0]:i6[1]+1]
    wsp = [getint(x) for x in moslines[9].split()[i6[0]:i6[1]+1]]
    windatmin = wsp[ilow]
    windatmax = wsp[ihigh]
    if min(nx) == low:
        diurnal = True
    else:
        diurnal = False
    if max(nx) == high:
        Hdiurnal = True
    else:
        Hdiurnal = False
    
    cldfracs = []
    for c in cld:
        if c == 'CL':
            cldfracs.append(0.)
        elif c == 'SC':
            cldfracs.append(0.25)
        elif c == 'FW':
            cldfracs.append(0.5)
        elif c == 'BK':
            cldfracs.append(0.75)
        elif c == 'OV':
            cldfracs.append(1.)
        else:
            cldfracs.append(1.)
        
    cfatmax = cldfracs[ihigh]
    cfatmin = cldfracs[ilow]


    return {'%s_Tmin'%model:low, '%s_Tmax'%model:high, 
            '%s_dptatmin'%model:dptatmin, 
            '%s_dptatmax'%model:dptatmax, 
            '%s_windatmin'%model:windatmin, 
            '%s_windatmax'%model:windatmax,
            '%s_diurnal'%model:diurnal,
            '%s_diurnal_high'%model:Hdiurnal,
            '%s_cfatmax'%model:cfatmax,
            '%s_cfatmin'%model:cfatmin}


def getmos(sta):

    mospage = urlopen('http://www.nws.noaa.gov/cgi-bin/mos/getall.pl?sta=%s'%sta).read()

    chunks = mospage.split('</PRE>\n<HR WIDTH="75%">\n<PRE>\n')[:2]

    GFS = chunks[0]
    NAM = chunks[1]

    GFS = GFS.split('\n')[4:]
    NAM = NAM.split('\n')

    GFS = parse_mos(GFS, 'GFS')
    NAM = parse_mos(NAM, 'NAM')

    out = GFS
    out.update(NAM)

    return out


if __name__=='__main__':
    sta = sys.argv[1]

    print getmos(sta)
