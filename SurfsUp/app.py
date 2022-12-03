import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

###########  The following code is nearly identical to Day 3 Activity 10 
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
######  There are 2 tables in the db
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
###### Everything you need here can be found in Day 3 Activity 10
# Create route @ is whatever we called the application. #in paranthesis is whatever route this is. home is just slash. 
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
session.close()

###### the 'precipitation' route you will query and return the data Day 3 Activity 10
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last year"""
    # Calculate the date 1 year ago from last date in database
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    print(f"\n\n{year_ago}\n\n")
    # Query for the date and precipitation for the last year
    year_ago_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago).\
        order_by(Measurement.date).all()
    # Dict with date as the key and prcp as the value
    # dictionary = {Measurement.date:Measurement.prcp}
    dictionary_two = {}
    for key,value in year_ago_data:
        dictionary_two[key]=value
    print(dictionary_two)
    return jsonify (dictionary_two)   
session.close()

###### the 'stations' route you will query and return the data Day 3 Activity 10
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""
    # Unravel results into a 1D array and convert to a list -numpy
    station_results = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    session.close()
    station_dictionary = list(np.ravel(station_results))
    return jsonify (station_dictionary = station_dictionary)   
session.close()

###### the 'tobs' route you will query and return the data Day 3 Activity 10
@app.route("/api/v1.0/tobs")
def temp_monthly():
    """Return the temperature observations (tobs) for previous year."""
    # Calculate the date 1 year ago from last date in database
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    # Query the primary station for all tobs from the last year
    twelve_months_station = session.query(Measurement.tobs).\
                                filter(Measurement.station=='USC00519281').\
                                filter(Measurement.date >= year_ago).\
                                order_by(Measurement.date.desc()).all()
    # Unravel results into a 1D array and convert to a list
    twelve_months_station_unraveled = list(np.ravel(twelve_months_station))
    # Return the results
    return jsonify (twelve_months_station_unraveled=twelve_months_station_unraveled)
session.close()

###### the 'temp' route you will query the data with params in the url and return the data Day 3 Activity 10
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""

# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

    # Select statement - session query 
    # Calculate TMIN, TAVG, TMAX with start 
    measures_start = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date>= start).all() 

    measures_stop = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date>= start, Measurement.date<= end ).all() 

    # Unravel results into a 1D array and convert to a list
    measures_start_unraveled = list(np.ravel(measures_start))
    # Return the results
    return jsonify (measures_start_unraveled)

session.close()

#Just need this at the end of the page because we do
if __name__ == '__main__':
    app.run()
