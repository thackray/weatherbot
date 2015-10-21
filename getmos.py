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
    wsp = [getint(x) for x in moslines[9].split()[i6[0]:i6[1]+1]]
    windatmin = wsp[ilow]
    windatmax = wsp[ihigh]

    return {'%s_Tmin'%model:low, '%s_Tmax'%model:high, 
            '%s_dptatmin'%model:dptatmin, 
            '%s_dptatmax'%model:dptatmax, 
            '%s_windatmin'%model:windatmin, 
            '%s_windatmax'%model:windatmax}


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
