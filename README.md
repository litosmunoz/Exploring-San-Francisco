# Project-3  GeoSpatial Data 
## Ironhack Data Analytics Bootcamp 

### Exploring San Francisco!!!

### Introduction: 
For the third weekly project in the data bootcamp, we have to identify the ideal location for the office of a new company, given certain conditions (eg. 30% of the company staff have at least 1 child). Using a database with over 18.000 companies and the foursquare API to access information for different venues, the objective is to find a location that works for as many employees as possible. 

### Conditions:
- Designers like to go to design talks and share knowledge.
- There must be some nearby companies that also do design.
- 30% of the company staff have at least 1 child.
- Developers like to be near successful tech startups that have raised at least 1 Million dollars.
- Executives like Starbucks A LOT. Ensure there's a starbucks not too far.
- Account managers need to travel a lot.
- Everyone in the company is between 25 and 40, give them some place to go party.
- The CEO is vegan.
- If you want to make the maintenance guy happy, a basketball stadium must be around 10 Km.
- The office dog—"Dobby" needs a hairdresser every month. Ensure there's one not too far away.

### Work done:
First I filtered within the companies collection for start ups that had raised more than 1 Million (dollars or euros), for videogame companies and for design companies. I realized that San Francisco was the city in which more startups had raised over 1M, and one of the cities with more video games companies and design companies (based on the database I was given). Therefore I decided to focus only in San Francisco. 

Then I plotted a heatmap with different layers. 
Layer 1 -Took into account every company in San Francisco
Layer 2 - Took into account each start up that raised more than 1M
Layer 3 - Took into account every video game company
Layer 4 - Took into account every design company

<img src="maps/Heatmap (only offices).png" width="1840" height="700">
<img src="maps/Heatmap (offices and startups that raised +1M).png" width="1840" height="700">
<img src="maps/Heatmap (offices, startups that raised +1M and Video Games Companies).png" width="1840" height="700">
<img src="maps/Heatmap (offices, startups that raised +1M, Video Games Companies and Design Companies).png" width="1840" height="700">

#
**Then I chose 6 points that seemed interesting.**

<img src="maps/Heatmap with Markers.png" width="1840" height="700">
 
Moreover, I used the foursquare API to find the distance from the different places (conditions) and created a new dataframe. 

<img src="maps/Key Locations (without scores).png" width="5000" height="200">
#
I am going to use a weighted average to calculate the overall score of each location given the distance to each variable.

### Leisure (30%)
    #Starbucks = 0.15
    #Night Clubs = 0.10
    #Vegan Rest = 0.05

### Kids (25%)
    #Parks = 0.125
    #School = 0.125

### Travel (40%)
    #Airport = 0.25
    #Rail Station = 0.075
    #Port = 0.075

### Others (5%)
    #Basketball St = 0.02
    #Dog Salon = 0.03

#
Calculate the score for each location by doing the sum of: 
((100/distance)*weight)*100 for each variable.

<img src="maps/Key Locations DataFrame.png" width="5000" height="200">

#
Finally I created a GeoDataframe and plotted the location points with their respective scores.

<img src="maps/Map with Scores.png" width="1500" height="500">

### Deliverables:
There is one main deliverable, a jupyter notebook where I have done my search and ended up with a selected location for the new office. I have saved the main dataframe with the conditions and the corresponding scores per location. As well, I have saved some maps that show visually where are the main zones of interest. 

### Author:
Carlos Muñoz Fresco