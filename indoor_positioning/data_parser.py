import glob
import re
import numpy as np
import json

from pathlib import Path
from dataclasses import dataclass
from trace import Trace
from typing import NewType
from unicodedata import name


# Alias types

SSID = NewType("ssid", str)
BSSID = NewType("bssid", str)
UUID = NewType("uuid", str)
RSSI = NewType("rssi", int)
Tss = NewType("tss", int)
Distance = NewType("distance", float)
Freq = NewType("freq", int)
XYZ = tuple[float, float, float]
SensorsXYZ = list[tuple[Tss, XYZ]]
WifiData = list[tuple[Tss, tuple[SSID, BSSID, RSSI]]]
BeaconData = list[tuple[Tss, tuple[UUID, RSSI]]]
WaypointData = list[tuple[Tss, tuple[Distance, Distance]]]

# Tracing file's Metadata

METADATA_NAMES = {
    "startTime": "start_time",
    "SiteID": "site_id",
    "SiteName": "site_name",
    "FloorId": "floor_id",
    "FloorName": "floor_name",
}

# Admisible sensor types and their mapping functions for the tracing files
# The lambda function is used as a replacement for the case function

SENSOR_TYPES = {
    "TYPE_ACCELEROMETER": {"name": "acc_calib", "mapping": lambda x: (x[0], (x[2], x[3], x[4].replace("\n", "")))},
    "TYPE_MAGNETIC_FIELD": {"name": "mag_calib", "mapping": lambda x: (x[0], (x[2], x[3], x[4].replace("\n", "")))},
    "TYPE_GYROSCOPE": {"name": "gyro_calib", "mapping": lambda x: (x[0], (x[2], x[3], x[4].replace("\n", "")))},
    "TYPE_ROTATION_VECTOR": {"name": "rotation_vector", "mapping": lambda x: (x[0], (x[2], x[3], x[4].replace("\n", "")))},
    "TYPE_ACCELEROMETER_UNCALIBRATED": {"name":  "acc_uncalib", "mapping": lambda x: (x[0], (x[2], x[3], x[4]))},
    "TYPE_MAGNETIC_FIELD_UNCALIBRATED": {"name": "mag_uncalib", "mapping": lambda x: (x[0], (x[2], x[3], x[4]))},
    "TYPE_GYROSCOPE_UNCALIBRATED": {"name": "gyro_uncalib", "mapping": lambda x: (x[0], (x[2], x[3], x[4]))},
    "TYPE_WIFI": {"name": "wifi", "mapping": lambda x:  (x[0], (x[2], x[3], x[4]))},
    "TYPE_BEACON": {"name": "beacon", "mapping": lambda x: (x[0], ("_".join([x[2], x[3], x[4]]), x[6]))},
    "TYPE_WAYPOINT": {"name": "waypoint", "mapping": lambda x: (x[0],  (x[2], x[3].replace("\n", "")))}
}


@dataclass
class TraceData:
    """Class used for keeping the data logged in each of the .txt trace files"""

    file_name: str
    start_time: int
    site_id:  str
    site_name: str
    floor_id: str
    floor_name: str
    acc_calib: SensorsXYZ
    acc_uncalib: SensorsXYZ
    mag_calib: SensorsXYZ
    mag_uncalib: SensorsXYZ
    gyro_calib: SensorsXYZ
    gyro_uncalib: SensorsXYZ
    rotation_vector: SensorsXYZ
    wifi: WifiData
    beacon: BeaconData
    # TODO: CHECK WHETER THERE IS WAYPOINT DATA TO SEE IF IT IS A TRAINING OR TESTING TRACE FILE
    waypoint: WaypointData


def tracing_parser(trace_filename: str) -> TraceData:
    """
    Parser for the tracing files which keep all the sensor data

    Args:
        trace_filename (str): Tracing file recorded for the XYZ2020 competition

    Returns:
        TraceData: DataClass used for keeping the information associated to the tracing files
    """

    trace_data_kwargs = {
        "file_name": trace_filename,
        "acc_calib": [],
        "acc_uncalib": [],
        "mag_calib": [],
        "mag_uncalib": [],
        "gyro_calib": [],
        "gyro_uncalib": [],
        "rotation_vector": [],
        "wifi": [],
        "beacon": [],
        "waypoint": []
    }

    with open(trace_filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:

        if line.startswith("#"):
            for subsection in line.split("\t"):
                if subsection.startswith(tuple(METADATA_NAMES.keys())):
                    split_sub = subsection.split(":")
                    trace_data_kwargs[METADATA_NAMES[split_sub[0]]
                                      ] = split_sub[1].replace("\n", "")

        else:
            split_line = line.split("\t")
            sensor_name = SENSOR_TYPES[split_line[1]]["name"]
            sensor_values = SENSOR_TYPES[split_line[1]]["mapping"](
                split_line
            )
            # Appends the data associated to each of the sensors
            trace_data_kwargs[sensor_name].append(sensor_values)

    return TraceData(**trace_data_kwargs)


def waypoint_list(map_folder):
    """From the dir of a map folder, returns a list of all the waypoints in said map

    Args:
        map_folder (str): DIR of the map

    Returns:
        list(float, float): List of the waypoint pairs in the map
    """
    tracefiles = glob.glob(map_folder + "/*.txt", recursive=True)
    waypoints = []
    for file in tracefiles:
        print("Parsing {}".format(file))
        parsed = tracing_parser(file)
        waypoints += [[xyz[1][0], xyz[1][1]] for xyz in parsed.waypoint]

    map_waypoints = np.unique(np.array(waypoints, dtype="float32"), axis=0)
    return map_waypoints


def floorplan(metadata_path, floor_folder_dir):
    floorplan = {}
    floorplan_dir = metadata_path + "/".join(Path(floor_folder_dir).parts[1:])
    floorplan_info = floorplan_dir + "/floor_info.json"
    floorplan_image = floorplan_dir + "/floor_image.png"
    with open(floorplan_info) as f:
        floor_info = json.load(f)
    width_meter = floor_info["map_info"]["width"]
    height_meter = floor_info["map_info"]["height"]
    floorplan["width"] = width_meter
    floorplan["height"] = height_meter
    floorplan["floor_image"] = floorplan_image
    return floorplan
