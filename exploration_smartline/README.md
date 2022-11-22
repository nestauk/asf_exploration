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
- Some datetimes are missing altogether (e.g. property `0109`, datetime `2020-12-31 23:56:00.0000000`)
- Need to standardise `PCF` as some values have floating point issues (some values appearing as `0.000124` are actually `0.000124230728`, others are `0.0001242307279999`)
- Gas and water meter readings reset at `65000`

## Points for clarification
- Why the duplicates?
- Some measurements look very precise (e.g. first `Front Room - Temperature` observation in property `0109` is `23.4208`) - what is their actual precision?
- Seems to be a lot of missing data (looking at e.g. the 'wide' form of property `0109` data) - why is this? What are the actual frequencies of the individual sensors?
- What are the different categories for `Accomodation_Type` in `properties.csv`?
- Is `PCF` the same for each type of sensor? Is it independent of time and property?
- How to interpret `Value`/`PCF`/`Unit` - is it the case that `Value * PCF` is equal to the value in the units specified by `Unit`?