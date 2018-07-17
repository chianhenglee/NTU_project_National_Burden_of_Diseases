"""
This is a rather ugly script trying to calculate the centroid of each polygon from the geojson files
of all the counties in Taiwan.

Input files are a txt file of the county names and the corresponding .json (geojson) files

It calculates a dictionary and then export the coordinates into a txt file
corresponds with the order of the .txt file of the county names.
"""

import json
import numpy as np


### Function to calculate the centroid of the polygons using an np array of [lon,lat]
def centroidnp(arr):
    length = arr.shape[0]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    return sum_x/length, sum_y/length



# Get counties name list
with open('counties/counties_list.txt') as f:
    Clist=f.read().splitlines()

# Construct dictionary and calculate center of counties lon lat
Dict_counties_centroid = {}
for c in Clist:
    with open('counties/'+c+'.json') as f:
        geojsonfile = json.load(f)

    coordinates_temp = geojsonfile['features'][0]['geometry']['coordinates']
    list_of_coordinates = np.array(sum(coordinates_temp,[]))

    # VERY ugly way to deal with nested list more than 2 layers deep
    while len(list_of_coordinates) < 9:
        # 9 is an arbitary number, assuming there should be more points
        # if we flatten the whole list properly
        print('Here')
        list_of_coordinates = np.array(sum(list_of_coordinates,[]))


    Dict_counties_centroid[c]=centroidnp(list_of_coordinates)



## Here export the coordinates into txt files
cc = list(Dict_counties_centroid.values())

with open('counties/counties_centroid.txt','w') as ff:
    for x,y in cc:
        ff.write('{},{}\n'.format(x,y))
