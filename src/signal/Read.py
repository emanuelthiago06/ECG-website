import os
import csv
import json
from pathlib import Path

import wfdb
import numpy as np

from src.signal.Signal import Signal, ECG, VCG
import src.LogHelper as log


def tep_header_maker(**kwargs):
    """ Helps the writing of a header during an ECG object creation """

    default_head = {}

    # Check if there's a better way to define these default values
    default_head = {'fs': 1200, 'sig_len': 1000, 'n_sig': 12,
                    'base_date': None, 'base_time': None,
                    'units': ['mV', 'mV', 'mV', 'mV', 'mV', 'mV',
                              'mV', 'mV', 'mV', 'mV', 'mV', 'mV'],
                    'sig_name': ['I', 'II', 'III', 'AVR', 'AVL', 'AVF', 'V1',
                                 'V2', 'V3', 'V4', 'V5', 'V6'], 'comments': []}

    header_args_names = ['fs', 'sig_len', 'n_sig', 'base_date',
                         'base_time', 'units', 'sig_name', 'comments']
    for arg in header_args_names:
        if arg in kwargs:
            default_head[arg] = kwargs[arg]

    return default_head


def check_if_file_exists(file_path, verbose):
    """ Verifies whether the file exists """

    if Path(file_path).exists():
        log.processing("Acessing file: " + file_path +
                       "...", active_flag=verbose)
        return True
    else:
        log.error("File " + file_path + " does not exist!")
        return False


class Read(object):
    """
    Class containing methods to read an ECG or VCG from a file
    into an ECG or VCG object, respectively.
    """

    def read_ecg_dat(file_path, verbose=False):
        """ 
        Reads dat files containing 12-lead ECGs and maps their content to 
        an ECG object.

        Parameters
        ----------
        file_path : string
            Path of the file containing the 12-lead ECG
        verbose : bool, optional
            If True shows additional information regarding the files 
            (e.g: name of the file and whether the data was read 
            succesfully).

        Returns
        -------
        ECG: ECG Object


        Notes
        -----
        This method was tested using dat files from the PTB-XL database.

        Examples
        --------
        >>> ReadConvert.read_file("Patients/00001_hr.dat", verbose = True)

        """
        if not(check_if_file_exists(file_path, verbose)):
            return

        # Reading the signal at file_path (without the '.dat')
        signal_and_header = wfdb.io.rdsamp(
            os.path.splitext(file_path)[0], sampfrom=800)
        signal = signal_and_header[0]
        header = signal_and_header[1]

        filename = os.path.split(os.path.splitext(file_path)[0])[1]
        ecg = ECG(signal, filename, header)
        log.success("Data read succesfully!", active_flag=verbose)

        return ecg

    def read_ecg_teb(file_path, verbose=False):
        """ 
        Reads TEP files containing 12-lead ECGs and maps their content to 
        an ECG object.

        Parameters
        ----------
        file_path : string
            Path of the file containing the 12-lead ECG
        verbose : bool, optional
            If True shows additional information regarding the files 
            (e.g: name of the file and whether the data was read 
            succesfully).

        Returns
        -------
        ECG: ECG Object


        Notes
        -----
        At the moment this method only works with .TEP files obtained
        by the electrocardiographs TEB ECGPC manufactured by TEB 
        (Tecnologia Eletrônica Brasileira). The files are read 
        according to their extension.

        Examples
        --------
        >>> ReadConvert.read_file("Patients/teb_test1.TEP", verbose = True)

        """
        if not(check_if_file_exists(file_path, verbose)):
            return

        signal = []
        qtd_derivs = 12

        with open(file_path, "rb") as file:
            hex_list = ["{:02x}".format(c) for c in file.read()]

        # obtaining data from the file
        for count in range(0, qtd_derivs):
            temp_signal = [int(sample, 16) for sample in list(
                hex_list[1816+count*26880:28696+count*26880])]
            temp_signal = bytearray(temp_signal)

            samples = []
            for sample in np.ndarray(shape=(13440, 1), dtype='<i2', buffer=temp_signal):
                samples.append(sample[0])

            signal.append(np.asarray(samples))

        signal = np.transpose(signal)
        header = tep_header_maker(sig_len=signal.shape[0])

        filename = os.path.split(os.path.splitext(file_path)[0])[1]
        ecg = ECG(signal, filename, header)
        log.success("Data read succesfully!", active_flag=verbose)

        return ecg

    def read_ecg_csv(file_path, verbose=False):
        """ 
        Reads csv files containing 12-lead ECGs and maps their 
        content to an ECG object.

        Parameters
        ----------
        file_path : string
            Path of the file containing the 12-lead ECG
        verbose : bool, optional
            If True shows additional information regarding the files 
            (e.g: name of the file and whether the data was read 
            succesfully).

        Returns
        -------
        ECG: ECG Object


        Notes
        -----


        Examples
        --------
        >>> ReadConvert.read_file("Patients/ecg_example.csv", verbose = True)

        """
        # Reading the signal at file_path
        csv_data = []
        with open(file_path, newline='') as temp_file:
            spamreader = csv.reader(
                temp_file, delimiter=';', quotechar='|')
            for row in spamreader:
                csv_data.append(row)

        # Make header
        string_temp = ""
        for element in csv_data[0]:
            string_temp += element + ","

        string_temp = "{" + string_temp[:-2].replace(
            'None', '\"None\"').replace('\'', '\"') + "}"
        header = json.loads(string_temp)

        # Signal
        temp_signal = []
        for i in csv_data[2:]:
            list_string = np.array(i[0].split(' '))
            temp_signal.append(list_string.astype(np.float))
        signal = np.asarray(temp_signal)

        filename = os.path.split(os.path.splitext(file_path)[0])[1]
        ecg = ECG(signal, filename, header)
        log.success("Data read succesfully!", active_flag=verbose)

        return ecg

    def test(verbose=True):
        log.success("Read = Ok", active_flag=verbose)
        pass
