# -*- coding: utf-8 -*-

""" Antunes Jul 21 PyAdapters project
 APL, sandy.antunes@jhuapl.edu

 Intent is the 'fromSunPy' to SpacePy and/or HAPI datamodel adapters
 This code has 2 functions so far:

 'TimeSeriesToSpaceData()' takes a SunPy 'TimeSeries' data object
 and converts it to a SpacePy 'SpaceData' object.

 'NDCubeToSpaceData()' takes a SunPy 'NDCube' data object
 and converts it to a SpacePy 'SpaceData' object.

 Testing is via 'sunpy_timeseries_tests.py'

"""

import spacepy

# REMOVE FOR ACTUAL DEV USE!!!
#import shutup; shutup.please()

""" Utilities for going FROM SunPy into SpacePy

mySpaceData = TimeSeriesToSpaceData(SunPy_TimeSeries)
mySpaceData = mapToSpaceData(SunPy_Map)
mySpaceData = ndcubeToSpaceData(SunPy_Map)



"""


def TimeSeriesToSpaceData(ts):
    """
    core data: data (a pandas.DataFrame or numpy.array)
    optional: meta (TimeSeriesMetaData obj or 'None')
         and units (dict or 'None')

    although you can access 'ts.data' directly, recommended is to
    use ts.to_dataframe() so it handles the internal data best,
    since dataframes can be made from numpy, pandas, tables, etc.
    """
    
    data = ts.to_dataframe()
    cols = ts.data.columns

    #x=ts.data.index
    #y=ts.data.values

    a_sd = spacepy.datamodel.SpaceData()

    for colname in cols:
        a_sd[colname] = ts.data[colname]

    a_sd.attrs = ts.meta
    #if ts.meta != None:
    #    # TimeSeriesMetaData exists
    #    #    meta = dict, MetaDict, tuple or list, defaults to None
    #    #    timerange is a TimeRange type, defaults to None
    #    #    colnames is a list, defaults to None
    #    a_sd['meta'] = ts.meta.meta
    #    a_sd['timerange'] = ts.data.meta.timerange
    #    a_sd['colnames'] = ts.data.meta.colnames
        
    if ts.units != None:
        a_sd['units'] = ts.units

    return a_sd


# Note SunPy 'map' and 'ndcube' are nearly identical, with 'ndcube'
# having additional WCS info. The older Map also allows for lists and not
# just numpy ndarrays

# Do I need to convert WCS to SkyCoords?

def mapToSpaceData(sunmap):
    # core data: 2D data as either 2D list or numpy/ndarray
    #       + header (dict) and optional plot_settings
    # see also MapSequence and CompositeMap for multiple maps
    # basis is the astropy.nddata container for data that also includes
    #     optional uncertainty, mask, wcs, meta & unit

    a_sd = ndcubeToSpaceData(sunmap, sunmap.header, sunmap.plot_settings)
    return a_sd

def ndcubeToSpaceData(nd, header=None, plot_settings=None):

    # core data: single numpy ndarray of data + WCS transformations
    # see NDCollections for sets of cubes + optional aligned_axes & meta
    # see NDCubeSequence for sequence of NDCubes + optional meta & common_axis

    # also works with 'mapToSpaceData' wrapper
    
    data = nd.data # numpy ndarray
    # ndarray has  .shape (tuple),
    # and optional dtype (any object), buffer (object), offset (int),
    #     strides (tuple of ints) and order (either 'C' or 'F')

    wcs = ns.wcs # astroPy wcs object
    
    # optional supplementary data
    uncert = nd.uncertainty # any type, def None
    mask = nd.mask   # any type, def None
    meta = nd.meta   # dict-like object, def None
    units = nd.units # string for the entire dataset, def None
    extra_coords = nd.extra_coords # (name, axis and array-or-obj of values)
   
    a_sd = spacepy.datamodel.SpaceData()

    a_sd['data']=data
    a_sd['wcs']=wcs
    if uncert != None: a_sd['uncertainty']=uncert
    if mask != None: a_sd['mask']=mask
    if meta != None: a_sd['meta']=meta
    if units != None:  a_sd['units']=units
    if extra_coords != None: a_sd['extra_coords']=extra_coords

    # these next 2 are only used for the map (not ndcube) class
    if header != None: a_sd['header']=header
    if plot_settings != None: a_sd['plot_settings']=plot_settings

    #a_sd.attrs = ????

    return a_sd
    
