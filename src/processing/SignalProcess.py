import numpy as np
import entropy_estimators.continuous


class SignalProcess(object):

    def getOptimalTimeDelay(signalToBeEvaluated, maxTimeDelay=150):
        """
        Obtains the optimized time-delay (tau) in samples
        for the phase space reconstruction.

        Parameters
        ----------

        signalToBeEvaluated : np.array
            Array containing the temporal series (an ECG or VCG lead) 
            that will be evaluated to find the optimal time-delay value.

        tauMax : int, optional
            Maximum number of time-delay values that will be tested
            in order to determine the optimal time-delay value.

        Returns
        -------
        optimizedTimeDelay : int
            Value of the optimized time delay in number of samples.

        """

        timeDelayNotFound = None

        mutualInformation = np.zeros(maxTimeDelay+1)
        for currentTimeDelay in range(1, maxTimeDelay+1):

            # np.newaxis and np.trasposed were used to make the array
            # suitable for entropy_estimators.continuous.get_mi

            signalWithoutDelay = np.array(
                signalToBeEvaluated[:-currentTimeDelay])[np.newaxis]
            signalWithDelay = np.array(
                np.roll(signalToBeEvaluated, -currentTimeDelay)
                [:-currentTimeDelay])[np.newaxis]

            signalWithoutDelay = signalWithoutDelay.transpose()
            signalWithDelay = signalWithDelay.transpose()

            mutualInformation[currentTimeDelay] = \
                entropy_estimators.continuous.get_mi(signalWithoutDelay,
                                                     signalWithDelay)
            if (currentTimeDelay > 1 and
                    (mutualInformation[currentTimeDelay-1] <
                        mutualInformation[currentTimeDelay])):

                optimizedTimeDelay = currentTimeDelay - 1
                return optimizedTimeDelay

        optimizedTimeDelay = timeDelayNotFound

        return optimizedTimeDelay

    def reconstructPhaseSpace(timeSeries, samples_to_delay):
        """
        Reconstructs the bidimensional Phase Space representation of the signal 
        (timeSeries) and saves it to a NumPy array.

        Parameters
        ----------
        samples_to_delay : int, optional
            Time-delay to be applied to the signal to reconstruct its phase space.

        Returns
        -------
        reconstructedPhaseSpace : np.array
            Bidimensional Phase Space representation of timeSeries

        """

        data = timeSeries

        data_delayed = np.roll(data, -samples_to_delay)

        data = data[:-samples_to_delay]
        data_delayed = data_delayed[:-samples_to_delay]

        reconstructedPhaseSpace = np.transpose(
            np.array([data, data_delayed]))

        return reconstructedPhaseSpace
