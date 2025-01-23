import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import cv2


def convert_fig_to_array(fig):
    """
    Small function that creates a canvas, draws it and converts
    it to a numpy array that is returned. This is done due to a
    memory leak problem that occurs when we save a lot of figures 
    (>>1e4) if they're not shown.
    """

    canvas = FigureCanvas(fig)
    canvas.draw()
    imgBuffer = canvas.buffer_rgba()
    return np.asarray(imgBuffer)


class Display(object):
    """
    Class containing methods to display or save data, such as
    ECG/VCG leads, mutual information curves, 3D VCG, VCG planes, 
    and bidimensional reconstructed phase space.
    ...

    Attributes
    ----------
    dataToBeDisplayed : np.array
        Array containing the ECG leads (12 leads).

    figureSize : tuple
        Name of the file that the ECG signal came from.

    plotLimits : list
        Name of the VCG reconstruction method used to obtain the VCG.      

    """

    def __init__(self, dataToBeDisplayed, figureSize, plotLimits):
        self.dataToBeDisplayed = dataToBeDisplayed
        self.figureSize = figureSize
        self.plotLimits = plotLimits

    def plot_lead(self):
        """ 
        Plots the ECG or VCG lead on the Display instance.


        Parameters
        ----------
        None

        Returns
        -------
        None

        Notes
        -----

        Examples
        --------
        >>> displayEcgLeadI.plot_lead()

        """

        # Depois adicionar a parte pra verificar os erros
        # Ver a parte de adição dos valores de instante de tempo
        # Talvez passar fs como arg pra função

        # if not(self.dataToBeDisplayed.shape[1] == 1):
        #     raise TypeError('Array must have shape (n,1)')
        plt.figure(figsize=self.figureSize)
        plt.plot(self.dataToBeDisplayed, '-k')
        plt.axis(self.plotLimits)
        plt.show()

    def plot_signal(self):
        """ 
        Plots all the leads of an ECG or VCG signal, where
        each lead is in a different subplot.


        Parameters
        ----------
        None

        Returns
        -------
        None

        Notes
        -----

        Examples
        --------
        >>> displayEcgLeadI.plot_signal()

        """
        plt.figure(figsize=self.figureSize)

        numberOfLeads = self.dataToBeDisplayed.shape[1]
        numberOfColsPlot = 3
        for numPlot in range(1, numberOfLeads+1):
            plt.subplot(numberOfLeads//numberOfColsPlot +
                        numberOfLeads % numberOfColsPlot,
                        numberOfColsPlot, numPlot)

            plt.plot(self.dataToBeDisplayed, '-k')
            plt.axis(self.plotLimits)

        plt.show()

    def plot_mutual_information_curve(self):
        """ 
        Plots the mutual information curve between a signal
        and its delayed version. The first local minimum in
        this curve is used to reconstruct the phase space of
        that signal.


        Parameters
        ----------
        None

        Returns
        -------
        None

        Notes
        -----

        Examples
        --------
        >>> displayEcgLeadI.plot_mutual_information_curve()

        """

        plt.figure(figsize=self.figureSize)
        plt.plot(self.dataToBeDisplayed, '-k')
        plt.axis(self.plotLimits)

        plt.title('Mutual Information vs Delay')
        plt.ylabel('Mutual information')
        plt.xlabel('Delay (number of samples)')

        plt.show()

    def plot_VCG_3D(self):
        """
        Plots the 3D representation of a VCG signal.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Notes
        -----

        Examples
        --------
        >>> displayVCG.plot_VCG_3D()
        """

        fig = plt.figure(figsize=self.figureSize)
        ax = fig.gca(projection='3d')
        ax.plot(self.dataToBeDisplayed[:, 0],
                self.dataToBeDisplayed[:, 1],
                self.dataToBeDisplayed[:, 2])
        plt.show()

    def plot_VCG_plane(self, planeName):
        """
        Plots a plane derived from the the 3D representation
         of a VCG signal.

        Parameters
        ----------
        planeName : string
            Name of the VCG plane (XY,XZ,YZ) to be shown on
             the plot.

        Returns
        -------
        None

        Notes
        -----

        Examples
        --------
        >>> displayVCG.plot_VCG_plane()
        """
        fig = plt.figure(figsize=self.figureSize)
        plt.plot(self.dataToBeDisplayed[:, 0],
                 self.dataToBeDisplayed[:, 1],
                 '-k')
        plt.axis(self.plotLimits)
        plt.title(planeName)
        plt.tight_layout()
        plt.show()

    def plot_RPS(self, showAxis='off'):
        """
        Plots reconstructed phase spaces.

        Parameters
        ----------
        showAxis : string
            Determines whether the plot axis are shown or not. 
            Receives values such as 'on' and 'off'. 
            To check other options see the 'options' parameter in 
            the pyplot.axis reference.

        Returns
        -------
        path : string
            Path to the saved figure. If no figure is saved then 
            an empty string is returned.

        Notes
        -----

        Examples
        --------
        >>> displayRPS.plot_RPS('off)


        """
        fig = plt.figure(figsize=self.figureSize)
        plt.plot(self.dataToBeDisplayed[:, 0],
                 self.dataToBeDisplayed[:, 1],
                 '-k')
        plt.axis(self.plotLimits)
        plt.axis(showAxis)
        plt.tight_layout()
        plt.show()

    def save_lead_image(self, imageFilename):
        """ 
        Saves the lead signal as an image.

        Parameters
        ----------
        imageFilename : string
            Name of the image to be saved.

        Returns
        -------
        None

        Notes
        -----

        Examples
        --------
        >>> displayEcgLeadI.save_lead('leadI.png')

        """

        matplotlib.use("Agg")

        fig = plt.figure(figsize=self.figureSize, clear=True)

        plt.plot(self.dataToBeDisplayed, '-k')
        plt.axis(self.plotLimits)

        img = convert_fig_to_array(fig)

        plt.imsave(imageFilename, img, cmap='gray')
        plt.close('all')

    def save_signal_image(self, imageFilename):
        """ 
        Saves the signal (all leads) as an image.

        Parameters
        ----------
        imageFilename : string
            Name of the image to be saved.

        Returns
        -------
        None

        Notes
        -----

        Examples
        --------
        >>> displayECG.save_signal_image('12leadECG.png)

        """

        matplotlib.use("Agg")

        fig = plt.figure(figsize=self.figureSize, clear=True)

        numberOfLeads = self.dataToBeDisplayed.shape[1]
        numberOfColsPlot = 3
        for numPlot in range(1, numberOfLeads+1):
            plt.subplot(numberOfLeads//numberOfColsPlot +
                        numberOfLeads % numberOfColsPlot,
                        numberOfColsPlot, numPlot)

            plt.plot(self.dataToBeDisplayed, '-k')
            plt.axis(self.plotLimits)

        img = convert_fig_to_array(fig)

        plt.imsave(imageFilename, img, cmap='gray')
        plt.close('all')

    def save_VCG_plane_image(self, imageFilename):
        """ 
        Saves a plane of a VCG as an image.

        Parameters
        ----------
        imageFilename : string
            Name of the image to be saved.

        Returns
        -------
        None

        Notes
        -----

        Examples
        --------
        >>> VCGPlaneXY.save_VCG_plane_image('XY.png')

        """

        matplotlib.use("Agg")

        fig = plt.figure(figsize=self.figureSize, clear=True)
        plt.plot(self.dataToBeDisplayed[:, 0],
                 self.dataToBeDisplayed[:, 1],
                 '-k')
        plt.axis(self.plotLimits)
        plt.tight_layout()

        img = convert_fig_to_array(fig)

        plt.imsave(imageFilename, img, cmap='gray')
        plt.close('all')

    def save_RPS_image(self, imageFilename, showAxis='off'):
        """ 
        Saves the two-dimensional phase space reconstruction as 
        an image with or without its axes.

        Parameters
        ----------
        imageFilename : string
            Name of the image to be saved.

        showAxis : string
            Determines whether the plot axis are shown or not. 
            Receives values such as 'on' and 'off'. 
            To check other options see the 'options' parameter in 
            the pyplot.axis reference.


        Returns
        -------
        None

        Notes
        -----

        Examples
        --------
        >>> displayRPSX.save_RPS_image('RPS_X_tau001s.png')
        >>> displayRPSX.save_RPS_image('RPS_X_tau001s.png', 'off')
        >>> displayRPSX.save_RPS_image('RPS_X_tau001s.png', 'on')

        """

        matplotlib.use("Agg")

        fig = plt.figure(figsize=self.figureSize, clear=True)
        plt.plot(self.dataToBeDisplayed[:, 0],
                 self.dataToBeDisplayed[:, 1],
                 '-k')
        #plt.axis(self.plotLimits)
        plt.axis(showAxis)
        plt.tight_layout()

        img = convert_fig_to_array(fig)

        plt.imsave(imageFilename, img, cmap='gray')
        plt.close('all')

    def encode_3lead_RPS_on_image(self, imageFilename):
        """ 
        Saves the two-dimensional phase space reconstruction as 
        an image without its axes where each color channel corresponds to
        a signal lead. The blue, green and red channels correspond, 
        respectively, to the first, second and third lead dataToBeDisplayed.  

        Parameters
        ----------
        imageFilename : string
            Name of the image to be saved.

        Returns
        -------
        None

        Notes
        -----

        Examples
        --------
        >>> disp_rps.encode_3lead_RPS_on_image('rps_signal1.png')

        """

        matplotlib.use("Agg")

        figureSizeAbsolute = (int(self.figureSize[0]*100),
                              int(self.figureSize[1]*100))

        outputImage = np.zeros(
            (figureSizeAbsolute[0], figureSizeAbsolute[1], 3), dtype=np.uint8)

        for lead in range(3):
            fig = plt.figure(figsize=self.figureSize, clear=True)

            plt.plot(self.dataToBeDisplayed[:, 0, lead],
                     self.dataToBeDisplayed[:, 1, lead], '-k')
            plt.axis(self.plotLimits)
            plt.axis('off')

            fig.tight_layout(pad=0)
            fig.canvas.draw()

            rps_lead_rgb_data = np.frombuffer(
                fig.canvas.tostring_rgb(), dtype=np.uint8)
            rps_lead_rgb_data = rps_lead_rgb_data.reshape(
                fig.canvas.get_width_height()[::-1] + (3,))

            rps_lead_gray_data = cv2.cvtColor(
                rps_lead_rgb_data, cv2.COLOR_RGB2GRAY)
            _, rps_lead_threshold_data = cv2.threshold(
                rps_lead_gray_data, 200, 255, cv2.THRESH_BINARY_INV)
            outputImage[:, :, lead] = rps_lead_threshold_data

        cv2.imwrite(imageFilename, outputImage)
        plt.close('all')
