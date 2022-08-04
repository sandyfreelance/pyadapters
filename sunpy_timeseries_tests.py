import sys

import sunpy
import sunpy.data.sample
from sunpy.timeseries import TimeSeries as ts
import sunpy.timeseries

import pyadapters # TimeSeriesToSpaceData, NDCUBE_to_SpaceData

import spacepy.plot as splot

""" Test routines for 'pyadapters'
    That can load sample SunPy data (TimeSeries, NDCube/Map) then
    load into a SpaceData object

    usage: python sunpy_timeseries_tests.py [optional_dataset_tag]

    optional_dataset_tag is any of the existing SunPy data samples:
       ESP, EVE, GBM, LYRA, NOAAIndices, NOAAPredict, NoRH, RHESSI, XRS
       or 'all' (all of the above)
    default is 'generic', a simple sine wave

    Still needs verifier for SpaceData
"""


try:
    choice = sys.argv[1]
except:
    choice = 'generic' # default to a single item

print("Analyzing ",choice)

def loadsamples(name):
    """ Loads the SunPy TimeSeries examples for each subclass
        Also does a plot via .peek() to pre-visualize and prints some info
        Usage is: timeseries = loadsamples('generic'
    """
    # the next 4 are used for DIY data creation, e.g. the 'generic' ts
    from astropy.time import TimeDelta
    import astropy.units as u
    import numpy as np
    import pandas as pd

    if name == "ESP" or name == "generic":
        if name == "ESP":
            print("No standard ESP test data yet, making a generic timeseries")
        times = sunpy.time.parse_time("now") - TimeDelta(np.arange(24 * 60)*u.minute)
        intensity = np.sin(np.arange(0, 12 * np.pi, step=(12 * np.pi) / (24 * 60)))
        df = pd.DataFrame(intensity, index=times, columns=['intensity'])
        header = {}
        units = {'intensity': u.W/u.m**2}
        sample=ts((df,header,units))
    elif name == "EVE":
        sample = ts(sunpy.data.sample.EVE_TIMESERIES, source='EVE')  
        sample = ts("http://lasp.colorado.edu/eve/data_access/evewebdata/quicklook/L0CS/LATEST_EVE_L0CS_DIODES_1m.txt", source='EVE')  
    elif name == "GBM":
        sample = ts(sunpy.data.sample.GBM_TIMESERIES, source='GBMSummary')  
    elif name == "LYRA":
        sample = ts(sunpy.data.sample.LYRA_LEVEL3_TIMESERIES) 
    elif name == "NOAAIndices":
        noaa_url = "https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json"
        sample = ts(noaa_url, source='NOAAIndices')
    elif name == "NOAAPredict":
        noaa_url = 'https://services.swpc.noaa.gov/json/solar-cycle/predicted-solar-cycle.json'  
        sample = ts(noaa_url, source='NOAAPredictIndices')  
    elif name == "NoRH":
        sample = ts(sunpy.data.sample.NORH_TIMESERIES, source='NoRH')
    elif name == "RHESSI":
        sample = ts(sunpy.data.sample.RHESSI_TIMESERIES)
    elif name == "XRS":
        sample = ts(sunpy.data.sample.GOES_XRS_TIMESERIES)

    print(sample.columns)
    print(sample.meta)
    print(sample.units)
        
    if name == "EVE":
        sample.peek(subplots=True)
    else:
        sample.peek()


    #print(dir(sample))
    #print(sample)
        
    return(sample)


def looptest(ts):
    from spacedata_to_timeseries import spacedata_to_timeseries
    # Simple test of TimeSeries -> SpaceData -> SpaceData
    # converts a ts to an sd, then converts back, then compares
    spacepyvar = pyadapters.TimeSeriesToSpaceData(test)
    newts = spacedata_to_timeseries(spacepyvar)

    ts.peek()
    newts.peek()


def spacedata_example1():
    # Generates a very simple spacedata as per the docs
    import spacepy.datamodel as	dm
    asd=dm.SpaceData()
    asd['1'] = dm.SpaceData(dog = 5, pig = dm.SpaceData(fish=dm.SpaceData(a='carp', b='perch')))
    asd['4'] = dm.SpaceData(cat = 'kitty')
    asd['5'] = 4
    asd.tree()
    return(asd)

def spacedata_example2():
    # Generates a very simple spacedata
    import spacepy.datamodel as dm
    import numpy as np

    asd=dm.SpaceData
    
    keys=['d1','d2','d3','d4']
    
    arr1 = np.array([1,2,3,4,5])
    arr2 = np.array([1,121,31,41])
    arr3 = np.array([1,121,31,41])

    asd[keys[0]]=arr1
    asd[keys[1]]=arr2
    asd[keys[2]]=arr3

    return(asd)


def load_sunpy_samplemaps():
    aia_131_map = sunpy.map.Map(sample_data.AIA_131_IMAGE)
    aia_171_map = sunpy.map.Map(sample_data.AIA_171_IMAGE)
    aia_211_map = sunpy.map.Map(sample_data.AIA_211_IMAGE)


    
def sunpy_info(test):
    # prints general info for SpacePy object
    print(dir(test))
    print("SunPy columns: ",test.columns)
    print("SunPy meta: ",test.meta)
    print("SunPy units: ",test.units)

def spacedata_info(test):
    # prints general info for SunPy object
    print(dir(test))
    print("SpacePy meta: ",test.meta)
    print("SpaceData keys: ",test.keys())
    print("SpaceData attrs: ",test.attrs)


# The actual test code

def alltests(choice):

    sample_data=['generic','ESP','EVE','GBM','LYRA',
                 'NOAAIndices','NOAAPredict','NoRH','RHESSI','XRS']

    if choice == 'all':
        choices = sample_data
    elif choice in sample_data:
        choices = [choice]
    
    for sd in choices:
        test=loadsamples(sd)
        spacepyvar = pyadapters.TimeSeriesToSpaceData(test)
        sunpy_info(suntest)
        spacedata_info(spacetest)
        #spacepyvar.tree()


# generic = 1D
# RHESSI = for each time, 9 columns
# 

"""
# sample test for cut-and-paste use
from sunpy_timeseries_tests import *
suntest=loadsamples('RHESSI')
spacetest=pyadapters.TimeSeriesToSpaceData(suntest)
sunpy_info(suntest)
spacedata_info(spacetest)
"""

suntest=loadsamples(choice)
spacetest=pyadapters.TimeSeriesToSpaceData(suntest)
sunpy_info(suntest)
spacedata_info(spacetest)
