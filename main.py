from indoor_positioning import data_parser, visualizer, data_processing
from pathlib import Path

import glob

# Venue id can be any of the metadata 
venue_id = "5cd56b6ae2acfd2d33b59ccb"

DATASET_DIR = "./dataset"
VENUE_DIR = DATASET_DIR + "/" + venue_id + "/"
METADATA_DIR = "./dataset/metadata/"
OUTPUT_DIR = './output/'
TSS_HISTOGRAMS_DIR = OUTPUT_DIR + "tss_hist/"

if __name__ == "__main__":
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    Path(TSS_HISTOGRAMS_DIR).mkdir(parents=True, exist_ok=True)
    Path(TSS_HISTOGRAMS_DIR + venue_id).mkdir(parents=True, exist_ok=True)

    # Specific tracing file selection

    tracing_files = glob.glob(VENUE_DIR + "**/*.txt", recursive=True)
    tracing_test_filename = tracing_files[0]
    tracing_test_id = Path(tracing_test_filename).parts[-1].replace(".txt","")
    parsed_data = data_parser.tracing_parser(tracing_test_filename)
    
    # Floor data

    floor_folder_dir = str(Path(tracing_test_filename).parent)
    # waypoint_list = data_parser.waypoint_list(floor_folder_dir)
    floorplan = data_parser.floorplan(METADATA_DIR, floor_folder_dir)



    "1.1 -- Visualizing tss difference"
    sensors_to_viz = {
        "Calibrated Acce": parsed_data.acc_calib,
        "Calibrated Magnetometer": parsed_data.mag_calib,
        "Calibrated Gyro": parsed_data.gyro_calib}

    histogram_figs = []
    for sensor in sensors_to_viz:
        tss = [xyz[0] for xyz in sensors_to_viz[sensor]]
        histogram_figs.append(visualizer.viz_histogram_tss_diff(tss))

    html_filename = TSS_HISTOGRAMS_DIR + venue_id + "/" + tracing_test_id + ".html"

    visualizer.figures_to_html(histogram_figs, html_filename)

    "1.2 Visualazing Filtering"

    acc_df = data_processing.acc_df(parsed_data)
    acc_filter_fig = visualizer.fig_acc_filter(acc_df)
    acc_filter_fig.show()


    "1.3 Waypoints viz"

    waypoints_fig = visualizer.fig_all_waypoints(floorplan, [])


    