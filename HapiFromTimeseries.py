# Converts a SunPy Timeseries object into the HAPI python client data, meta

import numpy as np

def sun2hapi(sunpy_ts):
    cols = sunpy_ts.columns
    units = sunpy_ts.units
    # meta = sunpy_ts.meta
    df = sunpy_ts.to_dataframe()
    data = df.to_numpy
    return (data, cols)


# for testing

# 1) get sample sunpy data
print("CHECKING INITIAL SUNPY DATA")
from sunpy.timeseries import TimeSeries as ts
import sunpy.data.sample
sample = ts(sunpy.data.sample.LYRA_LEVEL3_TIMESERIES) 

print(sample.columns)
print(sample.meta)
print(sample.units)
sample.peek()

# 2) get different sample hapi data (to look at internals)
print("GETTING SOME SAMPLE HAPI DATA")
from hapiplot import hapiplot

def testdata():

    from hapiclient import hapi

    server     = 'http://hapi-server.org/servers/TestData2.0/hapi'
    dataset    = 'dataset1'
    parameters = 'scalar'
    start      = '1970-01-01T00:00:00'
    stop       = '1970-01-02T00:01:00'
    parameters = 'scalar,vector'
    opts       = {'logging': True, 'usecache': True}

    data, meta = hapi(server, dataset, parameters, start, stop, **opts)

    # Plot all parameters
    print(data)
    print(meta)
    hapiplot(data, meta)

testdata()

# 3) actual test: convert sunpy to hapi, inspect data, then plot it
print("WORKING WITH THE REAL SUNPY2HAPI DATA")
data, meta = sun2hapi(sample)

print(data)
print(meta)
meta = {'startDate':'1970-01-01Z', 'stopdate': '2016-13-31Z'
hapiplot(data,meta)

