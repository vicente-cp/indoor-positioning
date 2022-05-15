import copy
from shapely.geometry import shape, GeometryCollection
from shapely.geometry import Point
import numpy as np
import json


def extract_geometries(geojson_dir):
    with open(geojson_dir) as f:
        geojson = json.load(f)

    # Extract floor plan geometry (First geometry)
    floor = copy.deepcopy(geojson)
    floor['features'] = [floor['features'][0]]
    floor_layout = GeometryCollection([shape(feature["geometry"]).buffer(0) for feature in floor['features']])[0]

    # Extract shops geometry (remaining ones)
    shops = copy.deepcopy(geojson)
    shops['features'] = shops['features'][1:]
    shops_geometry = GeometryCollection([shape(feature["geometry"]).buffer(0.1) for feature in shops['features']])

    # Geometry differences to get corridor (floor layout - shops)
    corridor = copy.deepcopy(floor_layout)
    for shop in shops_geometry:
        corridor = corridor.difference(shop)

    return floor_layout, corridor


def occupied_grid(floor_layout, corridor):
    return floor_layout.difference(corridor)
