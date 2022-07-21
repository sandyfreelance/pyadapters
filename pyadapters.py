# Antunes Jul 21 PyAdapters project
# APL, sandy.antunes@jhuapl.edu

import spacepy

# REMOVE FOR ACTUAL DEV USE!!!
#import shutup; shutup.please()

""" Utilities for going FROM SunPy into SpacePy

mySpaceData = TimeSeriesToSpaceData(SunPy_TimeSeries)
mySpaceData = mapToSpaceData(SunPy_Map)
mySpaceData = ndcubeToSpaceData(SunPy_Map)



"""


def TimeSeriesToSpaceData(ts):
    # core data: data (a pandas.DataFrame or numpy.array)
    # optional: meta (TimeSeriesMetaData obj or 'None')
    #      and units (dict or 'None')


    # although you can access 'ts.data' directly, recommended is to
    # use ts.to_dataframe()
    data = ts.to_dataframe()
    cols = ts.data.columns

    #x=ts.data.index
    #y=ts.data.values

    asd = spacepy.datamodel.SpaceData()

    
    for colname in cols:
        asd[colname] = ts.data[colname]

    asd.attrs = ts.meta
    #if ts.meta != None:
    #    # TimeSeriesMetaData exists
    #    #    meta = dict, MetaDict, tuple or list, defaults to None
    #    #    timerange is a TimeRange type, defaults to None
    #    #    colnames is a list, defaults to None
    #    asd['meta'] = ts.meta.meta
    #    asd['timerange'] = ts.data.meta.timerange
    #    asd['colnames'] = ts.data.meta.colnames
        
    if ts.units != None:
        asd['units'] = ts.units

    return(asd)


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

    asd = ndcubeToSpaceData(sunmap, sunmap.header, sunmap.plot_settings)
    
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
   
    asd = spacepy.datamodel.SpaceData()

    asd['data']=data
    asd['wcs']=wcs
    if uncert != None: asd['uncert']=uncert
    if mask != None: asd['mask']=mask
    if meta != None: asd['meta']=meta
    if units != None:  asd['units']=units
    if extra_coords != None: asd['extra_coords']=extra_coords

    # these next 2 are only used for the map (not ndcube) class
    if header != None: asd['header']=header
    if plot_settings != None: asd['plot_settings']=plot_settings

    #asd.attrs = ????

    return(asd)
    
