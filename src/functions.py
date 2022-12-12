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

client = MongoClient("localhost:27017")
db = client['Ironhack']
c = db.get_collection('Companies')

#---------------------------------------------------------------------------------------------------------------------------------------------

#Cleaning for businesses that raised more than 1M funding 
def cleaning_for_funding_raised():
    filter_ = {"$and":
             [{'offices': {'$exists': 1}},
             {'total_money_raised' : {'$regex' : '[$€].*[MB]'}}]}
    projection = {'name':1, '_id':0, 'total_money_raised':1, 'offices.country_code': 1, "offices.state_code":1,'offices.city':1,'offices.latitude':1,'offices.longitude':1}
    list_ = list(c.find(filter_, projection).sort('offices.country_code'))[20:]

    df = pd.DataFrame(list_).explode("offices").reset_index(drop=True)
    df = pd.concat([df, df["offices"].apply(pd.Series)], axis=1).reset_index(drop=True)
    df.dropna(subset=["latitude"],inplace=True)
    df.dropna(subset=["city"],inplace=True)
    df.drop(columns= 'offices', inplace=True)
    df.drop(columns= 0, inplace=True)
    return df

#---------------------------------------------------------------------------------------------------------------------------------------------

#Cleaning for videogames companies
def cleaning_for_videogames_companies(): 
    filter_2 = {"$and": 
             [{"category_code":"games_video"},
             {'offices': {'$exists': 1}}]}
    projection_2 = {'name':1, '_id':0, 'category_code':1, 'offices.country_code': 1, "offices.state_code":1,'offices.city':1, 'offices.latitude':1,'offices.longitude':1}
    list_2 = list(c.find(filter_2, projection_2).sort('offices.country_code'))[20:]

    df_2 = pd.DataFrame(list_2).explode("offices").reset_index(drop=True)
    df_2 = pd.concat([df_2, df_2["offices"].apply(pd.Series)], axis=1).reset_index(drop=True)
    df_2.drop(columns= 'offices', inplace=True)
    df_2.dropna(subset=["city"],inplace=True)
    df_2.dropna(subset=["latitude"],inplace=True)
    df_2.drop(columns= 0, inplace=True)
    df_2 = df_2[df_2['city']!='']
    return df_2

#---------------------------------------------------------------------------------------------------------------------------------------------

#Cleaning for design companies
def cleaning_for_design_companies():
    filter_3 = {"$and": 
             [{"tag_list": {'$regex': "design"}},
             {'offices': {'$exists': 1}}]}
    projection_3 = {'name':1, '_id':0, 'tag_list':1, 'offices.country_code': 1, "offices.state_code":1,'offices.city':1, 'offices.latitude':1,'offices.longitude':1}
    list_3 = list(c.find(filter_3, projection_3).sort('offices.country_code'))

    df_3 = pd.DataFrame(list_3).explode("offices").reset_index(drop=True)
    df_3 = pd.concat([df_3, df_3["offices"].apply(pd.Series)], axis=1).reset_index(drop=True)
    df_3.drop(columns= 'offices', inplace=True)
    df_3.dropna(subset=["city"],inplace=True)
    df_3.dropna(subset=["latitude"],inplace=True)
    df_3.drop(columns= 0, inplace=True)
    df_3 = df_3[df_3['city']!='']
    return df_3

#---------------------------------------------------------------------------------------------------------------------------------------------
o = db.get_collection('Offices')

# Get the total offices dataframe
def total_offices_worldwide():
    total_offices_worldwide = pd.DataFrame(list(o.find()))
    total_offices_worldwide = total_offices_worldwide[['name', 'offices', 'geojson']]
    total_offices_worldwide = pd.concat([total_offices_worldwide, total_offices_worldwide['offices'].apply(pd.Series)], axis=1).reset_index(drop=True)
    total_offices_worldwide = total_offices_worldwide[['name', 'city', 'longitude', 'latitude']]
    return total_offices_worldwide

#---------------------------------------------------------------------------------------------------------------------------------------------

def creating_groups():
    # create a feature group for every San Fran Company in the dataset
    sf_offices_group = folium.FeatureGroup(name= 'SanFran Offices')
    # adding heatmap to feature group
    HeatMap(data = total_offices_SF[['latitude', 'longitude']], radius=10, gradient={0.0: 'pink', 0.3: 'blue', 0.5: 'green',  0.7: 'yellow', 1.0: 'red'}).add_to(sf_offices_group)
    # add heatmap and feature group to SF map created before
    sf_offices_group.add_to(san_fran_map)

    # create a feature group for Companies that raised +1M
    df_group = folium.FeatureGroup(name= 'SanFran Companies that raised +1M')
    # adding heatmap to feature group
    HeatMap(data = df_SF[['latitude', 'longitude']], radius=10, gradient={'0':'Navy', '0.25':'Blue','0.5':'Green', '0.75':'Yellow','1': 'Red'}).add_to(df_group)
    # add heatmap and feature group to SF map created before
    df_group.add_to(san_fran_map)
    
    # create a feature group for Video Games companies
    df_2_group = folium.FeatureGroup(name= 'SanFran Video Games Companies')
    HeatMap(data = df_2_SF[['latitude', 'longitude']], radius=15, gradient = {0.4: 'yellow', 0.65: 'orange', 1: 'red'}).add_to(df_2_group)
    df_2_group.add_to(san_fran_map)

    # create a feature group for Design companies
    df_3_group = folium.FeatureGroup(name= 'SanFran Design Companies')
    HeatMap(data = df_3_SF[['latitude', 'longitude']], radius=15, gradient = {0.4: 'gray', 0.65: 'black', 1: 'white'}).add_to(df_3_group)
    df_3_group.add_to(san_fran_map)

    return folium.LayerControl(collapsed=False, position="topleft").add_to(san_fran_map)


#---------------------------------------------------------------------------------------------------------------------------------------------
# This function gets a query, the latitude and longitude from the API and returns a list with the distance from the point.
# Limit 1 to get the nearest place defined in the query

token_fsq = os.getenv("token_foursquare")

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
