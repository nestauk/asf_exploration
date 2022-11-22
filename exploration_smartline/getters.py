import pandas as pd

def get_property_data(id, format="long"):
    """Read in the sensor data file for a particular property.

    Args:
        id (str): 4-digit property ID.
        format (str, optional): Whether to return the data as-is with
        one row for each individual sensor measurement ("long")
        or processed to give one row for each datatime ("wide").
        Defaults to "long".

    Returns:
        pd.DataFrame: Property sensor data.
    """
    long_data = pd.read_csv(
        "inputs/smartline_data_request_0002/tbl" + str(id) + ".csv"
    )
    
    if format=="wide":
        wide_data = (
            long_data
            .assign(
                # some duplicate (sensor, datetime) pairs
                # todo: find out why
                # for now, add a count to avoid duplicate indices
                row = (
                    long_data
                    .groupby(['sensorName', 'Datetime'])
                    .cumcount()
                )
            ).pivot(
                index=["Datetime", "row"], 
                columns="sensorName",
                values="Value")
            )
        
        return wide_data
    else:
        return long_data