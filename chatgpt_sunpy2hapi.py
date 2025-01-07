from sunpy.timeseries import TimeSeries
import numpy as np

def convert_timeseries_to_hapi(ts: TimeSeries):
    """
    Converts a SunPy TimeSeries object to HAPI-compatible data and metadata.
    
    Parameters:
        ts (TimeSeries): The SunPy TimeSeries object to convert.
    
    Returns:
        tuple: A tuple containing:
            - hapidata (np.ndarray): A HAPI-compatible named NumPy array.
            - hapimeta (dict): HAPI-compatible metadata.
    """
    # Use .time to get an astropy.time.Time object
    times = ts.time  # Get astropy.time.Time object
    hapi_times = times.strftime("%Y-%m-%dT%H:%M:%S.%f")  # Format as HAPI-compliant ISO 8601

    # Extract data as a DataFrame
    data = ts.to_dataframe()

    # Define structured NumPy array
    dtypes = [('Time', 'U26')]  # ISO 8601 time string
    dtypes += [(col, data[col].dtype) for col in data.columns]
    hapidata = np.zeros(len(hapi_times), dtype=dtypes)

    # Populate structured array
    hapidata['Time'] = hapi_times
    for col in data.columns:
        hapidata[col] = data[col].values

    # Create HAPI metadata
    hapimeta = {
        "HAPI": "3.0",
        "status": {
            "code": 1200,
            "message": "OK"
        },
        "x_server": "Sample Server",  # Placeholder value for server name
        "x_dataset": "Sample Dataset",  # Placeholder value for dataset name
        "parameters": [
            {
                "name": "Time",
                "type": "string",
                "units": "UTC",
                "length": 26
            }
        ]
    }

    # Populate metadata for data columns
    for col in data.columns:
        parameter_meta = {
            "name": col,
            "type": "double" if data[col].dtype.kind in "fc" else "integer",
            "units": "unknown",  # Units are descriptive; set to "unknown"
            "description": col   # Use column name as a fallback description
        }
        hapimeta["parameters"].append(parameter_meta)

    return hapidata, hapimeta
