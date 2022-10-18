# -*- coding: utf-8 -*-

""" Antunes Oct 18 PyAdapters project
 APL, sandy.antunes@jhuapl.edu

 Intent is the 'fromSunPy' to HAPI datamodel adapters

 'TimeSeriesToHAPI()' takes a SunPy 'TimeSeries' data object
 and converts it to a HAPI CSV for data and JSON for metadata

 Testing is via 'sunpy_timeseries_tests.py'

"""

import numpy as np
import io

def TimeSeriesToHAPI(sample):
    """

    Usage: (hapidata, hapimeta) = TimeSeriesToHAPI(SunPyData)

    HAPI expects as CSV or JSON set of ordered data plus metadata of
    "HAPI": "3.0",
    "format": "csv"
    "startDate": "???"
    "stopDate": "???"
    "parameters": [ each with, at a minimum  {"name", "type", "units", "desc"}

    """

    #### SunPy warns to not use .data in favor of to_dataframe()
    #### but this is contentious-- https://github.com/sunpy/sunpy/issues/4622

    # First let us grab the data and format as csv
    hapidata = sample.data.to_csv(header=False,date_format='%d-%m-%YT%H:%M:%S.%fZ')
    
    # Now create the HAPI metadata
    
    label = sample.source # e.g. 'xrs'
    # Many but not all SunPy objects are from FITS, which has rich metadata
    # attrs for entire dataset, extracting FITS headers
    try:
        fitshdr = sample.meta.metadata[0][2]
    except:
        fitshdr = {}
    # common keys, if needed, are bitpix, naxis, extend, date,
    # telescop, instrume, object, origin,
    # date-obs, time-obs, date-end, time-end, comment, history
    # also a dup of hdrs called 'keycomments' for some reason

    startDate = sample.index[0].strftime('%d-%m-%YT%H:%M:%S.%fZ')
    stopDate=sample.index[-1].strftime('%d-%m-%YT%H:%M:%S.%fZ')
    datelength = len(startDate)
    
    # Creating HAPI metadata
    hapimeta = {"HAPI": "3.0", "startDate": startDate, "stopDate": stopDate,
                "format": "csv", "parameters": []}

    timedef = {"name": "Time",
               "type": "isotime",
               "units": "UTC",
               "length": datelength}
    hapimeta["parameters"].append(timedef)

    # populate each parameters
    for id in sample.columns:
        metasingle = {"name": id,
                      "type": "double",
                      "units": sample.units[id].to_string('generic'),
                      "desc": sample.observatory}
        
        hapimeta["parameters"].append(metasingle)


    #import json
    #hapimeta = str(json.dumps(hapimeta,indent=4))
    # convert dictionary to json string
    hapimeta = str(hapimeta).replace('\'','"')
    print("\n",hapimeta,"\n")

    print(hapimeta)
    
    return hapidata, hapimeta
