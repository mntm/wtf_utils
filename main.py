#!/usr/bin/env python3

from datetime import datetime, timedelta
from pytz import timezone
import pytz
import struct

mtl = timezone("America/Toronto")
fmt = "%Y %m %d %H %M %S %f %Z %z"
pad = 116444736000000000

epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000


# Take a int value and return its representation in little indian as string
def to_little_endian (i):
    pack = struct.pack('<Q',i)
    import binascii
    return binascii.hexlify(pack)


def datetime_to_WTF_timestamp(dt,tz=None):
    if tz==None :
        d1 = pytz.utc.localize(dt)
    else:
        d1 = tz.localize(dt).astimezone(pytz.utc)
    return int(unix_time_millis(d1) * 10000 + pad)


def WTF_timestamp_to_datetime(ts, tz=None):
    unix_epoch = (ts - pad) / 10000000
    modulo = int (((ts - pad) % 10000000)/10)
    d = datetime.fromtimestamp(unix_epoch,tz)
    d.replace(microsecond=modulo)
    return d
    
if __name__ == "__main__":
    
    d1 = datetime(2018, 12, 4, 0, 46,51,103680)
    timestamp = datetime_to_WTF_timestamp(d1,mtl)
    print ("debut:\t\t%s" % (to_little_endian(timestamp)))
    d1 = datetime(2018, 12, 4, 0, 46,55,342015)
    timestamp = datetime_to_WTF_timestamp(d1,mtl)
    print ("fin:\t\t%s" % (to_little_endian(timestamp)))
    print ("Test:\t\t%s" % (to_little_endian(131511664248689449)))


    

