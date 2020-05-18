## Climate App

# import dependencies
%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# create database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return(
        f"Let the Hawaii Clmate Analysis API begin!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation<br/>")
def precipitation():
    """Precipitation Obeserved in the Past Year"""
    # Query for the dates and precipitation observations from the last year
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Convert the query results to a Dictionary using `date` as the key and `prcp` as the value
    prcp = session.query(measurement.date, func.avg(measurement.prcp)).filter(measurement.date>=year_ago).group_by(measurement.date.desc()).all()
    
    # Return the JSON representation of your dictionary
    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def stations():
    """Stations Observed in Study"""
    # Return a JSON list of stations from the dataset
    station_set = session.query(station.station, station.name).all()
    return jsonify(station_set)

@app.route("/api/v1.0/tobs")
def tobs():
    """Temperatures Observed in the Past Year"""
    # Query the dates and temperature observations of the most active station for the last year of data
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date>=year_ago, measurement.station == "USC00519281").order_by(measurement.date.desc()).all()
    
    # Return a JSON list of temperature observations (TOBS) for the previous year
    return jsonify(tobs)

# Given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
@app.route("/api/v1.0/<start>")
def start(start):
    # Pull last date of observation from step 1 and calculate start date and format
    start_date = dt.datetime.strptime(start, %Y-%m-%d)
    prior_date = dt.timedelta(days=365)
    start = start_date-prior_date
    end = dt.date(2017, 8, 23)
    
    # calculate TMIN, TAVG, and TMAX for all dates within the specified year and return JSON
    start_calc = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    calc = list(np.ravel(start_calc))
    return jsonify(calc)

# Given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive 
@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
    # set start and end dates and format them
    start_date = dt.datetime.strptime(start, %Y-%m-%d)
    end_date = dt.datetime.strptime(end, %Y-%m-%d)
    observation = dt.timedelta(days=365)
    start = start_date-observation
    end = end_date-observation
    
    # calculate TMIN, TAVG, and TMAX for all dates within the specified year and return JSON
    end_calc = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    done = list(np.ravel(end_calc))
    return jsonify(done)

if __name__ == "__main__":
    app.run(debug=True)