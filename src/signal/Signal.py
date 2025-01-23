import os
import numpy as np
import pandas as pd

from biosppy.signals import ecg


class Signal(object):
    """
    Class containing methods to process signal objects such as ECG or
    VCG signals.
    ...

    Attributes
    ----------
    signal : np.array
        Array containing the ECG or VCG leads.

    filename : string
        Name of the file that the ECG or VCG signal Was read from.

    header : dict
        Dictionary containing information about the signal such as
        its sampling frequency, its length, the units of the lead
        values, name of the leads and comments.

    samplingFreq : int
        Sampling frequency of the original signal.

    filteredSignal : np.array
        Array containing the ECG leads after the application of a filtering algorithm

    rPeakIndexes : array
        Array containing the R-Peak indexes of ECG signal.

    heartRate : float
        Average heart rate value, obtained as the mean value of the heart rate obtained from each
        cycle (delimited by R-Peaks).

    """

    def __init__(self, signal, filename, header):
        self.signal = signal
        self.filename = filename
        self.header = header
        self.samplingFreq = header['fs']

        _, _, self.rPeakIndexes, _, _, _, \
            self.heartRate = ecg.ecg(self.signal[:, 0],
                                     self.samplingFreq, show=False)

        self.heartRate = np.mean(self.heartRate)

    def getSignalCycle(self, cycleNumber=1):
        """
        Returns the chosen cycle (points between two R peaks).

        Parameters
        ----------
        cycleNumber : int
            Number of the cycle that should be returned in the
            trimmed ECG.

        Returns
        -------
        signal_cycle : np.array
            Array containing the ECG/VCG lead samples that are in the
            chosen cycle.

        """
        if cycleNumber < len(self.rPeakIndexes):
            additional_samples = 2
            signal_cycle = self.signal[:, :][self.rPeakIndexes[cycleNumber-1] -
                                             additional_samples:self.rPeakIndexes[cycleNumber]+1+additional_samples]

            return signal_cycle

        else:
            raise ValueError("The parameter cycleNumber must be\
             less or equal than number of cycles in the ECG signal")

    def getAverageCycle(self):

        # A pair of rPeakIndexes define a cycle
        numberCycles = self.rPeakIndexes.size-1

        # A NumPy array is created to store all cycles
        allCycles = np.zeros(
            (self.signal.shape[0], self.signal.shape[1], numberCycles))

        # Each cycle is put in all cycles and has its size stored
        # in size_cycles. Note that each cycle has a different size
        size_cycles = []

        for cycle in range(1, numberCycles+1):
            ecgCycle = self.getSignalCycle(cycle)

            allCycles[:ecgCycle.shape[0],
                      :ecgCycle.shape[1], cycle-1] = ecgCycle

            size_cycles.append(ecgCycle.shape[0])

        numSamplesBiggestCycle = max(size_cycles)

        # The remaining rows of the np.array are deleted to make
        # allCycles.shape[0] == numSamplesBiggestCycle
        allCycles = np.delete(
            allCycles, np.s_[numSamplesBiggestCycle::1], 0)

        #
        rng = np.random.default_rng()
        randomNumberLimits = np.arange(
            1, numSamplesBiggestCycle-1)
        for cycle in range(numberCycles):

            sizeDifferenceMaxAndCurrentCycle = numSamplesBiggestCycle - \
                size_cycles[cycle]

            valuesToInsert = np.zeros((
                sizeDifferenceMaxAndCurrentCycle, self.signal.shape[1]))

            indexesToInsert = rng.choice(randomNumberLimits,
                                         sizeDifferenceMaxAndCurrentCycle,
                                         replace=False)

            for it, index in enumerate(indexesToInsert):
                valuesToInsert[it, :] = (allCycles[index+1, :, cycle] +
                                         allCycles[index-1, :, cycle])/2

            for lead in range(self.signal.shape[1]):
                new_lead_values = np.delete(
                    np.insert(allCycles[:, lead, cycle],
                              indexesToInsert, valuesToInsert[:, lead], axis=0),
                    np.s_[:sizeDifferenceMaxAndCurrentCycle], axis=0
                )
                allCycles[:, lead, cycle] = new_lead_values

        averageSignalCycle = np.mean(allCycles, axis=2)
        return averageSignalCycle


class ECG(Signal):
    """
    Class containing methods to process ECG objects, including
    methods to filter, select leads, plot and save the ECG signals.
    """

    def __init__(self, signal, filename, header):
        super().__init__(signal, filename, header)


class VCG(Signal):
    """
    Class containing methods to process VCG objects, including
    methods to plot/save the VCG signals and reconstruct the
    phase space of the VCG leads.
    """

    def __init__(self, signal, filename, header, reconstructionMethod):
        super().__init__(signal, filename, header)
        self.reconstructionMethod = reconstructionMethod
