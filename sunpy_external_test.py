import pickle

case = 'read'  # 'gen' or 'read'

fsave='sunpy_pickle.sav'

if case == 'gen':
    print("Loading SunPy then generating pickle of sample SunPy data")
    import sunpy
    import sunpy.data.sample
    from sunpy.timeseries import TimeSeries as ts
    import sunpy.timeseries

    sample = ts(sunpy.data.sample.GOES_XRS_TIMESERIES)
    print(dir(sample))
    sample.peek()
    
    with open(fsave,'wb') as f:
        pickle.dump(sample,f,pickle.HIGHEST_PROTOCOL)
    
else:
    print("Reading sample SunPy data from pickle, no load of SunPy")
    with open(fsave,'rb') as f:
        myobj = pickle.load(f)
    print(dir(myobj))
    myobj.peek()
