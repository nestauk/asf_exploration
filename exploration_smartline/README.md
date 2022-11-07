# Instructions

- Download the data from Google Drive: A Sustainable Future > 1. Reducing household emissions > 2. Projects/Research Work > 9. Boiler Optimisation > 00.Phase 3 > Smartline Coastline Housing
- Place in `/inputs` and unzip

# Data notes

## Tables and features
- `properties.csv`: information about the monitored properties. Features:
  - `IntID`: ID for the property.
  - `Accommodation_Type`: Type of property.
  - `Bedrooms`: Number of bedrooms.
- `tbl####.csv`: hourly sensor readings for property with ID `####` (IDs less than 1000 are displayed with leading zeroes). Long format, i.e. one row for each sensor reading. Features:
  - `PropertyReference`: Property ID. Same as `IntID` in `properties.csv`.
  - `sensorName`: Name of sensor taking measurement.
  - `Datetime`: Date and time of measurement.
  - `Value`: Value of measurement.
  - `PCF`: Pulse Conversion Factor. Used to multiply the difference between meter readings to give the usage.
  - `Unit`: Unit of measurement (e.g. °C, kWh).

## Quirks and observations
- There are duplicate records for some sensors and datetimes (see e.g. property `0109`, `Front Room - Temperature` sensor, datetime `2020-10-01 19:58:00.0000000`)