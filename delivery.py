from gmail import send
from pytools import pload
import sys

def make_message(info):
    subj = "Weatherbot forecast for %s"%info['station']
    mess = "Forecast valid for %s<br>"%info['fctime']
    mess += "High: %d +/- %d <br> Low: %d +/- %d"%(info['high'],info['hconf'],
                                           info['low'],info['lconf'])

    return subj, mess


if __name__=='__main__':
    
    tag = sys.argv[1]

    recipients = open('/home/thackray/weatherbot/mailinglist.%s'%tag,
                         'r').read().split('\n')

    info = pload('/home/thackray/weatherbot/'+tag+'.fc')

    subj, mess = make_message(info)

    for recip in recipients:
        send(recip, subj, mess)




