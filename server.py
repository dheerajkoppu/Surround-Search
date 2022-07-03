# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 14:37:00 2022

@author: Dheeraj Koppu
"""

# Loading Libraries
import googlemaps
import pandas as pd
import requests
from dis import dis
from flask import Flask, request, render_template, flash
import warnings
warnings.filterwarnings("ignore")
############################# Backend Methods #############################
# Method for finding the Geolocation Coordinates
def get_geo_coord(address):
     params = {
         'key': API_KEY,
         'address': address.replace(' ', '+')
     }
     base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
     response = requests.get(base_url, params=params)
     data = response.json()
     if data['status'] == 'OK':
         result = data['results'][0]
         location = result['geometry']['location']
         return location['lat'], location['lng']
     else:
         return

# Main method returns the locations list
# If there are no locations available its returns list of zeros
def surround_search():
    attributes = details
    key_word = attributes[0]
    location_rating = int(attributes[1])
    price_level = int(attributes[2])
    distance = float(attributes[3])
    distance *= 1609.344
    currently_open = int(attributes[4])
    if currently_open == 0:
      currently_open = True
    else:
      currently_open = False    
    # Getting User Location and conveting it into data needed for Google Maps link
    loc = str(attributes[5])
    user_loc = loc.replace(" ", "+") 
    cur_user_loc = loc.replace(",", "%2C") 
    gmaps = googlemaps.Client(key = API_KEY)
    # Do a simple nearby search where we specify the location
    # in lat/lon format, along with a radius measured in meters
    places_result  = gmaps.places_nearby(location = get_geo_coord(loc), radius = distance, open_now = currently_open , type = key_word) 
    avail_loc = places_result['results']
    locs = pd.DataFrame(columns=['Location','Address','Time to Reach','Distance to Cover', 'Directions'])

    if len(avail_loc)!=0:
        df = pd.DataFrame(avail_loc) 
        needed = ['geometry','name','opening_hours','place_id','rating','types','user_ratings_total','vicinity']
        
        if 'price_level' in df.columns:
            needed.append('price_level')
        
        df = df[needed]
    
        df = df.dropna() # removing rows with NAN values
        ## Checking for conditions
    
        for i in range(location_rating):
            df = df[df['rating'] != i]
        
        if 'price_level' in df.columns:
            df = df[df['price_level'] <= price_level]
            
            
        if len(df)!=0: # Condition to check if any locations are available
            df = df.reset_index(drop=True)
            names = df['name']
            placeid = df['place_id']
            address = df['vicinity']
            
            url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&'
            for i in range(0,len(df)):          
                   x = names[i]
                   y = address[i]
                   current_coord = get_geo_coord(address[i])
                   current_place = placeid[i]
                   # Used for showing directions to the location
                   link = 'https://www.google.com/maps/dir/?api=1&origin='+ cur_user_loc + '&destination=QVB&destination_place_id=' +current_place + '&travelmode=driving'
                    # '#' is creating problem in google api 
                   if '#' in address[i]:
                       address[i] = address[i].replace('#','')
                   
                   r = requests.get(url + "origins="  + loc + "&destinations=" + address[i] + "&key=" + API_KEY)
                   time_to_reach = r.json()["rows"][0]['elements'][0]['duration']['text']
                   dist = r.json()["rows"][0]['elements'][0]['distance']['text']
                   
                   locs.loc[len(locs)] = [x, y, time_to_reach, dist, link]
    
        else:
            locs.loc[0] = [None,None,None,None, None] # No location is available
    
    else:
        locs.loc[0] = [None,None,None,None, None] # No location is available
        
    if locs['Location'].isnull().sum()==0:
        locs = locs.reset_index(drop=True)
    locs = locs[:5]
    return locs


# Initializing with global variables
global attraction
global loc
global locs

details = list()
# Flask constructor
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
loc = ''
locs = []
attraction = ''
API_KEY = 'AIzaSyBxhrVX-8Pprg0g7JvxeCjUCV5QxaPhGu0'
# A decorator used to tell the application
# Which URL is associated function

# Gets users inputs from HTML File
@app.route('/', methods =["GET", "POST"])
def gfg():
    global details 
    if request.method == "POST":
      # Getting inputs
        key_word = request.form.get("search_keyword")  
        rating = request.form.get("search_ratings")
        price_level = request.form.get("price_level")
        distance = request.form.get("distance")
        currently_open = request.form.get("currently_open")
        loc = request.form.get("city")
        # Putting inputs into a list
        details = [key_word, rating, price_level, distance, currently_open, loc]
        locs = surround_search()
        # Rendering it into the html
        return render_template("output.html",tables=[locs.to_html(index = False, render_links=True, classes='data', justify='center')], titles="")
    return render_template("index.html")

# If its run and not imported, run
if __name__=='__main__':
    app.run(debug =True)