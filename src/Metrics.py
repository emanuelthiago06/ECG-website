import math
import os
import sys
import glob
import time
import os.path

import cv2
import numpy as np
import matplotlib.pyplot as plt


class Metrics():
    """
    Class containing methods to calculate metrics of the signals.
    So far these metrics are only for the reconstructed phase
    space (RPS) images and to compare different RPS.
    ...

    Attributes
    ----------
    image1_path : string
        Path to one of the images contained the RPS to be compared.

    image2_path : string
        Path to the other image contained the RPS to be compared.

    block_size : int
        Size of the blocks that will be compared.

    image1 : np.array
        RPS image already threholded that will be compared.

    image2 : np.array
        Other RPS image already threholded that will be compared.
    """

    def __init__(self, img_path1, img_path2="", block_size=10):
        self.image1_path = img_path1
        self.image2_path = img_path2
        self.block_size = block_size
        self.image1 = ([] if img_path1 ==
                       "" else self.convert2binary(img_path1))
        self.image2 = ([] if img_path2 ==
                       "" else self.convert2binary(img_path2))

    def convert2binary(self, img_path):
        """ 
        The image is read and resized. After that, it is converted to gray 
        scale and then binarized

        Parameters
        ----------
        img_path : string
            Path to the image containing the phase space

        Returns
        -------
        thresholded_image: 
            Binary image containing the phase space

        Notes
        -----

        Examples
        --------
        >>> metrics.convert2binary(self,"")

        """

        if os.path.isfile(img_path) == False:
            raise(ValueError('Reconstructed phase space image not found'))

        img = cv2.imread(img_path)

        aux_row_size = img.shape[0]
        aux_row_size = int(aux_row_size / self.block_size)
        aux_row_size = self.block_size * aux_row_size

        aux_col_size = img.shape[1]
        aux_col_size = int(aux_col_size / self.block_size)
        aux_col_size = self.block_size * aux_col_size

        img = cv2.resize(img, (aux_row_size, aux_col_size))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        threshold, thresholded_image = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        return thresholded_image

    def count_method(self, image=[]):
        """ 
        Calculates the average pixel values ​​for each block. If less than 255 
        means that there is some black pixel in it and the counter is 
        incremented. Otherwise, the counter maintains its current value.

        Parameters
        ----------
        image: 
            Binary image containing the phase space

        Returns
        -------
        d: float 
            The index "d".

        Notes
        -----

        Examples
        --------
        >>> metrics.count_method(self, image = [])

        """

        th2 = np.array(image)
        if not len(th2):
            th2 = self.image1

        blockSize = self.block_size
        count = 0
        n_blocks = 0

        for r in range(0, th2.shape[0], blockSize):
            for c in range(0, th2.shape[1], blockSize):
                window = th2[r:r+blockSize, c:c+blockSize]
                n_blocks = n_blocks + 1
                if np.mean(window) < 255:
                    count = count + 1

        d = count/n_blocks
        return d

    def dif_method(self):
        """ 
        Calculates the difference between the d indexes of each image

        Parameters
        ----------


        Returns
        -------
        d_1 - d_2: float
            The difference between the "d" indexes of each image

        Notes
        -----

        Examples
        --------
        >>> metrics.dif_method(self)

        """

        d_1 = self.count_method(self.image1)
        d_2 = self.count_method(self.image2)
        return d_1 - d_2

    def sim_method(self):
        """ 
        It is created a counter with initial value 0 and a third matrix, 
        corresponding toa third image the same size as the other two. The third
        blocks images are then evaluated to count how many blocks are traversed
        by the trajectory by calculating the average of the pixel values ​​in that block.

        Parameters
        ----------

        Returns
        -------
        d_sim: int
            The number of blocks that are visited by the trajectory of the phase
        space in both images.

        Notes
        -----

        Examples
        --------
        >>> metrics.sim_method(self)

        """

        th2_1 = self.image1
        th2_2 = self.image2
        blockSize = self.block_size

        count = 0

        a, b = th2_1.shape
        # Cria terceira matriz com shape das outras sendo que so
        #  com valores 255
        th3 = np.full((a, b), 255)

        for r in range(0, th2_1.shape[0], blockSize):
            for c in range(0, th2_1.shape[1], blockSize):

                # Pega os dois blocos numa janela
                window1 = th2_1[r:r+blockSize, c:c+blockSize]
                window2 = th2_2[r:r+blockSize, c:c+blockSize]

                # Caso as duas janelas tenham trajetoria (preto na
                #  limiarizacao)
                if np.mean(window1) < 255 and np.mean(window2) < 255:
                    # Os pixels que compoem a janela da terceira imagem
                    #  ficam pretos
                    th3[r:r+blockSize, c:c+blockSize] = 0

        for r in range(0, th3.shape[0], blockSize):
            for c in range(0, th3.shape[1], blockSize):
                window = th3[r:r+blockSize, c:c+blockSize]
                if np.mean(window) < 255:
                    count = count + 1

        # Antes tava calculando o indice d(count/n_blocks)
        # Mas vi no roopaei que e a soma dos blocos 1 (count)
        d_sim = count

        return d_sim

    def sum_weights(self, thr_image):
        """ 
        Method used to assist in weighted box counting

        Parameters
        ----------

        Returns
        -------
        result_sum/temp_mat.size : float


        Notes
        -----

        Examples
        --------
        >>> metrics.sum_weights(self, thr_image)

        """

        th2 = thr_image
        blockSize = self.block_size
        temp_mat = []
        result_sum = 0
        for r in range(0, th2.shape[0], blockSize):
            temp_row = []
            for c in range(0, th2.shape[1], blockSize):
                # Pega um bloco
                window = th2[r:r+blockSize, c:c+blockSize]
                if np.mean(window) < 255:
                    temp_row.append(1)
                else:
                    temp_row.append(0)

            temp_mat.append(temp_row)
        temp_mat = np.array(temp_mat)

        for r in range(0,  temp_mat.shape[0]):
            for c in range(0, temp_mat.shape[0]):
                r_up = {True: r, False: r-1}[r == 0]
                r_down = {True: temp_mat.shape[0],
                          False: r+2}[r == temp_mat.shape[0]]
                c_left = {True: c, False: c-1}[c == 0]
                c_right = {True: temp_mat.shape[1],
                           False: c+2}[c == temp_mat.shape[1]]

                if np.sum(temp_mat[r_up:r_down, c_left:c_right]) >= temp_mat[r_up:r_down, c_left:c_right].size:
                    result_sum += 2
                elif np.sum(temp_mat[r_up:r_down, c_left:c_right]) > 0:
                    result_sum += 1
        return result_sum/temp_mat.size

    def pond_method(self):
        """ 
        Calculates the index in Weighted box counting method

        Parameters
        ----------

        Returns
        -------
            sum_weights(image1) - sum_weights(image2) : float 

        Notes
        -----

        Examples
        --------
        >>> metrics.sum_weights(self, thr_image)

        """
        return self.sum_weights(self.image1) - self.sum_weights(self.image2)
