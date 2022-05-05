from random import sample
from scipy import signal

import pandas as pd
import numpy as np


def acc_butter_filter(order=8, cutoff_freq=2.5, sample_freq=50):
    """Signal filter polynomials of the butterworth filter designed for the accelerometer

    Args:
        order (int, optional): Order of the filter. Defaults to 5.
        cutoff_freq (int, optional): Cutoff frequency in Hz. Defaults to 2.
        sample_freq (int, optional): Sample frequency of the signals in Hz. Defaults to 50.

    Returns:
        (float, float): Polynomials of the IIR filter
    """
    b_filter, a_filter = signal.butter(
        N=order, Wn=cutoff_freq, btype="low", analog=False,  fs=sample_freq)
    return b_filter, a_filter


def filter_signal(data, b_filter, a_filter):
    """_summary_

    Args:
        filter (_type_): _description_
        signal (_type_): _description_

    Returns:
        _type_: _description_
    """

    signal_filt = signal.filtfilt(b_filter, a_filter, data, method="gust")
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


def acc_df(data_parser, calibrated=True):

    if calibrated:
        acc_parsed = data_parser.acc_calib
    else:
        acc_parsed = data_parser.acc_uncalib

    tss = np.array([xyz[0] for xyz in acc_parsed], dtype="int")
    non_filtered_acc = acc_magnitude(data_parser, calibrated=calibrated)
    b, a = acc_butter_filter()
    filtered_acc = filter_signal(non_filtered_acc, b, a)

    return pd.DataFrame(data={"tss": tss, "non_filtered_acc": non_filtered_acc, "filtered_acc": filtered_acc})
