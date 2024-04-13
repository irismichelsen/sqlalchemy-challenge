# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# Create our session (link) from Python to the DB
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement


#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Create a menu/instructions for finding different webpages
@app.route("/")
def welcome():
    """List all available api routes"""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date (YYYY-MM-DD)<br/>"
        f"/api/v1.0/start_date/end_date (YYYY-MM-DD/YYYY-MM-DD)<br/>"
    )

# Define first route "Precipitation"
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """ Return a list of all the precipitation dates for the last year """
    # Query precipitation data
    # Get all the results from the past year
    sel = [Measurement.date, Measurement.prcp]
    results = session.query(*sel).\
        filter(Measurement.date > dt.datetime(2016,8,22)).\
        order_by(Measurement.date).all()

    # Close the session
    session.close()

    # Convert the results into a dictionary
    all_precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_precip.append(precip_dict)

    return jsonify(all_precip)

# Define second route "Stations"
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """ Return a list of all the stations """
    # Query station data
    results = session.query(Station.name, Station.station).all()
#    results = session.query(Station.station).all()

    # clean up
    session.close()

    # Convert results into a dictionary
    all_stations = []
    for name, station in results:
        station_dict = {}
        station_dict["name"] = name
        station_dict["station"] = station
        all_stations.append(station_dict)

    # Convert list of tuples into normal list
#    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

# Define the third route "tobs" - times of observation
@app.route("/api/v1.0/tobs")

def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    print("something")

    """ Return a list of all the precipitation dates for the last year """
    # Query precipitation data
    # Get all the results from the last year
    sel=[Measurement.date, Measurement.tobs]
    results = session.query(*sel).\
        filter(Measurement.date > dt.datetime(2016,8,22)).\
        filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.date).all()

    # Close session
    session.close()

    # Convert results into a dictionary
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

# Create two more routes with adjustable start/end dates (part 1)
@app.route("/api/v1.0/<start_date_str>")
def data_start_date(start_date_str):
    """ For a specified start, calculate TMIN, TAVG, and TMAX 
    for all the dates greater than or equal to the start date. """   
   
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Get all the results from the last year
    sel=[Measurement.date,
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)]
    results = session.query(*sel).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_date_str).\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()

    # Close session
    session.close()

    # Get results into dictionary format for json
    all_tobs = []
    for date, min, avg, max in results:
        response_str = f"Date: {date} Min: {min:.2f} Avg: {avg:.2f} Max: {max:.2f}"
        tobs_dict = {}
        tobs_dict["response"] = response_str
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

# Create two more routes with adjustable start/end dates (part 2)
@app.route("/api/v1.0/<start_date_str>/<end_date_str>")
def data_startend_date(start_date_str, end_date_str):
    """ For a specified start, calculate TMIN, TAVG, and TMAX 
    for all the dates greater than or equal to the start date. """   
   
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # get all the results from the last year
    sel=[Measurement.date,
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)]
    results = session.query(*sel).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_date_str).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) <= end_date_str).\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()

    # clean up
    session.close()

    # Get results into dictionary format for json
    all_tobs = []
    for date, min, avg, max in results:
        response_str = f"Date: {date} Min: {min:.2f} Avg: {avg:.2f} Max: {max:.2f}"
        tobs_dict = {}
        tobs_dict["response"] = response_str
        all_tobs.append(tobs_dict)


    return jsonify(all_tobs)

##########################################
# Debug Conditions
##########################################
# Define when to use debugger
if __name__ == "__main__":
    app.run(debug=True)

