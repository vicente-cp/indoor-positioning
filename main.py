from indoor_positioning import data_parser, visualizer
from pathlib import Path

import glob


DATA_DIR = './dataset/5cd56b6ae2acfd2d33b59ccb/'
OUTPUT_DIR = './output/'
TSS_HISTOGRAMS_DIR = OUTPUT_DIR + "tss_hist/"

if __name__ == "__main__":
    venue_location_id = DATA_DIR.split("/")[2]

    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    Path(TSS_HISTOGRAMS_DIR).mkdir(parents=True, exist_ok=True)
    Path(TSS_HISTOGRAMS_DIR + venue_location_id).mkdir(parents=True, exist_ok=True)

    tracing_files = glob.glob(DATA_DIR + "**/*.txt", recursive=True)
    tracing_test = tracing_files[0]
    parsed_data = data_parser.tracing_parser(tracing_test)

    "1 -- Visualizing tss difference"
    sensors_to_viz = {
        "Calibrated Acce": parsed_data.acc_calib,
        "Calibrated Magnetometer": parsed_data.mag_calib,
        "Calibrated Gyro": parsed_data.gyro_calib}

    histogram_figs = []
    for sensor in sensors_to_viz:
        tss = [xyz[0] for xyz in sensors_to_viz[sensor]]
        histogram_figs.append(visualizer.viz_histogram_tss_diff(tss))

    html_filename = TSS_HISTOGRAMS_DIR + \
        venue_location_id + "/" + \
        tracing_test.split("/")[4][:-4] + ".html"

    visualizer.figures_to_html(histogram_figs, html_filename)
