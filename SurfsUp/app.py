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
    )

# Define first route
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

##########################################
# Debug Conditions
##########################################
# Define when to use debugger
if __name__ == "__main__":
    app.run(debug=True)

