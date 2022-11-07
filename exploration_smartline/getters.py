import pandas as pd

def get_property_data(id, format="long"):
    
    raw_property_data = pd.read_csv(
        "inputs/smartline_data_request_0002/tbl" + str(id) + ".csv"
    )
    
    if format=="wide":
        wide_data = (
            raw_property_data
            .assign(
                row = (
                    raw_property_data
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
        return raw_property_data