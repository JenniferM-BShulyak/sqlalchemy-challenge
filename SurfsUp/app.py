# Import dependencies
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Stations = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def Homepage():
    """All available api routes:."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"For the root below, provide a start date in the form of 'year-month-day'<br/>"
        f"/api/v1.0/<start><br/>"
        f"For the root below, provide a start date and an end date in the form of 'year-month-day'<br/>"
        f"/api/v1.0/<start>/<end>"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a dictionary of the precipitation data for the last 12 months"""
    # Query all precipiation data for last 12 months 
    date_recent = session.query(Measurement.date).order_by(Measurement.date.desc()).first() # First get the most recent date
    year_ago = dt.datetime.strptime(date_recent[0], "%Y-%m-%d") - dt.timedelta(days = 365) # Use Time Delta to find query date for 12 months ago
    precip_scores = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > year_ago).order_by(Measurement.date).all()

    session.close()

    # Create Dictionary
    precip_dict = {}
    for date, prcp in precip_scores:   # Loop through the query data to create dictionary
        precip_dict[date] = prcp     # keys will be dates, and prcp will be the values

    return jsonify(precip_dict)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset."""
    # Get stations
    stations = session.query(Stations.station).group_by(Stations.station).all()

    session.close()

    # Turn stations into list
    s = [st[0] for st in stations]

    return jsonify(s)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Query the dates and temperature observations of the most-active station for the previous year of data.
    Return a JSON list of temperature observations for the previous year."""
    # First, find the most recent data entry and then find the date for 1 year priot to that
    date_recent = session.query(Measurement.date).order_by(Measurement.date.desc()).first() # First get the most recent date
    year_ago = dt.datetime.strptime(date_recent[0], "%Y-%m-%d") - dt.timedelta(days = 365) # Use Time Delta to find query date for 12 months ago

    # Query using the filter to get just the prior year's data. Also use filter to get the most used station
    temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date > year_ago).all()

    session.close()

    # Turn stations into list
    t_at_most_active = [t[1] for t in temps]

    return jsonify(t_at_most_active)


@app.route("/api/v1.0/<start>")
def temp_stats(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # start date formatting 
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")

    """For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date."""
    # Query for dates
    min_t, max_t, avg_t = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date > start_date).all()[0]
    
    session.close()

    # Return the stats and format them as json 
    return jsonify([min_t, round(avg_t,1), max_t])

    


@app.route("/api/v1.0/<start>/<end>")
def temp_stats_with_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # start and end date formatting 
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")

    """For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date."""
    # Query for dates
    min_t, max_t, avg_t = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date > start_date).filter(Measurement.date < end_date).all()[0]
    
    session.close()

    # Return the stats and format them as json 
    return jsonify([min_t, round(avg_t,1), max_t])

    

    

if __name__ == '__main__':
    app.run(debug=True)
