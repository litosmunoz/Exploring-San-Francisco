import os
import requests
import json
from dotenv import load_dotenv
import pandas as pd
from pandas import json_normalize
from pymongo import MongoClient
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster
from cartoframes.viz import Map as Map2, Layer, popup_element

#---------------------------------------------------------------------------------------------------------------------------------------------

# This function gets a query, the latitude and longitude from the API and returns a list with the distance from the point.
# Limit 1 to get the nearest place defined in the query
def foursquare_query (query, lat, lon):

    url = f"https://api.foursquare.com/v3/places/search?query={query}&ll={lat}%2C{lon}&limit=1"

    headers = {"accept": "application/json", "Authorization": token_fsq}
    response = requests.get(url, headers=headers).json()

    list = []
    for i in response["results"]:
        distance = i["distance"]

        list.append(distance)
    
    return list

#--------------------------------------------------------------------------------------------------------------------------------------------

#This function gets a category, the latitude and longitude from the API and returns a list with the distance from the point.
#Limit 1 to get the nearest place defined by category
def foursquare_cat (category, lat, lon):

    url = f"https://api.foursquare.com/v3/places/search?ll={lat}%2C{lon}&categories={category}&limit=1"

    headers = {"accept": "application/json", "Authorization": token_fsq}
    response = requests.get(url, headers=headers).json()

    list = []
    for i in response["results"]:
        distance = i["distance"]

        list.append(distance)
    
    return list
