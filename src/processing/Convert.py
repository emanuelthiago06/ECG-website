import os

import numpy as np

from src.signal.Signal import Signal, ECG, VCG
import src.LogHelper as log


class Convert(object):
    """
    Class containing methods to convert an ECG object to a VCG
    object or to a CSV.
    """

    def ecg_to_vcg(ECG, method=1, verbose=False):
        """
        Converts an ECG object to a VCG object based on the chosen method. 

        Parameters
        ----------
        ECG (ECG): ECG-type object.

        method : int, optional
            Method used to reconstruct Frank VCG. Defaults to 1 (Kors).

        verbose : bool, optional
            If True shows additional information regarding the files 

        Returns
        -------
            VCG: VCG-type object containing the signal 

        Notes
        -----

        Examples
        --------

        """

        # Dict with the conversion matrices to reconstruct the VCG
        matrix = {}

        matrix['kors'] = [[0.380, -0.070, 0.110], [-0.070, 0.930, -0.230],
                          [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                          [-0.130, 0.060, -0.430], [0.050, -0.020, -0.060],
                          [-0.010, -0.050, -0.140], [0.140, 0.060, -0.200],
                          [0.060, -0.170, -0.110], [0.540, 0.130, 0.310]]

        matrix['kors_quasi'] = [[0, 0, 0], [0, 1, 0], [0, 0, 0],
                                [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                                [0, 0, -0.5], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                                [1, 0, 0]]

        matrix['dower_inverse'] = [[0.632, -0.235, 0.059],
                                   [0.235, 1.066, -0.132], [-0.397, 1.301, 0.191],
                                   [-0.434, -0.415, 0.037], [0.515, -0.768, 0.125],
                                   [-0.081, 1.184, -0.162], [-0.515, 0.157, -0.917],
                                   [0.044, 0.164, -0.139], [0.882, 0.098, -1.277],
                                   [1.212, 0.127, -0.601], [1.125, 0.127, -0.086],
                                   [0.831, 0.076, 0.23]]

        if method == 1:
            methodName = 'kors'
        elif method == 2:
            methodName = 'kors_quasi'
        elif method == 3:
            methodName = 'dower_inverse'
        else:
            raise(ValueError('Invalid Method'))

        vcg_signal = ECG.signal@np.asarray(matrix[methodName])

        vcg = VCG(vcg_signal, ECG.filename,
                  ECG.header, methodName)

        log.success("ECG converted to VCG succesfully!", active_flag=verbose)
        return vcg

    def ecg_to_csv(ECG, filename, output_path='Converted_to_CSV', verbose=False):
        """
        Converts an ecg to a CSV file, including its header.

        Parameters
        ----------
            ECG (ECG): ECG class.
            filename: string 
                Name of the CSV file that will be saved.
            output_path: string
                Path to which the CSV file will be saved.
            verbose : bool, optional
                If True shows additional information regarding the files.

        Returns
        -------
            None

        Notes
        -----

        Examples
        --------
        """

        # Checking whether the directory exists
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Creating file
        csv_file = open(output_path+"/" + filename + ".csv", "w")

        # Writing the CSV file
        # DEPOIS:  Colocar o numero de campos do header = numero de colunas
        #  do sinal (RFC 4180 secao 2.3)
        for key, value in ECG.header.items():
            header = "".join(["\""+str(key)+"\"", ":", str(value), ","])
            csv_file.write(header)
        csv_file.write('\n\n')

        # Writing the signal on the CSV file
        for i in range(0, len(ECG.signal)):
            for j in range(0, len(ECG.signal[i])):
                if j != 0:
                    csv_file.write(",")
                csv_file.write(str(ECG.signal[i][j]))
            csv_file.write('\n')

        csv_file.close()
        log.success("ECG converted to CSV succesfully!", active_flag=verbose)

    def test(verbose=True):
        log.success("Convert = Ok", active_flag=verbose)
        pass
