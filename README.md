# sqlalchemy-challenge Week 10

This repo contains climate_analysis.ipynb, app.py, and a resources folder containing hawaii_measurements.csv, hawaii_stations.csv, and the hawaii.sqlite.

---

# Part 1: Climate Analysis and Exploration: climate_analysis.ipynb



# Part 2: Design Your Climate App: app.py

SQLAlchemy was used to connect to the sqlite database. 

Automap_base() was used to reflect the tables into classes called Station and Measurement in order to perform the analyses. 

A SQLAlchemy session was created in order to link Python to the database.

## Precipiation Analysis

This analysis included:

    (1) Finding the most recent date in the dataset (8/23/2017).

    (2) Using the most recent date, the previous 12 months of precipitation data was retrieved by querying the 12 previous months of data.

    (3) The date and prcp values from their query were loaded into a dataframe with the index being set as the date. The dataframe was sorted by the date.

    (4) The data was plotted.

    (5) Summary statistics were produced. 

## Station Analysis

This analysis included:

    (1) A query to calculate the total number of stations in the dataset. 

    (2) A query to find the most active stations and the station id with the highest number of measurements. This station is: USC00519281

    (3) The lowest, highest, and average temperatures were found for the most active station. 

    (4) A query to retrieve the previous 12 months of temperature observation data for the most active station. 

    (5) A histogram of the temperature data for the most active station. 

# Part 2: Design your Climate App: app.py

A Flask API was designed based on the queries in Part 1. The Flask includes the following routes:

    (1) / for the homepage which included a list of the possible routes
    
    (2) /api/v1.0/precipitation which returns a JSON dictionary of the precipitation results.

    (3) /api/v1.0/stations which returns a JSON list of the stations of the dataset. 

    (4) /api/v1.0/tobs which returns a JSON list of the temperature observations of the most active station for the past 12 months.

    (5) /api/v1.0/<start> and /api/v1.0/<start>/<end> which return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range.