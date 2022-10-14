""" Known fields from xrs:

xrsa & xrsb have
bitpix: 8, naxis: 0, date: 26/06/2012, numext: 3,
telescop: GOES 15, instrume: X-ray Detector, object: Sun, origin: SDAD/GSFC,
date-obs: 07/06/2011, time-obs: 00:00:00.000,
date-end: 07/06/2011, time-end: 23:59:57.632,
comment: Energy band information given in extensio
history:
keycomments: {'SIMPLE': 'Written by IDL: Tue Jan'}

units = ordered dict, e.g. xrsa: Unit("W/m2"), xrsb: Unit("W/m2")
data = 42177 rows x 2 columns
sample.source = 'xrs'
meta = all that FITS stuff

print(meta.to_string(depth=48))


Separate data by units, keep dimensionality
Likely need 3 sets of Attributes
(1) describe data and relationships
(2) technically compliant
DISPLAY_TIME: 'time_series', VAR_TYPE: 'data' or 'support_data' or 'metadata'
'FIELD_NAME' = eh, make it match col name,
DEPEND_0 = 'name of time var', DEPEND_1 = '[0, 1, 2]' etc, unless there is
   only 1 var (DEPEND_2 if a two-d variable)
(3) glom the extras
see also https://spdf.gsfc.nasa.gov/istp_guide/vattributes.html

Testing needed:
(top level): python setup.py build
(in tests directory) python test_all.py
(or test_datamodel, etc)
python test_datamodel.py converterTests.test_toHDF5ListString
python test_datamodel.py converterTests

Testing Spacedata-> dump to CDF and plot in AutoPlot

Need to support Python 3.7 & 3.8,
SunPy 4.0, 3.1, 3.0, NDCube 2.0 (1.2 if possible)


Tell Jon if any generic functions are needed for making Spacedata


Suggestions: move docstrings -> Sphinx?
enumsfor dixcts (and Andrew's datatype checking)
Exception handling, if in != out datatypes, etc
SunPy 'TimeRange' -> SpacePy Epoch (or TickTock? Eh, Epoch)
line 110 'uncert' -> 'uncertainty' as in sunpy.???
shift personal notes to # Dev notes
static type the conversion routine? (after 3.6 is good practice)

Tell him which version of SunPy this works with, but we don't list it as a
Dependency, right?  (Because it relies on the object!)


"""

import spacepy

sd = spacepy.SpaceData()

import pickle
with open('sunpy_pickle.sav','rb') as f:
    sample=pickle.load(f)

#sd['Epoch'] = spacepy.dmarray(sample.index)
#sd['xrs'].attrs['DISPLAY_TYPE']='time_series'
#sd['xrs'].attrs['VAR_TYPE']='support_data'

# or

sd['Epoch'] = spacepy.dmarray(sample.index,
                              attrs = {'DISPLAY_TYPE': 'time_series',
                                       'VAR_TYPE': 'support_data',
                                       'FIELDNAM': 'epoch',
                                       'FORMAT': 'I22',
                                       'LABLAXIS': 'Epoch',
                                       'MONOTON': 'INCREASE'})

# sample for e.g. a 3-vect.  Skip for 1-vects
sd['xrs_index']=spacepy.dmarray([1,2,3],
                                  attrs={'CATDESC': 'index for B coords',
                                         'FIELDNAM': 'index for B coords',
                                         'FORMAT': 'I10',
                                         'UNITS': ' ',
                                         'VAR_TYPE': 'metadata'})

sd['label_SC']=spacepy.dmarray(
    ['B_X','B_Y','B_Z'],
    attrs={'CATDESC': 'Labels for B in SC coordinates',
           'FIELDNAM': 'Labels for B in SC coordinates',
           'FORMAT': 'A3',
           'UNITS': ' ',
           'VAR_TYPE': 'metadata'})

# could do each as its own, or as a 2-vect
#### SunPy warns to not use .data in favor of to_dataframe()
#### but this is contentious-- https://github.com/sunpy/sunpy/issues/4622
###sd['xrs']=spacepy.dmarray([sample.data['xrsa'].to_numpy(),sample.data['xrsb'].to_numpy()])
sd['xrs']=spacepy.dmarray([sample.data['xrsa'].to_numpy(),sample.data['xrsb'].to_numpy()])


# ALSO make sure the above is a numpy array, if not cast it to that


#sd['xrs'].attrs['CAT_DESC']='whatever'
#sd['xrs'].attrs['object']='Sun' # etc etc
#sd['xrs'].attrs['DISPLAY_TYPE']='time_series'
#sd['xrs'].attrs['VAR_TYPE']='data'
#sd['xrs'].attrs['FIELD_NAME']='xrs'
#sd['xrs'].attrs['DEPEND_0']='Epoch'
#sd['xrs'].attrs['DEPEND_1']='xrs_index'

                          
# or
sd['xrs'].attrs = {'CATDESC': 'Magnetic field in SC coordinntes (1 min cadence)',
                   'DEPEND_0': 'Epoch',
                   'DEPEND_1': 'xrs_index',
                   'DISPLAY_TYPE': 'time_series',
                   'FIELD_NAME': 'xrs',
                   'VAR_TYPE': 'data',
                   'object': 'Sun',
                   'FILLVAL': -1e+31,
                   'FORMAT': 'E12.2',
                   'LABLAXIS': 'B_SC',
                   'LABL_PTR_1': 'label_SC',
                   'SCALETYP': 'linear',
                   'SI_conv': '1.0e-9->Tesla',
                   'UNITS': 'nT', # also VALIDMAX, VALIDMIN lists of same size?
                   }

                 
print(sd)
print(dir(sd))
