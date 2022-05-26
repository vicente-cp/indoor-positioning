import copy
from shapely.geometry import shape, GeometryCollection
from shapely.geometry import Point
from shapely.affinity import affine_transform
import numpy as np
import json


def extract_geometries(geojson_dir):
    """Converts the geojson data to a shapely 

    Args:
        geojson_dir (str): Dir of the geojson file

    Returns:
        MultiPolygon: Shapely MultiPolygon of the respective floor geometry
    """

    with open(geojson_dir) as f:
        geojson = json.load(f)

    # Extract floor plan geometry (First geometry)
    floor = copy.deepcopy(geojson)
    floor['features'] = [floor['features'][0]]
    floor_layout = GeometryCollection([shape(feature["geometry"]).buffer(
        0) for feature in floor['features']])[0]

    # Extract shops geometry (remaining ones)
    shops = copy.deepcopy(geojson)
    shops['features'] = shops['features'][1:]
    shops_geometry = GeometryCollection([shape(
        feature["geometry"]).buffer(0.1) for feature in shops['features']])

    # Geometry differences to get corridor (floor layout - shops)
    corridor = copy.deepcopy(floor_layout)
    for shop in shops_geometry:
        corridor = corridor.difference(shop)

    return floor_layout.difference(corridor)


def transform(geom, floorplan):
    """Correctly scales and offsets the geojson shapely object using the width and height given in the floor_info 

    Args:
        geom (Shapely obj): shapely object associated to the flo
        floorplan (dict): Dict of the floorplan, which incorporates both the real width and height of the floor layout

    Returns:
        MultiPolygon: shapely object of the correctly scaled and offset floor layout
    """
    bord = geom.bounds
    real_width = floorplan["width"]
    real_height = floorplan["height"]
    x_scaling = real_width/(bord[2]-bord[0])
    y_scaling = real_height/(bord[3]-bord[1])
    affine_geom = affine_transform(
        geom, [x_scaling, 0, 0, y_scaling, -bord[0] * x_scaling, -bord[1] * y_scaling])
    return affine_geom
