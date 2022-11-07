import spacepy.datamodel as dm
import spacepy.pycdf as pycdf

# sample data from https://spacepy.github.io/quickstart.html
import spacepy.datamodel as dm
mydata = dm.SpaceData(attrs={'MissionName': 'BigSat1'})
mydata['Counts'] = dm.dmarray([[42, 69, 77], [100, 200, 250]], attrs={'Units': 'cnts/s'})
mydata['Epoch'] = dm.dmarray([1, 2, 3], attrs={'units': 'minutes'})
mydata['OrbitNumber'] = dm.dmarray(16, attrs={'StartsFrom': 1})
mydata.attrs['PI'] = 'Prof. Big Shot'

pycdf.CDF.from_data('test.cdf',mydata)
