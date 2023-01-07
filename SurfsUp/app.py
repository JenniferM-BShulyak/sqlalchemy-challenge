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
engine = create_engine("sqlite:///.../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.Station

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
        f"/api/v1.0/<start><br/>"
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
    for date, prcp in precip_scores:
        precip_dict[date] = prcp

    return jsonify(precip_dict)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset."""
    # Get stations
    stations = session.query(Station.station).group_by(Station.station).all()

    session.close()

    # Turn stations into list
    s = [st[0] for st in stations]

    return jsonify(s)


if __name__ == '__main__':
    app.run(debug=True)
