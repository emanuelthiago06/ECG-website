import numpy as np
from biosppy.signals import ecg


class Filter(object):
    def fir_biosppy(signal, samplingFreq):
        """ 
        Filters the signal (all leads) using a FIR
        bandpass [3, 45] filter with order = int(0.3 * sampling rate).

        Parameters
        ----------
        self.signal : np.array
            NumPy array containg the leads of the signal that will
            be filtered.
        samplingFreq : int
            Sampling Frequency of the signal that will be filtered.

        Returns
        -------
        filteredSignal : np.array
            NumPy array containg the leads of the signal after
            the filtering operation.
        Notes
        -----

        Examples
        --------
        >>> Filter.fir_biosppy(ecg.signal, ecg.samplingFreq)

        """

        filteredSignal = np.zeros_like(signal)
        number_leads = signal.shape[1]

        for lead in range(number_leads):
            filteredSignal[:, lead] = ecg.ecg(
                signal[:, lead], samplingFreq, show=False)[1]

        return filteredSignal
