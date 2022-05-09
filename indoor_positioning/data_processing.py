from random import sample
from scipy import signal

import pandas as pd
import numpy as np


def butter_filter(order=8, cutoff_freq=2.5, sample_freq=50, output="ba"):
    """Signal filter polynomials of the butterworth filter designed for the sensors

    Args:
        order (int, optional): Order of the filter. Defaults to 5.
        cutoff_freq (int, optional): Cutoff frequency in Hz. Defaults to 2.
        sample_freq (int, optional): Sample frequency of the signals in Hz. Defaults to 50.

    Returns:
        (float, float): Polynomials of the IIR filter
    """
    if output not in ['ba', 'sos']:
        raise ValueError("{} is not a valid output form.".format(output))

    if output == "ba":
        b_filter, a_filter = signal.butter(
            N=order, Wn=cutoff_freq, btype="low", analog=False,  fs=sample_freq)
        return b_filter, a_filter
    elif output == "sos":
        sos = signal.butter(
            N=order, Wn=cutoff_freq, btype="low", analog=False,  fs=sample_freq, output="sos")
        return sos


def filter_signal(data, filt_param, filt_type="sosfiltfilt"):
    """_summary_

    Args:
        filter (_type_): _description_
        signal (_type_): _description_

    Returns:
        _type_: _description_
    """
    if filt_type == "filtfilt":
        signal_filt = signal.filtfilt(filt_param[0], filt_param[1], data, method="gust")
    elif filt_type == "sosfiltfilt":
        signal_filt = signal.sosfiltfilt(filt_param, data)
    else:
        raise TypeError("Use either filtfilt or sosfiltfilt as the filt_type")

    return signal_filt


def acc_magnitude(data_parser, calibrated=True):

    if calibrated:
        acc_parsed = data_parser.acc_calib
    else:
        acc_parsed = data_parser.acc_uncalib

    acc_aux = [[xyz[1][0], xyz[1][1], xyz[1][2]] for xyz in acc_parsed]
    np_acc = np.array(acc_aux, dtype="float32")
    acc_mag = np.linalg.norm(np_acc, ord=2, axis=1)

    return acc_mag


def mag_magnitude(data_parser, calibrated=True):

    if calibrated:
        mag_parsed = data_parser.mag_calib
    else:
        mag_parsed = data_parser.mag_uncalib

    mag_aux = [[xyz[1][0], xyz[1][1], xyz[1][2]] for xyz in mag_parsed]
    np_mag = np.array(mag_aux, dtype="float32")
    mag_norm = np.linalg.norm(np_mag, ord=2, axis=1)

    return mag_norm


def acc_df(data_parser, calibrated=True, filt_type="sosfiltfilt"):

    if filt_type not in ['filtfilt', 'sosfiltfilt']:
        raise ValueError("{} is not a valid output form.".format(filt_type))

    if calibrated:
        acc_parsed = data_parser.acc_calib
    else:
        acc_parsed = data_parser.acc_uncalib

    tss = np.array([xyz[0] for xyz in acc_parsed], dtype="int")
    non_filtered_acc = acc_magnitude(data_parser, calibrated=calibrated)

    if filt_type == "filtfilt":
        b, a = butter_filter(output="ba")
        filtered_acc = filter_signal(non_filtered_acc, [b, a], filt_type=filt_type)
    else:
        sos = butter_filter(output="sos")
        filtered_acc = filter_signal(non_filtered_acc, sos, filt_type=filt_type)

    return pd.DataFrame(data={"tss": tss, "non_filtered_acc": non_filtered_acc, "filtered_acc": filtered_acc})


def mag_df(data_parser, calibrated=True):

    if calibrated:
        mag_parsed = data_parser.mag_calib
    else:
        mag_parsed = data_parser.mag_uncalib

    tss = np.array([xyz[0] for xyz in mag_parsed], dtype="int")
    mag_norm = mag_magnitude(data_parser, calibrated=calibrated)

    return pd.DataFrame(data={"tss": tss, "mag_magnitude": mag_norm})


def all_waypoint_distances(waypoint_list):
    len_mat = waypoint_list.shape[0]
    dist_matrix = np.empty((len_mat, len_mat), dtype="float32")
    for ix, waypoint in enumerate(waypoint_list):
        dist_matrix[ix, :] = np.linalg.norm((waypoint_list - waypoint), axis=1)
    return dist_matrix


def farthest_node(waypoint_list):
    dist_matrix = all_waypoint_distances(waypoint_list)

    # Excluding the distance to self node
    dist_matrix[dist_matrix == 0] = np.inf

    # Since the matrix is symetrical, axis can be either 0 or 1
    ind_farthest_node = np.argmax(np.min(dist_matrix, axis=1))

    return ind_farthest_node
