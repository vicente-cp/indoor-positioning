# Indoor Positioning Solutions for real-time data
The purpose of this repository is to present an array of approaches to handle indoor positioning in the context of multi-type data. There are multiple visualization tools for both the dataset and filtered data.


# Dataset

For all related purposes, this project makes use of the  [Indoor Location & Navigation Research Prediction Competition](https://www.kaggle.com/competitions/indoor-location-navigation/overview) dataset.  Based on real-time sensor data, the dataset was generated using a sensor data recording app by the company XYZ10, in partnership with Microsoft Research.

 Although the original dataset has nearly 30.000 traces from over 200 buildings, only a portion of that information is used in this repository.

## Description

Quoting the data description in the XYZ10 2021 competition:


 > The dataset for this competition consists of dense indoor signatures of WiFi, geomagnetic field, iBeacons etc., as well as ground truth (waypoint) (locations) collected from hundreds of buildings in Chinese cities. The data found in path trace files (*.txt) corresponds to an indoor path between position p_1 and p_2 walked by a site-surveyor.

> During the walk, an Android smartphone is held flat in front of the surveyors body, and a sensor data recording app is running on the device to collect IMU (accelerometer, gyroscope) and geomagnetic field (magnetometer) readings, as well as WiFi and Bluetooth iBeacon scanning results. A detailed description of the format of trace file is shown, along with other details and processing scripts, at this github link. In addition to raw trace files, floor plan metadata (e.g., raster image, size, GeoJSON) are also included for each floor.

<!--
# Approaches

Everything is done using data fusion

## Fingerprinting

## SLAM

### SLAM 1

### SLAM 2



# Visualization

## Three.js

### Positioning

### Smartphone Orientation
-->


## Contents
```
indoor-location-competition-20
│   README.md
│   main.py                                                           //main function of the sample code
└───indoor_positioning                                 //main folder
 |     └───data_parser.py                                 // tracing files parser
 |     └───data_processing.py                        // mostly data filtering
 |     └───data_visualizer.py                            // visualization tools
 |     └───gridding                                              // map grid tools
 |
└───dataset                                                  //example raw data from one site
      └───site_id
      |     └───B1                                                 //traces from one floor
      |     |    └───path_data_files                             
      |     |    |          └───5dda14a2c5b77e0006b17533.txt     //trace file
      |     |    |          |   ...
      |     |    |
      |     |
      |    └───F1
      |    │   ...
      |
     └───metadata
           └───site_id                                                // site information
                 └───B1                             
                            └───floor_image.png             //raster floor plan
                            └───floor_info.json                 //floor size info
                            └───geojson_map.json         //floor plan in vector format (GeoJSON)

```
