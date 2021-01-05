# import necessary libraries
#from app import db

#from models import create_classes
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
import pandas as pd
import numpy as np

import datetime as dt
from datetime import datetime
from dateutil.relativedelta import relativedelta

import json

#################################################
# Mac
#################################################
# Set Executable Path & Initialize Chrome Browser

#def init_browser():
    #executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    #return Browser("chrome", **executable_path, headless=False)

#################################################
# Windows
#################################################
# Set Executable Path & Initialize Chrome Browser

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

#################################################
# Database Setup
#################################################

#from flask_sqlalchemy import SQLAlchemy
import warnings
warnings.filterwarnings('ignore')

import os
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, load_only
from sqlalchemy import create_engine, func, inspect, distinct

# Imports the methods needed to abstract classes into tables
from sqlalchemy.ext.declarative import declarative_base

# Allow us to declare column types
from sqlalchemy import Column, Integer, String, Float

#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"

# Sets an object to utilize the default declarative base in SQL Alchemy
Base = declarative_base()

class us_election_results(Base):
    __tablename__ = 'us_election_results'
    id = Column(Float, primary_key=True)
    year = Column(Integer)
    state_name = Column(String(255))
    state_abbr = Column(String(255))
    combined_fips = Column(Integer)
    county_name = Column(String(255))
    county_fips = Column(Integer)
    votes_dem = Column(Integer)
    votes_gop = Column(Integer)
    total_votes = Column(Integer)
    diff = Column(Integer)
    per_dem = Column(Float)
    per_gop = Column(Float)
    per_point_diff = Column(Float)


# Create a Specific Instance of the Dog and Cat classes
# ----------------------------------

# Calls the Pet Constructors to create "Dog" and "Cat" objects
#dog = Dog(name='Rex', color='Brown', age=4)
#cat = Cat(name="Felix", color="Gray", age=7)

# Create Database Connection
# ----------------------------------
# Creates a connection to our DB
database_path = "db.sqlite"
engine = create_engine(f"sqlite:///{database_path}?check_same_thread=False")
conn = engine.connect()

# Remove tracking modifications
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a "Metadata" Layer That Abstracts our SQL Database

# Use this to clear out the db
# ----------------------------------
Base.metadata.drop_all(engine)

# ----------------------------------
# Create (if not already in existence) the tables associated with our classes.
Base.metadata.create_all(engine)

# Create a Session Object to Connect to DB
# ----------------------------------
# Session is a temporary binding to our DB
session = Session(bind=engine)

# Add Records to the Appropriate DB
# ----------------------------------
# Use the SQL ALchemy methods to run simple "INSERT" statements using the classes and objects  
#try:
#    session.add(dog)
#    session.add(cat)
#    session.commit()   
#except:
#    session.rollback()
#    raise
#finally:
    # Query the Tables
    # ----------------------------------
    # Perform a simple query of the database
#    dog_list = session.query(Dog)
#    for doggy in dog_list:
#        print(doggy.name)

#    cat_list = session.query(Cat)
    
#    for kitty in cat_list:
#        print(kitty.name)    
    
    #session.close()

# Create the inspector and connect it to the engine
inspector = inspect(engine)

# Collect the names of tables within the database
inspector.get_table_names()

# Display the column names of pets
columns = inspector.get_columns('us_election_results')
for column in columns:
    print(column["name"], column["type"])

# Use `engine.execute` to select and display the first 10 rows from the measurement table
engine.execute('SELECT * FROM us_election_results LIMIT 10').fetchall()

# Display the column names of measurement
# columns = inspector.get_columns('us_election_results')
# for column in columns:
#    print(column["name"], column["type"])

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
print(Base.classes.keys())

# Save reference to the table
#Pet = Base.classes.pets
UsElectionResult = Base.classes.us_election_results

# Create our session (link) from Python to the DB
#session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#db = SQLAlchemy(app)

#Pets = create_classes(session)

# create route that renders index.html template
@app.route("/")
def index():
    return render_template("index.html")

# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        name = request.form["petName"]
        lat = request.form["petLat"]
        lon = request.form["petLon"]

        pet = Pet(name=name, lat=lat, lon=lon)
        try:
            session.add(pet)
            session.commit()
        except:
            session.rollback()
            raise

        return redirect("/", code=302)

    return render_template("form.html")

@app.route("/api/pals")
def pals():
    results = session.query(Pet.name, Pet.lat, Pet.lon).all()

    hover_text = [result[0] for result in results]
    lat = [result[1] for result in results]
    lon = [result[2] for result in results]
    print(hover_text)
    pet_data = [{
        "type": "scattergeo",
        "locationmode": "USA-states",
        "lat": lat,
        "lon": lon,
        "text": hover_text,
        "hoverinfo": "text",
        "marker": {
            "size": 50,
            "line": {
                "color": "rgb(8,8,8)",
                "width": 1
            },
        }
    }]
    print(pet_data)
    return jsonify(pet_data)

if __name__ == "__main__":
    app.run(debug=True)
