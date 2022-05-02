import re

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
    "TYPE_ACCELEROMETER": {"name": "acc_calib", "mapping": lambda x: (x[0], (x[2], x[3], x[4]))},
    "TYPE_MAGNETIC_FIELD": {"name": "mag_calib", "mapping": lambda x: (x[0], (x[2], x[3], x[4]))},
    "TYPE_GYROSCOPE": {"name": "gyro_calib", "mapping": lambda x: (x[0], (x[2], x[3], x[4]))},
    "TYPE_ROTATION_VECTOR": {"name": "rotation_vector", "mapping": lambda x: (x[0], (x[2], x[3], x[4]))},
    "TYPE_ACCELEROMETER_UNCALIBRATED": {"name":  "acc_uncalib", "mapping": lambda x: (x[0], (x[2], x[3], x[4]))},
    "TYPE_MAGNETIC_FIELD_UNCALIBRATED": {"name": "mag_uncalib", "mapping": lambda x: (x[0], (x[2], x[3], x[4]))},
    "TYPE_GYROSCOPE_UNCALIBRATED": {"name": "gyro_uncalib", "mapping": lambda x: (x[0], (x[2], x[3], x[4]))},
    "TYPE_WIFI": {"name": "wifi", "mapping": lambda x:  (x[0], (x[2], x[3], x[4]))},
    "TYPE_BEACON": {"name": "beacon", "mapping": lambda x: (x[0], ("_".join([x[2], x[3], x[4]]), x[6]))},
    "TYPE_WAYPOINT": {"name": "waypoint", "mapping": lambda x: (x[0],  (x[2], x[3]))}
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
