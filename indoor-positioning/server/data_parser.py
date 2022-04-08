from dataclasses import dataclass
from typing import NewType

# Alias types

BSSID = NewType("bssid", str)
UUID = NewType("uuid", str)
RSSI = NewType("rssi", int)
Tss = NewType("tss", int)
Distance = NewType("distance", float)
Freq = NewType("freq", int)
XYZ = tuple[float, float, float] # Used for sensors which contain XYZ data
SensorsXYZ = list[tuple[Tss, XYZ]] # Ex: bar = [(Tss(10010), (0.5, 0.67, 10.2)), ( Tss(10011), (0.52, 0.57, 19.16)), ... , (Tss(20012) ,(3.52, 1.2, 6.2)) ]
WifiData = list[tuple[Tss, tuple(RSSI, Freq)]]
BeaconData = list[tuple[Tss, tuple(RSSI,  Distance)]]


@dataclass
class TraceData:
    
    """Class used for keeping the data logged in each of the .txt trace files"""
    
    file_name: str
    start_time: int
    site_id:  str
    site_name: str
    floor_id: str
    foor_name: str
    acc_calib: SensorsXYZ
    acc_uncalib: SensorsXYZ
    mag_calib: SensorsXYZ
    mag_uncalib: SensorsXYZ
    gyro_calib: SensorsXYZ
    gyro_uncalib: SensorsXYZ
    rotation_vector: SensorsXYZ
    wifi: WifiData
    beacon: BeaconData
