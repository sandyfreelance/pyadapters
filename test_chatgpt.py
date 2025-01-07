"""
Experiment: try ChatGPT 4o to make an adapter for SunPy TimeSeries to plottable
HAPI Python object.  Build using the 'GBMSummary' dataset then cross-test
using 'EVE'.

Took 47 minutes, roughly a dozen iterations.  Required I inspect the code
when the same error came up and apply some of my domain knowledge of the
data, but not much deep diving into the APIs.  

It provided sample 'blank' invocations i.e. assuming the SunPy TimeSeries
was populated.  It tried to make a test code but that was too vague and
also assumed the SunPy TimeSeries was a 'file' even though its code assumed
rightly it was a populated object.  Once I provided it with a valid test
routine, we were able to roll.

It could not run the code directly because of required package installed,
so we iterated with 'I run test and feed back errors'.  It got stuck on
one set of metadata errors, until I realized it was assuming all data
columns were time fields.  It also kept failing to include imports at
the top of the main code (easily remedied manually, but I had to remember
to do so).

This was a very rapid and useful way to approach this.  It required data
saavyness by me and some knowledge of SunPy and HAPI.  Its code had
novice bugs but was readable and had reasonable comments.  The code itself
was short enough to visualize.

This was a little like working with a summer intern who knows coding but
not the problem space, and requires handholding.  The development was
more enjoyable and more rapid than starting solo from scratch.  I recommend
we look into ChatGPT for future adapters-like projects.

"""

import sunpy
import sunpy.data.sample
from sunpy.timeseries import TimeSeries as ts
import sunpy.timeseries

import hapiplot

sample = ts(sunpy.data.sample.EVE_TIMESERIES, source='EVE')
#sample = ts(sunpy.data.sample.GBM_TIMESERIES, source='GBMSummary')
#sample.peek() #subplots=True)

import chatgpt_sunpy2hapi as sh
hapidata, hapimeta = sh.convert_timeseries_to_hapi(sample)

hapiplot.hapiplot(hapidata, hapimeta)

"""
It took 47 minutes to create with ChatGPT 4o.  The initial prompt loading was:

> The Heliophysics API (HAPI) is described at https://hapi-server.org/ and has Python clients.  The SunPy Python package is described at sunpy.org.  HAPI uses a named numpy array to store CSV data.  SunPy uses an internal TimeSeries data type.

Then my ask:

> Please write Python code to convert a SunPy TimeSeries object to a HAPI python object.

(v1)

> This code needs to also create and return the 'hapimeta' metadata. For an example, see the usage in the 'hapiplot' package of "hapiplot.hapiplot(hapidata, hapimeta).

(v2)

> Here is my test code, attached.  It fails with "[redact]"


(It tried to run it and said):
It seems the required package astropy, which is a dependency of SunPy, is not available in this environment. This library is essential for handling time conversions in astronomical contexts.

You can test the updated code locally in an environment where astropy, sunpy, and hapiplot are installed. Here’s the updated code again:

(v3)

> I still get this error: "[redact]"

(v4)

> I still get the same error: "[redact]"

(v5)

(I did deeper manually because ChatGPT is stuck)
> This syntax is the part that is failing and causing the above errors: ">>> for col in data.columns:
...     print(ts.meta.get(col, {}).get("units", "unknown"))".  Can you write a different way to populate the metadata?

(v6)

> Your code is missing two imports, 'import numpy as mp' and 'from sunpy.timeseries import TimeSeries'.  Once I added those two lines, I still get an error: "[redact]"

(v7)

(More manual analysis by me)

> Your problem is assuming all units are some form of time.  Most units are not time.  So 'test.meta.get' will always fail.  For example, "ts.meta.get("4-15 keV", "units")" fails with the same error as before.  Please use a different method than 'ts.meta.get' to extract and populate the metadata.  The units are not important because they are descriptive.

(v8)

> Thank you. There is still something weird, 'hapiplot' returns this error: "Traceback (most recent call last):
  File "/Users/antunak1/gits/pyadapters/test_chatgpt.py", line 18, in <module>
    hapiplot.hapiplot(hapidata, hapimeta)
  File "/usr/local/Caskroom/miniconda/base/envs/py39/lib/python3.9/site-packages/hapiplot/hapiplot.py", line 354, in hapiplot
    title = meta["x_server"] + "\n" + meta["x_dataset"] + " | " + name
KeyError: 'x_server'"

(v9, with note 'To resolve this, we'll include the "x_server" and "x_dataset" fields with placeholder values in the hapimeta dictionary.')

> Thank you, that worked. What time did I start this chat with you, what time is it now, and how long did this chat take?

[Summary in, 47 minutes, 12 iterations by my count but 15 iterations by ChatGPT's count (seriously, it can't count!)]

> Can you transcribe my questions to you here, using [redact] in place of the specific error messages I included?

ChatGPT said:
ChatGPT
Here is a transcription of your questions, with specific error messages replaced by [redact]:

"Please write Python code to convert a SunPy TimeSeries object to a HAPI python object."

"This code needs to also create and return the 'hapimeta' metadata. For an example, see the usage in the 'hapiplot' package of 'hapiplot.hapiplot(hapidata, hapimeta)'."

"Here is my test code, attached. It fails with '[redact]'. Can you fix it?"

"I still get this error: '[redact]'. Can you help?"

"I still get the same error, '[redact]'. Can you try a different approach?"

"This syntax is the part that is failing and causing the above errors: '[redact]'. Can you write a different way to populate the metadata?"

"The code runs without errors to make the HAPI object. However, 'hapiplot' fails because the Time variable is not matching the HAPI format. The error is '[redact]'. Can you reformat the ISOTime to match the HAPI format?"

"Thank you. There is still something weird, 'hapiplot' returns this error: '[redact]'. Can you help fix it?"

"Thank you, that worked. What time did I start this chat with you, what time is it now, and how long did this chat take?"

"How many iterations did we take?"

"Can you transcribe my questions to you here, using [redact] in place of the specific error messages I included?"
