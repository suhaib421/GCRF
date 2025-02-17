# -*- coding: utf-8 -*-
#
#File: fNIRSSignalGenerator.py
#
'''
Created on Fri Jul 03 21:27:00 2020
Module ***fNIRSSignalGenerator***
This module implements the class :class:`fNIRSSignalGenerator <fNIRSSignalGenerator>`.
:Log:
+-------------+---------+------------------------------------------------------+
| Date        | Authors | Description                                          |
+=============+=========+======================================================+
| 03-Jul-2020 |   FOE   | - Class :class:`fNIRSSignalGenerator` created but    |
|             |   JJR   |   unfinished.                                        |
+-------------+--------+------------------------------------------------------+
.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx> and Jesús Joel Rivas <jrivas@inaoep.mx>
.. codeauthor::    Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx> and Jesús Joel Rivas <jrivas@inaoep.mx>
'''

import copy
import warnings

import numpy as np
import random
import math 

import matplotlib.pyplot as plt

import csv
import pandas as pd
import scipy.io
import h5py
import sys
#from sklearn import preprocessing

#from scipy import stats

#import CONST

from optodeArrayInfo import optodeArrayInfo

from channelLocationMap import channelLocationMap

# Class fNIRSSignalGenerator is a subclass of channelLocationMap
class fNIRSSignalGenerator(channelLocationMap):
    '''
    A basic class to generate synthetic fNIRS signals.
    '''

    #def __init__(self, nSamples = 1, nChannels = 1):   # __init__ used before the creation of the class channelLocationMap
    def __init__(self, nSamples=1, id=1, description='ChannelLocationMap0001', nChannels=1, nOptodes=1,
                 chLocations=np.array([[np.NaN, np.NaN, np.NaN]]),
                 optodesLocations=np.array([[np.NaN, np.NaN, np.NaN]]),
                 optodesTypes=np.array([np.NaN]), referencePoints=dict(), surfacePositioningSystem='UI 10/20',
                 chSurfacePositions=tuple(('',)), optodesSurfacePositions=tuple(('',)),
                 chOptodeArrays=np.array([np.NaN]),
                 optodesOptodeArrays=np.array([np.NaN]), pairings=np.array([[np.NaN, np.NaN]]),
                 optodeArrays=np.array([optodeArrayInfo()])):
        '''
        Class constructor.
        :Properties:
        data: The fNIRS data tensor.
        #frequency_bands: The EEG frequency bands.
        :Parameters:
        :param nSamples: Number of temporal samples.
            Optional. Default is 1.
        :type nSamples: int (positive)
        :param nChannels: Number of channels.
            Optional. Default is 1.
        :type nChannels: int (positive)
        '''
        # Initialization of an object of the superclass channelLocationMap
        super().__init__(id = id, description = description, nChannels = nChannels, nOptodes = nOptodes,
                         chLocations = chLocations, optodesLocations = optodesLocations,
                         optodesTypes = optodesTypes, referencePoints = referencePoints,
                         surfacePositioningSystem = surfacePositioningSystem,
                         chSurfacePositions = chSurfacePositions, optodesSurfacePositions = optodesSurfacePositions,
                         chOptodeArrays = chOptodeArrays,
                         optodesOptodeArrays = optodesOptodeArrays, pairings = pairings,
                         optodeArrays = optodeArrays)

        #Ensure all properties exist
        self.__data = np.zeros((0,0,0),dtype=float)
        self.__samplingRate = 10 #[Hz]

        #Check parameters
        if type(nSamples) is not int:
            msg = self.getClassName() + ':__init__: Unexpected parameter type for parameter ''nSamples''.'
            raise ValueError(msg)
        if nSamples < 0:
            msg = self.getClassName() + ':__init__: Unexpected parameter value for parameter ''nSamples''.'
            raise ValueError(msg)
        if type(nChannels) is not int:
            msg = self.getClassName() + ':__init__: Unexpected parameter type for parameter ''nChannels''.'
            raise ValueError(msg)
        if nChannels < 0:
            msg = self.getClassName() + ':__init__: Unexpected parameter value for parameter ''nChannels''.'
            raise ValueError(msg)

        #Initialize
        self.data = np.zeros((nSamples,nChannels,2),dtype=float)

        # Create constant HBO2 = 0 and constant HHB = 1
        # Represent HbO2 (Oxi) and HHb (Desoxi) respectively
        # for the third component of the tensor data.
        self.__HBO2 = 0
        self.__HHB  = 1

        return
    #end __init__(self, nSamples = 1, nChannels = 1)


    #Properties getters/setters
    #
    # Remember: Sphinx ignores docstrings on property setters so all
    #documentation for a property must be on the @property method

    # Note that python does not have constants nor static constants,
    # so in order to have a constant, a new property is defined
    # with only a getter method and the setter method raises an error message.
    @property
    def HBO2(self):  # HBO2 getter
        '''
        Constant HBO2 = 0
        Represents HbO2 (Oxi) for the third component of the tensor data.
        :getter: Gets constant HBO2.
        :type: int
        '''

        return 0
    # end HBO2(self)

    @HBO2.setter
    def HBO2(self, value):  # HBO2 setter
        '''
        Constant HBO2 = 0
        Represents HbO2 (Oxi) for the third component of the tensor data.
        :setter: Raise an error message because the value of constant HBO2 is being tried to be changed.
        :type: int
        '''

        msg = self.getClassName() + ':HBO2: ConstantError: Can not rebind const.'
        raise ValueError(msg)
    # end HBO2(self, value)

    @property
    def HHB(self):  # HHB getter
        '''
        Constant HHB = 1
        Represents HHb (Desoxi) for the third component of the tensor data.
        :getter: Gets constant HHB.
        :type: int
        '''

        return 1
    # end HHB(self)

    @HHB.setter
    def HHB(self, value):  # HHB setter
        '''
        Constant HHB = 1
        Represents HHb (Desoxi) for the third component of the tensor data.
        :setter: Raise an error message because the value of constant HHB is being tried to be changed.
        :type: int
        '''

        msg = self.getClassName() + ':HHB: ConstantError: Can not rebind const.'
        raise ValueError(msg)
    # end HHB(self, value)


    @property
    def data(self): #data getter
        '''
        The data tensor.
        The data tensor always have 3 dimensions, namely:
        * Temporal (temporal samples)
        * Spatial (channels)
        * Signals (for fNIRS this is fixed to 2; the oxygenated (HbO2) and the deoxygenated (HHb) hemoglobin)
        :getter: Gets the data.
        :setter: Sets the data.
        :type: numpy.ndarray [nSamples x nChannels x 2]
        '''

        return copy.deepcopy(self.__data)
    #end data(self)

    @data.setter
    def data(self,newData): #data setter

        #Check parameters
        if type(newData) is not np.ndarray:
            msg = self.getClassName() + ':data: Unexpected attribute type.'
            raise ValueError(msg)
        if newData.ndim != 3:
            msg = self.getClassName() + ':data: Unexpected attribute value. ' \
                    + 'Data tensor must be 3D <temporal, spatial, signal>'
            raise ValueError(msg)
        if newData.shape[2] != 2:
            msg = self.getClassName() + ':data: Unexpected attribute value. ' \
                    + 'Number of signals in fNIRS must be 2.'
            raise ValueError(msg)

        self.__data = copy.deepcopy(newData)

        return None
    #end data(self,newData)


    @property
    def nChannels(self): #nChannels getter
        '''
        Number of channels.
        When setting the number of channels:
        * if the number of channels is smaller than
        the current number of channels, a warning is issued
        and the channels indexed rightmost in the data tensor will be
        removed.
        * if the number of channels is greater than
        the current number of channels, the new channels will
        be filled with zeros.
        :getter: Gets the number of channels.
        :setter: Sets the number of channels.
        :type: int
        '''

        return self.__data.shape[1]
    #end nChannels(self)

    @nChannels.setter
    def nChannels(self,newNChannels): #nChannels setter

        #Check parameters
        if type(newNChannels) is not int:
            msg = self.getClassName() + ':nChannels: Unexpected attribute type.'
            raise ValueError(msg)
        if newNChannels < 0:
            msg = self.getClassName() + ':nChannels: Unexpected attribute value. Number of channels must be greater or equal than 0.'
            raise ValueError(msg)

        if newNChannels > self.nChannels:
            #Add channels with zeros
            tmpNChannels = newNChannels-self.nChannels
            tmpData = np.zeros((self.nSamples,tmpNChannels,2),dtype=float)
            self.data = np.concatenate((self.data,tmpData), axis=1)
        elif newNChannels < self.nChannels:
            msg = self.getClassName() + ':nChannels: New number of channels is smaller than current number of channels. Some data will be lost.'
            warnings.warn(msg,RuntimeWarning)
            self.data = copy.deepcopy(self.data[:,0:newNChannels,:])

        return None
    #end nChannels(self,newNChannels)


    @property
    def nSamples(self): #nSamples getter
        '''
        Number of temporal samples.
        When setting the number of temporal samples:
        * if the number of temporal samples is smaller than
        the current number of temporal samples, a warning is issued
        and the last temporal samples will be removed.
        * if the number of temporal samples is greater than
        the current number of temporal samples, the new temporal samples will
        be filled with zeros.
        :getter: Gets the number of temporal samples.
        :setter: Sets the number of temporal samples.
        :type: int
        '''

        return self.__data.shape[0]
    #end nSamples(self)

    @nSamples.setter
    def nSamples(self,newNSamples): #nSamples setter

        #Check parameters
        if type(newNSamples) is not int:
            msg = self.getClassName() + ':nSamples: Unexpected attribute type.'
            raise ValueError(msg)
        if newNSamples < 0:
            msg = self.getClassName() + ':nSamples: Unexpected attribute value. Number of temporal samples must be greater or equal than 0.'
            raise ValueError(msg)

        if newNSamples > self.nSamples:
            #Add channels with zeros
            tmpNSamples = newNSamples-self.nSamples
            tmpData = np.zeros((tmpNSamples,self.nChannels,2),dtype=float)
            self.data = np.concatenate((self.data,tmpData), axis=0)
        elif newNSamples < self.nSamples:
            msg = self.getClassName() + ':nSamples: New number of temporal samples is smaller than current number of temporal samples. Some data will be lost.'
            warnings.warn(msg,RuntimeWarning)
            self.data = copy.deepcopy(self.data[0:newNSamples,:,:])

        return None
    #end nSamples(self,newNSamples)


    @property
    def samplingRate(self): #samplingrate getter
        '''
        Sampling rate at which the synthetic data will be generated.
        :getter: Gets the sampling rate.
        :setter: Sets the sampling rate.
        :type: float
        '''

        return self.__samplingRate
    #end samplingRate(self)

    @samplingRate.setter
    def samplingRate(self,newSamplingRate): #samplingrate setter

        #Check parameters
        if type(newSamplingRate) is int:
            newSamplingRate = float(newSamplingRate)
        if type(newSamplingRate) is not float:
            msg = self.getClassName() + ':samplingrate: Unexpected attribute type.'
            raise ValueError(msg)
        if newSamplingRate <= 0:
            msg = self.getClassName() + ':samplingrate: Unexpected attribute value. ' \
                    + 'Sampling rate must be strictly positive.'
            raise ValueError(msg)

        self.__samplingRate = newSamplingRate

        return None
    #end samplingRate(self,newSamplingRate)


    #Private methods


    #Protected methods


    #Public methods

    def getClassName(self):
        '''Gets the class name.
        :return: The class name
        :rtype: str
        '''

        return type(self).__name__
    #end getClassName(self)


    def addStimulusResult(self, channelsList=list(), boxCarList=list(), initSample=0, endSample=-1, \
                           tau_p=6, tau_d=10, amplitudeScalingFactor=6, \
                           enableHbO2Channels = np.ones(1, dtype=int), \
                           enableHHbChannels = np.ones(1, dtype=int), \
                           enableHbO2Blocks = np.ones(1, dtype=int), \
                           enableHHbBlocks = np.ones(1, dtype=int), boxcar_amp=[1], channel_amp=[1]):
        '''
        Adds a stimulus result to the data tensor.
        This method calls :meth:`generateStimulusResult` for generating
        the new synthetic data corresponding to the stimulus whose times of occurrence
        are on the supplied boxcar.
        Here, such newly generated data tensor is added to the class :attr:`data`.
        :Parameters:
        :param channelsList: List of channels affected. Default is the empty list.
        :type channelsList: list
        :param boxCarList: List of tuples. Each tuple is a pair (xi, yi).
            (xi, yi) is an interval where the boxcar is equal to 1.
            0 <= xi, yi < nSamples/samplingRate, xi < yi.
            Default is the empty list.
        :type boxCarList: list
        :param initSample: Initial temporal sample. Default is 0.
        :type initSample: int (positive)
        :param endSample: Last temporal sample. A positive value
            explicitly indicates a sample. A value -1 indicates the last
            sample of :attr:`data`. If not -1, then the endSample must be
            greater than the initSample. Default is -1.
        :type endSample: int (positive or -1)
        :param tau_p: stands for the first peak delay, which is basically set to 6 sec. Default is 6.
        :type tau_p: int (positive)
        :param tau_d: stands for the second peak delay, which is basically set to 10 sec. Default is 10.
            Represents the delay of undershoot to response.
        :type tau_d: int (positive)
        :param amplitudeScalingFactor: A scaling factor for the amplitude.
            It is the amplitude ratio between the first and second peaks.
            It was set to 6 sec. as in typical fMRI studies.
            Default is 6.
        :type amplitudeScalingFactor: float (positive)
        :param enableHbO2Channels: A vector whose length is nChannels. Each position contains an integer value: 1 or 0.
            The value 1 indicates that the corresponding channel has the HbO2 signal enabled, and 0 indicates otherwise.
            Default is array([1]). This array of 1´s is extended automatically, by the compiler, to the number of
            channels (columns) and the number of samples (rows) when the operation * (element-wise matrix multiplication)
            is applied.
        :type numpy.ndarray
        :param enableHHbChannels: A vector whose length is nChannels. Each position contains an integer value: 1 or 0.
            The value 1 indicates that the corresponding channel has the HHb signal enabled, and 0 indicates otherwise.
            Default is array([1]). This array of 1´s is extended automatically, by the compiler, to the number of
            channels (columns) and the number of samples (rows) when the operation * (element-wise matrix multiplication)
            is applied.
        :type numpy.ndarray
        :param enableHbO2Blocks: A vector whose length is nBlocks. Each position contains an integer value: 1 or 0.
            The value 1 indicates that the corresponding block has the HbO2 signal enabled, and 0 indicates otherwise.
            Default is array([1]). This array of 1´s is extended automatically, by the compiler, to the number of
            blocks (columns) and the number of samples (rows) when the operation * (element-wise matrix multiplication)   OJO
            is applied.
        :type numpy.ndarray
        :param enableHHbBlocks: A vector whose length is nBlocks. Each position contains an integer value: 1 or 0.
            The value 1 indicates that the corresponding block has the HHb signal enabled, and 0 indicates otherwise.
            Default is array([1]). This array of 1´s is extended automatically, by the compiler, to the number of
            blocks (columns) and the number of samples (rows) when the operation * (element-wise matrix multiplication)   OJO
            is applied.
        :type numpy.ndarray
        :return: None
        :rtype: NoneType
        '''

        # Check parameters
        if type(channelsList) is not list:
            msg = self.getClassName() + ':addStimulusResult: Unexpected parameter type for parameter ''channelList''.'
            raise ValueError(msg)
        for elem in channelsList:
            if type(elem) is not int:
                msg = self.getClassName() + ':addStimulusResult: Unexpected parameter value for parameter ''channelList''.'
                raise ValueError(msg)
            if elem < 0 or elem >= self.nChannels:  # Ensure the nChannels exist
                msg = self.getClassName() + ':addStimulusResult: Unexpected parameter value for parameter ''channelList''.'
                raise ValueError(msg)

        if type(initSample) is not int:
            msg = self.getClassName() + ':addStimulusResult: Unexpected parameter type for parameter ''initSample''.'
            raise ValueError(msg)
        if initSample < 0 or initSample >= self.nSamples:  # Ensure the nSamples exist
            msg = self.getClassName() + ':addStimulusResult: Unexpected parameter value for parameter ''initSample''.'
            raise ValueError(msg)

        if type(endSample) is not int:
            msg = self.getClassName() + ':addStimulusResult: Unexpected parameter type for parameter ''endSample''.'
            raise ValueError(msg)
        if endSample < -1 or endSample >= self.nSamples:  # Ensure the nSamples exist
            msg = self.getClassName() + ':addStimulusResult: Unexpected parameter value for parameter ''endSample''.'
            raise ValueError(msg)
        if endSample == -1:  # If -1, substitute by the maximum last sample
            endSample = self.nSamples - 1
        if endSample <= initSample:  # Ensure the endSample is posterior to the initSample
            msg = self.getClassName() + ':addStimulusResult: Unexpected parameter value for parameter ''endSample''.'
            raise ValueError(msg)
        #No need to type check boxCarList, tau_p, tau_d, amplitudeScalingFactor, enableHbO2Channels, enableHHbChannels,
        #enableHbO2Blocks, and enableHHbBlocks as these
        #are passed to method generateStimulusResult.

        channelsList = list(set(channelsList))  # Unique and sort elements
        nChannels = len(channelsList)
        nSamples = endSample - initSample
        tmpData = self.generateStimulusResult(boxCarList=boxCarList, \
                                              nSamples=nSamples, \
                                              nChannels=nChannels, \
                                              tau_p=tau_p, \
                                              tau_d=tau_d, \
                                              amplitudeScalingFactor=amplitudeScalingFactor, \
                                              enableHbO2Channels=enableHbO2Channels, \
                                              enableHHbChannels=enableHHbChannels, \
                                              enableHbO2Blocks=enableHbO2Blocks, \
                                              enableHHbBlocks=enableHHbBlocks, boxcar_amp=boxcar_amp, channel_amp=channel_amp)
        self.__data[initSample:endSample, channelsList, :] = \
            self.__data[initSample:endSample, channelsList, :] + tmpData

        return
    # end addStimulusResult(self,channelsList = list(), boxCarList=list(), initSample = 0, ... , enableHHbBlocks = np.ones(1, dtype=int))


    def double_gamma_function(self, timestamps = np.arange(25, dtype=float), \
                                tau_p = 6, tau_d = 10, amplitudeScalingFactor = 6):
        '''
        Generates double gamma function in the domain of timestamps
        :Parameters:
        :param timestamps: array of evenly spaced values representing temporal samples.
            Optional. Default is array([0., 1., 2., ..., 24.]).
        :type timestamps: array of float (positive)
        :param tau_p: stands for the first peak delay, which is basically set to 6 sec. Default is 6.
        :type tau_p: int (positive)
        :param tau_d: stands for the second peak delay, which is basically set to 10 sec. Default is 10.
            Represents the delay of undershoot to response.
        :type tau_d: int (positive)
        :param amplitudeScalingFactor: A scaling factor for the amplitude.
            It is the amplitude ratio between the first and second peaks.
            It was set to 6 sec. as in typical fMRI studies.
            Default is 6.
        :type amplitudeScalingFactor: float (positive)
        :return: An array.
        :rtype: numpy.ndarray
        '''

        #Check parameters
        if type(timestamps) is not np.ndarray:
            msg = self.getClassName() + ':double_gamma_function: Unexpected parameter type for parameter ''timestamps''.'
            raise ValueError(msg)

        if type(tau_p) is not int:
            msg = self.getClassName() + ':double_gamma_function: Unexpected parameter type for parameter ''tau_p''.'
            raise ValueError(msg)
        if tau_p <= 0:
            msg = self.getClassName() + ':double_gamma_function: Unexpected parameter value for parameter ''tau_p''.'
            raise ValueError(msg)

        if type(tau_d) is not int:
            msg = self.getClassName() + ':double_gamma_function: Unexpected parameter type for parameter ''tau_d''.'
            raise ValueError(msg)
        if tau_d <= 0:
            msg = self.getClassName() + ':double_gamma_function: Unexpected parameter value for parameter ''tau_d''.'
            raise ValueError(msg)

        if type(amplitudeScalingFactor) is int:
            amplitudeScalingFactor = float(amplitudeScalingFactor)
        if type(amplitudeScalingFactor) is not float:
            msg = self.getClassName() + ':double_gamma_function: Unexpected parameter type for parameter ''amplitudeScalingFactor''.'
            raise ValueError(msg)
        if amplitudeScalingFactor <= 0:
            msg = self.getClassName() + ':double_gamma_function: Unexpected parameter value for parameter ''amplitudeScalingFactor''.'
            raise ValueError(msg)

        HRF = ( pow(timestamps, tau_p) * np.exp(-1 * timestamps) ) / math.factorial(tau_p)
        HRF = HRF - ( pow(timestamps, tau_p+tau_d) * np.exp(-1 * timestamps) ) / ( amplitudeScalingFactor * math.factorial(tau_p+tau_d) )

        return HRF
    #end double_gamma_function(self, timestamps = np.arange(25, dtype=float), tau_p=6, ... , amplitudeScalingFactor=6)


    def generateStimulusResult(self, boxCarList=list(), nSamples = 100, nChannels = 1, \
                                tau_p = 6, tau_d = 10, amplitudeScalingFactor = 6, \
                                enableHbO2Channels=np.ones(1, dtype=int), \
                                enableHHbChannels =np.ones(1, dtype=int), \
                                enableHbO2Blocks  =np.ones(1, dtype=int), \
                                enableHHbBlocks   =np.ones(1, dtype=int), boxcar_amp=[1], channel_amp=list[1]):

        '''
        Generates synthetic data for the stimulus whose times of occurrence are on the supplied boxcar
        :Parameters:
        :param boxCarList: List of tuples. Each tuple is a pair (xi, yi).
            (xi, yi) is an interval where the boxcar is equal to 1.
            0 <= xi, yi < nSamples/samplingRate, xi < yi.
            Default is the empty list.
        :type boxCarList: list
        :param nSamples: Number of temporal samples.
            Optional. Default is 1.
        :type nSamples: int (positive)
        :param nChannels: Number of channels.
            Optional. Default is 1.
        :type nChannels: int (positive)
        :param tau_p: stands for the first peak delay, which is basically set to 6 sec. Default is 6.
        :type tau_p: int (positive)
        :param tau_d: stands for the second peak delay, which is basically set to 10 sec. Default is 10.
            Represents the delay of undershoot to response.
        :type tau_d: int (positive)
        :param amplitudeScalingFactor: A scaling factor for the amplitude.
            It is the amplitude ratio between the first and second peaks.
            It was set to 6 sec. as in typical fMRI studies.
            Default is 6.
        :type amplitudeScalingFactor: float (positive)
        :param enableHbO2Channels: A vector whose length is nChannels. Each position contains an integer value: 1 or 0.
            The value 1 indicates that the corresponding channel has the HbO2 signal enabled, and 0 indicates otherwise.
            Default is array([1]). This array of 1´s is extended automatically, by the compiler, to the number of
            channels (columns) and the number of samples (rows) when the operation * (element-wise matrix multiplication)
            is applied.
        :type numpy.ndarray
        :param enableHHbChannels: A vector whose length is nChannels. Each position contains an integer value: 1 or 0.
            The value 1 indicates that the corresponding channel has the HHb signal enabled, and 0 indicates otherwise.
            Default is array([1]). This array of 1´s is extended automatically, by the compiler, to the number of
            channels (columns) and the number of samples (rows) when the operation * (element-wise matrix multiplication)
            is applied.
        :type numpy.ndarray
        :param enableHbO2Blocks: A vector whose length is nBlocks. Each position contains an integer value: 1 or 0.
            The value 1 indicates that the corresponding block has the HbO2 signal enabled, and 0 indicates otherwise.
            Default is array([1]). This array of 1´s is extended automatically, by the compiler, to the number of
            blocks (columns) and the number of samples (rows) when the operation * (element-wise matrix multiplication)   OJO
            is applied.
        :type numpy.ndarray
        :param enableHHbBlocks: A vector whose length is nBlocks. Each position contains an integer value: 1 or 0.
            The value 1 indicates that the corresponding block has the HHb signal enabled, and 0 indicates otherwise.
            Default is array([1]). This array of 1´s is extended automatically, by the compiler, to the number of
            blocks (columns) and the number of samples (rows) when the operation * (element-wise matrix multiplication)   OJO
            is applied.
        :type numpy.ndarray
        :return: A data tensor.
        :rtype: numpy.ndarray
        '''

        #Check parameters
        if type(boxCarList) is not list:
            msg = self.getClassName() + ':generateStimulusResult: Unexpected parameter type for parameter ''boxCarList''.'
            raise ValueError(msg)
        for elem in boxCarList:
            if type(elem) is not tuple:
                msg = self.getClassName() + ':generateStimulusResult: Unexpected parameter value for parameter ''boxCarList''.'
                raise ValueError(msg)
            if elem[0] < 0 or elem[0] >= self.nSamples/self.samplingRate:  # Ensure 0 <= xi < nSamples/samplingRate
                msg = self.getClassName() + ':generateStimulusResult: Unexpected parameter value for parameter ''boxCarList''.'
                raise ValueError(msg)
            if elem[1] < 0 or elem[1] >= self.nSamples/self.samplingRate:  # Ensure 0 <= yi < nSamples/samplingRate
                msg = self.getClassName() + ':generateStimulusResult: Unexpected parameter value for parameter ''boxCarList''.'
                raise ValueError(msg)
            if elem[0] >= elem[1]:  # Ensure xi < yi
                msg = self.getClassName() + ':generateStimulusResult: Unexpected parameter value for parameter ''boxCarList''.'
                raise ValueError(msg)

        if type(nSamples) is not int:
            msg = self.getClassName() + ':generateStimulusResult: Unexpected parameter type for parameter ''nSamples''.'
            raise ValueError(msg)
        if nSamples <= 0:
            msg = self.getClassName() + ':generateStimulusResult: Unexpected parameter value for parameter ''nSamples''.'
            raise ValueError(msg)

        if type(nChannels) is not int:
            msg = self.getClassName() + ':generateStimulusResult: Unexpected parameter type for parameter ''nChannels''.'
            raise ValueError(msg)
        if nChannels <= 0:
            msg = self.getClassName() + ':generateStimulusResult: Unexpected parameter value for parameter ''nChannels''.'
            raise ValueError(msg)

        if type(tau_p) is not int:
            msg = self.getClassName() + ':generateStimulusResult: Unexpected parameter type for parameter ''tau_p''.'
            raise ValueError(msg)
        if tau_p <= 0:
            msg = self.getClassName() + ':generateStimulusResult: Unexpected parameter value for parameter ''tau_p''.'
            raise ValueError(msg)

        if type(tau_d) is not int:
            msg = self.getClassName() + ':generateStimulusResult: Unexpected parameter type for parameter ''tau_d''.'
            raise ValueError(msg)
        if tau_d <= 0:
            msg = self.getClassName() + ':generateStimulusResult: Unexpected parameter value for parameter ''tau_d''.'
            raise ValueError(msg)

        if type(amplitudeScalingFactor) is int:
            amplitudeScalingFactor = float(amplitudeScalingFactor)
        if type(amplitudeScalingFactor) is not float:
            msg = self.getClassName() + ':generateStimulusResult: Unexpected parameter type for parameter ''amplitudeScalingFactor''.'
            raise ValueError(msg)
        if amplitudeScalingFactor <= 0:
            msg = self.getClassName() + ':generateStimulusResult: Unexpected parameter value for parameter ''amplitudeScalingFactor''.'
            raise ValueError(msg)

        if type(enableHbO2Channels) is list:
            enableHbO2Channels = np.array(enableHbO2Channels)
        if type(enableHbO2Channels) is not np.ndarray:
            msg = self.getClassName() + ':generateStimulusResult: Unexpected parameter type for parameter ''enableHbO2Channels''.'
            raise ValueError(msg)
        for i in range(0, len(enableHbO2Channels)):
            if enableHbO2Channels[i] != 1 and enableHbO2Channels[i] != 0:
                msg = self.getClassName() + ':generateStimulusResult: Unexpected parameter type for parameter ''enableHbO2Channels''.'
                raise ValueError(msg)

        if type(enableHHbChannels) is list:
            enableHHbChannels = np.array(enableHHbChannels)
        if type(enableHHbChannels) is not np.ndarray:
            msg = self.getClassName() + ':generateStimulusResult: Unexpected parameter type for parameter ''enableHHbChannels''.'
            raise ValueError(msg)
        for i in range(0, len(enableHHbChannels)):
            if enableHHbChannels[i] != 1 and enableHHbChannels[i] != 0:
                msg = self.getClassName() + ':generateStimulusResult: Unexpected parameter type for parameter ''enableHHbChannels''.'
                raise ValueError(msg)

        if type(enableHbO2Blocks) is list:
            enableHbO2Blocks = np.array(enableHbO2Blocks)
        if type(enableHbO2Blocks) is not np.ndarray:
            msg = self.getClassName() + ':generateStimulusResult: Unexpected parameter type for parameter ''enableHbO2Blocks''.'
            raise ValueError(msg)
        for i in range(0, len(enableHbO2Blocks)):
            if enableHbO2Blocks[i] != 1 and enableHbO2Blocks[i] != 0:
                msg = self.getClassName() + ':generateStimulusResult: Unexpected parameter type for parameter ''enableHbO2Blocks''.'
                raise ValueError(msg)

        if type(enableHHbBlocks) is list:
            enableHHbBlocks = np.array(enableHHbBlocks)
        if type(enableHHbBlocks) is not np.ndarray:
            msg = self.getClassName() + ':generateStimulusResult: Unexpected parameter type for parameter ''enableHHbBlocks''.'
            raise ValueError(msg)
        for i in range(0, len(enableHHbBlocks)):
            if enableHHbBlocks[i] != 1 and enableHHbBlocks[i] != 0:
                msg = self.getClassName() + ':generateStimulusResult: Unexpected parameter type for parameter ''enableHHbBlocks''.'
                raise ValueError(msg)
        boxCarListSet = list(set(boxCarList))  # Unique and sort elements
        nBlocks = len(boxCarListSet)
        
        if len(boxcar_amp) == 1:
            boxcar_amp = [boxcar_amp]*nBlocks

        if len(channel_amp) == 1:
            channel_amp = [channel_amp]*nChannels

        timestamps = np.arange(0, nSamples/self.samplingRate, 1/self.samplingRate, dtype = float)
        #print(timestamps)
        #print(self.samplingRate)

        ntimestamps = len(timestamps)
        boxCar      = np.zeros(ntimestamps) #creation of the boxcar with 0s
        boxCarHbO2  = np.zeros(ntimestamps) #creation of the boxcar for HbO2 with 0s
        boxCarHHb   = np.zeros(ntimestamps) #creation of the boxcar for HHb with 0s

        iBlock = 0
        for elem in boxCarList:
            i = np.searchsorted(timestamps, elem[0])
            j = np.searchsorted(timestamps, elem[1]) + 1
            boxCar[i:j] = 1
            if enableHbO2Blocks[iBlock] == 1:
                boxCarHbO2[i:j] = boxcar_amp[iBlock]
            if enableHHbBlocks[iBlock] == 1:
                boxCarHHb[i:j] = boxcar_amp[iBlock]
            iBlock+=1

        #plt.plot(boxCar, color='black')
        #plt.title('BoxCar')
        #plt.show()

        #plt.plot(boxCarHbO2, color='red')
        #plt.title('BoxCar with the enabled blocks for HbO2 signal')
        #plt.show()

        #plt.plot(boxCarHHb, color='blue')
        #plt.title('BoxCar with the enabled blocks for HHb signal')
        #plt.show()

        HRF = self.double_gamma_function(timestamps, tau_p, tau_d, amplitudeScalingFactor)

        # This is only for visualizing the doble gamma function
        #timestamps1 = np.arange(0, 25, 0.1, dtype=float)
        #HRF1 = self.double_gamma_function(timestamps1, tau_p, tau_d, amplitudeScalingFactor)
        #HRF2 = -1*(1/3)*self.double_gamma_function(timestamps1, tau_p, tau_d, amplitudeScalingFactor)
        #plt.plot(HRF1, color='red', label='Oxygenated')
        #plt.plot(HRF2, color='blue', label='Deoxygenated' )
        #plt.title('HRF')
        #plt.xlabel('Time [samples]')
        #plt.ylabel('HRF')
        #plt.yticks([0])
        #plt.legend()
        #plt.show()
        

        #HbO2 = np.convolve(boxCarHbO2, HRF)
        HbO2 = np.convolve(boxCarHbO2, HRF, mode='full')
        HbO2 = HbO2[0:2999]

        #plt.plot(HbO2, color='red')
        #plt.title('Result of the convolution of HRF and the BoxCar for HbO2 signal')
        #plt.show()

        HbO2 = HbO2.reshape(-1, 1) #Reshape to column vector
        HbO2 = np.tile(HbO2, nChannels)

        #HbO2forHHb = np.convolve(boxCarHHb, HRF)
        HbO2forHHb = np.convolve(boxCarHHb, HRF, mode='full')
        HbO2forHHb = HbO2forHHb[0:2999]

        #plt.plot(HbO2forHHb, color='blue')
        #plt.title('Result of the convolution of HRF and the BoxCar for HHb signal')
        #plt.show()

        HbO2forHHb = HbO2forHHb.reshape(-1, 1) #Reshape to column vector
        HbO2forHHb = np.tile(HbO2forHHb, nChannels)

        HHb = (-1/3) * HbO2forHHb

        synthData = np.zeros((nSamples, nChannels, 2)) #The synthetic data tensor

        #print(HbO2[0:nSamples, :])
        #print(HHb[0:nSamples, :])

        #print(enableHHbChannels)

        #print(HHb[0:nSamples, :] * enableHHbChannels)

        synthData[:, :, self.HBO2] = synthData[:, :, self.HBO2] + HbO2[0:nSamples, :] * enableHbO2Channels
        synthData[:, :, self.HHB]  = synthData[:, :, self.HHB]  + HHb[0:nSamples, :] * enableHHbChannels

        for j in range(nChannels):
            synthData[:,j,:]=channel_amp[j]*synthData[:,j,:]


        return synthData
    #end generateStimulusResult(self, boxCarList=list(), nSamples = 100, nChannels = 1, ... , enableHHbChannels = np.ones(1, dtype=int))


    def addGaussianNoise(self, channelsList=list(), initSample=0, endSample=-1):

        '''
        Adds Gaussian noise to the data tensor.
        The generated noise is added to the class :attr:`data`.
        :Parameters:
        :param channelsList: List of channels affected. Default is the empty list.
        :type channelsList: list
        :param initSample: Initial temporal sample. Default is 0.
        :type initSample: int (positive)
        :param endSample: Last temporal sample. A positive value
            explicitly indicates a sample. A value -1 indicates the last
            sample of :attr:`data`. If not -1, then the endSample must be
            greater than the initSample. Default is -1.
        :type endSample: int (positive or -1)
        :return: None
        :rtype: NoneType
        '''

        #Check parameters
        if type(channelsList) is not list:
            msg = self.getClassName() + ':addGaussianNoise: Unexpected parameter type for parameter ''channelList''.'
            raise ValueError(msg)
        for elem in channelsList:
            if type(elem) is not int:
                msg = self.getClassName() + ':addGaussianNoise: Unexpected parameter value for parameter ''channelList''.'
                raise ValueError(msg)
            if elem < 0 or elem >= self.nChannels:  # Ensure the nChannels exist
                msg = self.getClassName() + ':addGaussianNoise: Unexpected parameter value for parameter ''channelList''.'
                raise ValueError(msg)

        if type(initSample) is not int:
            msg = self.getClassName() + ':addGaussianNoise: Unexpected parameter type for parameter ''initSample''.'
            raise ValueError(msg)
        if initSample < 0 or initSample >= self.nSamples:  # Ensure the nSamples exist
            msg = self.getClassName() + ':addGaussianNoise: Unexpected parameter value for parameter ''initSample''.'
            raise ValueError(msg)

        if type(endSample) is not int:
            msg = self.getClassName() + ':addGaussianNoise: Unexpected parameter type for parameter ''endSample''.'
            raise ValueError(msg)
        if endSample < -1 or endSample >= self.nSamples:  # Ensure the nSamples exist
            msg = self.getClassName() + ':addGaussianNoise: Unexpected parameter value for parameter ''endSample''.'
            raise ValueError(msg)
        if endSample == -1:  # If -1, substitute by the maximum last sample
            endSample = self.nSamples - 1
        if endSample <= initSample:  # Ensure the endSample is posterior to the initSample
            msg = self.getClassName() + ':addGaussianNoise: Unexpected parameter value for parameter ''endSample''.'
            raise ValueError(msg)

        channelsList = list(set(channelsList))  # Unique and sort elements
        nChannels = len(channelsList)
        nSamples = endSample - initSample

        timestamps = np.arange(0, nSamples/self.samplingRate, \
                                  1/self.samplingRate, dtype = float)

        timestamps = timestamps.reshape(-1, 1) #Reshape to column vector
        timestamps = np.tile(timestamps,nChannels)

        noiseHbO2 = np.random.normal(0, 0.3, timestamps.shape)
        #noiseHbO2 = np.random.normal(0, 0.3, timestamps.shape)
        noiseHHb  = np.random.normal(0, 0.3, timestamps.shape)

        noiseHbO2_plot = np.random.normal(0, 0.3, timestamps.shape)

        #plt.plot(noiseHbO2_plot[0:nSamples,0], color='blue')
        #plt.title('Gaussian Noise')
        #plt.show()

        #plt.plot(noiseHHb[0:nSamples,0], color='blue')
        #plt.show()

        self.__data[0:nSamples,channelsList,0] = \
                self.__data[0:nSamples,channelsList,0] + noiseHbO2

        self.__data[0:nSamples,channelsList,1] = \
                self.__data[0:nSamples,channelsList,1] + noiseHHb

        return
    #end addGaussianNoise(self, channelsList=list(), initSample=0, endSample=-1)


    def addPhysiologicalNoise(self, channelsList=list(), initSample=0, endSample=-1, \
                               frequencyMean = 0.22, frequencySD = 0.07, \
                               frequencyResolutionStep = 0.01):
        '''
        Adds physiological noise to the data tensor.
        The generated noise is added to the class :attr:`data`.
        :Parameters:
        :param channelsList: List of channels affected. Default is the empty list.
        :type channelsList: list
        :param initSample: Initial temporal sample. Default is 0.
        :type initSample: int (positive)
        :param endSample: Last temporal sample. A positive value
            explicitly indicates a sample. A value -1 indicates the last
            sample of :attr:`data`. If not -1, then the endSample must be
            greater than the initSample. Default is -1.
        :type endSample: int (positive or -1)
        :param frequencyMean: The frequency mean that corresponds to the physiological noise
            Optional. Default is 0.22 (this is for the breathing rate noise.
            It could be the corresponding of any of the other physiological noises)
        :type frequencyMean: float (positive)
        :param frequencySD: The frequency standard deviation that corresponds to the physiological noise
            Optional. Default is 0.07 (this is for the breathing rate noise.
            It could be the corresponding of any of the other physiological noises)
        :type frequencySD: float (positive)
        :param frequencyResolutionStep: The step for generating evenly spaced values
            within the interval of frequencies of the noise to be simulated.
            Optional. Default is 0.01.
        :type frequencyResolutionStep: float (positive)
        :return: None
        :rtype: NoneType
        '''

        #Check parameters
        if type(channelsList) is not list:
            msg = self.getClassName() + ':addPhysiologicalNoise: Unexpected parameter type for parameter ''channelList''.'
            raise ValueError(msg)
        for elem in channelsList:
            if type(elem) is not int:
                msg = self.getClassName() + ':addPhysiologicalNoise: Unexpected parameter value for parameter ''channelList''.'
                raise ValueError(msg)
            if elem < 0 or elem >= self.nChannels:  # Ensure the nChannels exist
                msg = self.getClassName() + ':addPhysiologicalNoise: Unexpected parameter value for parameter ''channelList''.'
                raise ValueError(msg)

        if type(initSample) is not int:
            msg = self.getClassName() + ':addPhysiologicalNoise: Unexpected parameter type for parameter ''initSample''.'
            raise ValueError(msg)
        if initSample < 0 or initSample >= self.nSamples:  # Ensure the nSamples exist
            msg = self.getClassName() + ':addPhysiologicalNoise: Unexpected parameter value for parameter ''initSample''.'
            raise ValueError(msg)

        if type(endSample) is not int:
            msg = self.getClassName() + ':addPhysiologicalNoise: Unexpected parameter type for parameter ''endSample''.'
            raise ValueError(msg)
        if endSample < -1 or endSample >= self.nSamples:  # Ensure the nSamples exist
            msg = self.getClassName() + ':addPhysiologicalNoise: Unexpected parameter value for parameter ''endSample''.'
            raise ValueError(msg)
        if endSample == -1:  # If -1, substitute by the maximum last sample
            endSample = self.nSamples - 1
        if endSample <= initSample:  # Ensure the endSample is posterior to the initSample
            msg = self.getClassName() + ':addPhysiologicalNoise: Unexpected parameter value for parameter ''endSample''.'
            raise ValueError(msg)

        if type(frequencyMean) is not float:
            msg = self.getClassName() + ':addPhysiologicalNoise: Unexpected parameter type for parameter ''frequencyMean''.'
            raise ValueError(msg)
        if frequencyMean <= 0:
            msg = self.getClassName() + ':addPhysiologicalNoise: Unexpected parameter value for parameter ''frequencyMean''.'
            raise ValueError(msg)

        if type(frequencySD) is not float:
            msg = self.getClassName() + ':addPhysiologicalNoise: Unexpected parameter type for parameter ''frequencySD''.'
            raise ValueError(msg)
        if frequencySD <= 0:
            msg = self.getClassName() + ':addPhysiologicalNoise: Unexpected parameter value for parameter ''frequencySD''.'
            raise ValueError(msg)

        if type(frequencyResolutionStep) is not float:
            msg = self.getClassName() + ':addPhysiologicalNoise: Unexpected parameter type for parameter ''frequencyResolutionStep''.'
            raise ValueError(msg)
        if frequencyResolutionStep <= 0:
            msg = self.getClassName() + ':addPhysiologicalNoise: Unexpected parameter value for parameter ''frequencyResolutionStep''.'
            raise ValueError(msg)

        channelsList = list(set(channelsList))  # Unique and sort elements
        nChannels = len(channelsList)
        nSamples = endSample - initSample

        tmpData = np.zeros((nSamples, nChannels, 2)) #The temporal data tensor for saving the generated noise

        timestamps = np.arange(0, nSamples/self.samplingRate, 1/self.samplingRate, dtype = float)
        timestamps = timestamps.reshape(-1, 1) #Reshape to column vector
        timestamps = np.tile(timestamps,nChannels)

        frequencySet = np.arange(frequencyMean-2*frequencySD, \
                                 frequencyMean+2*frequencySD+frequencyResolutionStep, \
                                 frequencyResolutionStep, dtype = float)   # From paper (Elwell et al., 1999)
        amplitudeScalingFactor = 1   # estandarizada para la distribución tenga media 0 y desv 1 z-score
        for freq in frequencySet:
            #Amplitude. One random amplitude per channel
            A = amplitudeScalingFactor*np.random.rand(1,nChannels)
            A = np.tile(A,[nSamples,1])
            #Phase [rad]. One random phase per channel
            theta = 2* math.pi * np.random.rand(1,nChannels) - math.pi
            theta = np.tile(theta,[nSamples,1])
            #theta = 0
            #Generate the fundamental signal
            tmpSin = A * np.sin(2*math.pi*freq*timestamps+theta)
            #Elment-wise multiplication with the amplitude
                #NOTE: In python NumPy, a*b among ndarrays is the
                #element-wise product. For matrix multiplication, one
                #need to do np.matmul(a,b)
            tmpData[:,:,self.HBO2] = tmpData[:,:,self.HBO2] + tmpSin
            tmpData[:,:,self.HHB]  = tmpData[:,:,self.HHB]  + (-1/3)*tmpSin

        #plt.plot(tmpSin[0:nSamples,0], color='blue')
        #plt.show()

        #TODO: al tener la señal final se debe estandarizar z_score  eliminar la media y dividir por la desv. stand

        self.__data[0:nSamples,channelsList,:] = self.__data[0:nSamples,channelsList,:] + tmpData

        return
    #end addPhysiologicalNoise(self, channelsList=list(), initSample=0, ... , frequencyResolutionStep = 0.01)


    def addHeartRateNoise(self, channelsList=list(), initSample=0, endSample=-1, \
                          frequencyResolutionStep = 0.01):
        '''
        Adds noise of heart rate to the data tensor.
        The generated noise is added to the class :attr:`data`.
        :Parameters:
        :param channelsList: List of channels affected. Default is the empty list.
        :type channelsList: list
        :param initSample: Initial temporal sample. Default is 0.
        :type initSample: int (positive)
        :param endSample: Last temporal sample. A positive value
            explicitly indicates a sample. A value -1 indicates the last
            sample of :attr:`data`. If not -1, then the endSample must be
            greater than the initSample. Default is -1.
        :type endSample: int (positive or -1)
        :param frequencyResolutionStep: The step for generating evenly spaced values
            within the interval of frequencies of the noise to be simulated.
            Optional. Default is 0.01.
        :type frequencyResolutionStep: float (positive)
        :return: None
        :rtype: NoneType
        '''

        #Check parameters
        #No need to type check channelsList, initSample, endSample, and frequencyResolutionStep as
        #these are passed to method addPhysiologicalNoise.

        self.addPhysiologicalNoise(channelsList, initSample, endSample, \
                                  frequencyMean=1.08, frequencySD=0.16, \
                                  frequencyResolutionStep=0.01)  # From paper (Elwell et al., 1999)

        return
    #end addHeartRateNoise(self, channelsList=list(), initSample=0, ... , frequencyResolutionStep = 0.01)


    def addBreathingRateNoise(self, channelsList=list(), initSample=0, endSample=-1, \
                              frequencyResolutionStep = 0.01):
        '''
        Adds noise of breathing rate to the data tensor.
        The generated noise is added to the class :attr:`data`.
        :Parameters:
        :param channelsList: List of channels affected. Default is the empty list.
        :type channelsList: list
        :param initSample: Initial temporal sample. Default is 0.
        :type initSample: int (positive)
        :param endSample: Last temporal sample. A positive value
            explicitly indicates a sample. A value -1 indicates the last
            sample of :attr:`data`. If not -1, then the endSample must be
            greater than the initSample. Default is -1.
        :type endSample: int (positive or -1)
        :param frequencyResolutionStep: The step for generating evenly spaced values
            within the interval of frequencies of the noise to be simulated.
            Optional. Default is 0.01.
        :type frequencyResolutionStep: float (positive)
        :return: None
        :rtype: NoneType
        '''

        #Check parameters
        #No need to type check channelsList, initSample, endSample, and frequencyResolutionStep as
        #these are passed to method addPhysiologicalNoise.

        self.addPhysiologicalNoise(channelsList, initSample, endSample, \
                                  frequencyMean=0.22, frequencySD=0.07, \
                                  frequencyResolutionStep=0.01)  # From paper (Elwell et al., 1999)

        return
    #end addBreathingRateNoise(self, channelsList=list(), initSample=0, ... , frequencyResolutionStep = 0.01)


    def addVasomotionNoise(self, channelsList=list(), initSample=0, endSample=-1, \
                           frequencyResolutionStep = 0.01):
        '''
        Adds noise of vasomotion to the data tensor.
        The generated noise is added to the class :attr:`data`.
        :Parameters:
        :param channelsList: List of channels affected. Default is the empty list.
        :type channelsList: list
        :param initSample: Initial temporal sample. Default is 0.
        :type initSample: int (positive)
        :param endSample: Last temporal sample. A positive value
            explicitly indicates a sample. A value -1 indicates the last
            sample of :attr:`data`. If not -1, then the endSample must be
            greater than the initSample. Default is -1.
        :type endSample: int (positive or -1)
        :param frequencyResolutionStep: The step for generating evenly spaced values
            within the interval of frequencies of the noise to be simulated.
            Optional. Default is 0.01.
        :type frequencyResolutionStep: float (positive)
        :return: None
        :rtype: NoneType
        '''

        #Check parameters
        #No need to type check channelsList, initSample, endSample, and frequencyResolutionStep as
        #these are passed to method addPhysiologicalNoise.

        self.addPhysiologicalNoise(channelsList, initSample, endSample, frequencyMean=0.082, frequencySD=0.016, frequencyResolutionStep=0.01)  # From paper (Elwell et al., 1999)

        return
    #end addVasomotionNoise(self, channelsList=list(), initSample=0, ... , frequencyResolutionStep = 0.01)
    
    def import_distsVec(self):
        datDists1 = h5py.File('resting33.snirf','r')
        sourceArray1=np.array(datDists1.get('/nirs/probe/sourcePos2D'));
        detectorArray1=np.array(datDists1.get('/nirs/probe/detectorPos2D'));
        
        distances1 = np.empty((68,1))
        for i in range(69):
            if i > 0:
                sourceIndex = np.array(datDists1.get('/nirs/data1/measurementList'+str(i)+'/sourceIndex'));
                sourceIndex = sourceIndex.astype(int)
                detectorIndex = np.array(datDists1.get('/nirs/data1/measurementList'+str(i)+'/detectorIndex'));
                detectorIndex = detectorIndex.astype(int)
                distances1[i-1] = np.sqrt(np.sum(np.square(sourceArray1[sourceIndex-1,:]-detectorArray1[detectorIndex-1,:])))
        
        datDists2 = h5py.File('resting86.snirf','r')
        sourceArray2=np.array(datDists2.get('/nirs/probe/sourcePos2D'));
        detectorArray2=np.array(datDists2.get('/nirs/probe/detectorPos2D'));
        
        distances2 = np.empty((112,1))
        for i in range(113):
            if i > 0:
                sourceIndex = np.array(datDists2.get('/nirs/data1/measurementList'+str(i)+'/sourceIndex'));
                sourceIndex = sourceIndex.astype(int)
                detectorIndex = np.array(datDists2.get('/nirs/data1/measurementList'+str(i)+'/detectorIndex'));
                detectorIndex = detectorIndex.astype(int)
                distances2[i-1] = np.sqrt(np.sum(np.square(sourceArray2[sourceIndex-1,:]-detectorArray2[detectorIndex-1,:])))
            
        distsVecList =[distances1, distances2]
            
        return distsVecList
        
        
    
    def process_datums(self, dataMat, distsVec, ppf, dpf):
        #https://mail.nmr.mgh.harvard.edu/pipermail//homer-users/2006-July/000124.html
        numCols = dataMat.shape[1]
        extinctionCoeffs = np.array([[830,974,693.04],[690,276,2051.96]]) #https://omlc.org/spectra/hemoglobin/summary.html
        for n in range(numCols):
            currColHBO = np.array([dataMat[:,n,0]])
            currColHBB = np.array([dataMat[:,n,1]])
            #print(currColHBO.shape)
            #print(currColHBB.shape)
            meanHBO = np.mean(currColHBO)
            meanHBB = np.mean(currColHBB)
            currColHBO /= meanHBO
            currColHBB /= meanHBB
            currColHBO = np.log(currColHBO)
            currColHBB = np.log(currColHBB)
            currColHBO *= -1
            currColHBB *= -1
            currColHBO *=  6.25*distsVec[n]
            currColHBB *=  6.25*distsVec[n]
            OptDensMatT = np.concatenate((currColHBO,currColHBB),axis=0)
            #OptDensMatT = np.transpose(OptDensMat)
            #print(OptDensMatT.shape)
            Extinction = extinctionCoeffs[:,1:]
            ExtinctionT = np.transpose(Extinction)
            ExtinctionInv = np.matmul(np.matmul(ExtinctionT,Extinction),ExtinctionT)
            #print(ExtinctionInv.shape)
            HBO_HBR = np.matmul(ExtinctionInv,OptDensMatT)
            dataMat[:,n,0] = HBO_HBR[0,:]
            dataMat[:,n,1] = HBO_HBR[1,:]
        
        return dataMat
            
            
            
    
    def import_datums(self, distsVecList, nSamples=100):
        #np.set_printoptions(threshold=sys.maxsize)
        #nSamples = 3000
        print('nSamples', nSamples)
        #timestamps = np.arange(0, nSamples/self.samplingRate, 1/self.samplingRate, dtype = float)
        #ntimestamps = timestamps.shape[0]
        #print('timestamps', timestamps, ntimestamps)
        listo1 = [33, 34, 36, 37, 38, 39, 40, 41, 43, 44, 46, 47, 49, 51]
        shortchans1 = [0,34,3,37,6,40,11,45,16,50,21,55,26,60,31,65]
        listo2 = [86, 91, 92, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104]
        shortchans2 = [4,60,13,69,19,75,26,82,32,88,41,97,47,103,54,110]
        dists1 = distsVecList[0]
        dists1 = np.delete(dists1, shortchans1, 0)
        dhalf1= int(dists1.shape[0]/2)
        dists1 = dists1[0:dhalf1,:]
        
        dists2 = distsVecList[1]
        dists2 = np.delete(dists2, shortchans2, 0)
        dhalf2= int(dists2.shape[0]/2)
        dists2 = dists2[0:dhalf2,:]
        
        D = np.empty((nSamples,1,2))
        Added_counter = 0
        print("Dataset 1")
        print(Added_counter)
        for e in listo1:
            e_s = str(e)
            #print('subject'+e_s)
            dat=h5py.File('resting'+e_s+'.snirf','r')
            d=np.array(dat.get('/nirs/data1/dataTimeSeries'));
            #print(d.shape)
            d = np.delete(d, shortchans1, 1)
            
            l=int(d.shape[1])
            #print(d.shape)
            lhalf = int((l/2))
            #print(lhalf)
            nS = d.shape[0]
            #print(nS)
            d1 = d[:,0:lhalf]
            d2 = d[:,lhalf:]
            
            d = np.dstack((d2,d1))
            d = self.process_datums(d,dists1,ppf=1,dpf=1)
            newSampling = int(math.floor(50/self.samplingRate))
            #print("NEW SAMPLING",newSampling)
            #TODO roll-over sampling so rational floats can be accepted as newSampling values
            da = d[0::newSampling,:,:]
            db = d[1::newSampling,:,:]
            dc = d[2::newSampling,:,:]
            dd = d[3::newSampling,:,:]
            de = d[4::newSampling,:,:]
            #print(da)
            #print(db)
            #print(dc)
            #print(dd)
            #print(de)
            al = da.shape[0]
            bl = db.shape[0]
            cl = dc.shape[0]
            dl = dd.shape[0]
            el = de.shape[0]
            #print(al)
            #print(bl)
            #print(cl)
            #print(dl)
            #print(el)
            seq = [al,bl,cl,dl,el]
            things = [da,db,dc,dd,de]
            for i in range(5):
                ell = seq[i]
                daz = things[i]
                #print(ell)
                if ell>nSamples:
                    #print(ell, "enough samples")
                    excess = ell - nSamples
                    #print('excess',excess)
                    daz = daz[0:-excess,:,:]
                    #print('new array', daz.shape)
                    D = np.concatenate((D,daz),axis=1)
                    Added_counter += 1
                    print(Added_counter)
                    #print('D',D.shape)
                elif ell<nSamples:
                    continue
                    #print(ell, "NOT enough samples")
                else:
                    D = np.concatenate((D,daz),axis=1)
                    Added_counter += 1
                    print(Added_counter)
                    #print('D',D.shape)
        print("Dataset 2")
        for e in listo2:
        
            e_s = str(e)
            #print('subject'+e_s)
            dat=h5py.File('resting'+e_s+'.snirf','r')
            d=np.array(dat.get('/nirs/data1/dataTimeSeries'));
            #print(d.shape)
            d = np.delete(d, shortchans2, 1)
            l=int(d.shape[1])
            #print(d.shape)
            lhalf = int((l/2))
            #print(lhalf)
            nS = d.shape[0]
            #print(nS)
            d1 = d[:,0:lhalf]
            d2 = d[:,lhalf:]
            d = np.dstack((d2,d1))
            d = self.process_datums(d,dists2,ppf=1,dpf=1)
            newSampling = int(math.floor(50/self.samplingRate))
            #print("NEW SAMPLING",newSampling)
            #TODO roll-over sampling so rational floats can be accepted as newSampling values
            if nS < 30000:
                d = d[0:15000,:,:]
                da = d[0::newSampling,:,:]
                db = d[1::newSampling,:,:]
                dc = d[2::newSampling,:,:]
                dd = d[3::newSampling,:,:]
                de = d[4::newSampling,:,:]
                #print(da)
                #print(db)
                #print(dc)
                #print(dd)
                #print(de)
                al = da.shape[0]
                bl = db.shape[0]
                cl = dc.shape[0]
                dl = dd.shape[0]
                el = de.shape[0]
                #print(al)
                #print(bl)
                #print(cl)
                #print(dl)
                #print(el)
                seq = [al,bl,cl,dl,el]
                things = [da,db,dc,dd,de]
                for i in range(5):
                    ell = seq[i]
                    daz = things[i]
                    #print(ell)
                    if ell>nSamples:
                        #print(ell, "enough samples")
                        excess = ell - nSamples
                        #print('excess',excess)
                        daz = daz[0:-excess,:,:]
                        #print('new array', daz.shape)
                        D = np.concatenate((D,daz),axis=1)
                        Added_counter += 1
                        print(Added_counter)
                        #print('D',D.shape)
                    elif ell<nSamples:
                        continue
                        #print(ell, "NOT enough samples")
                    else:
                        D = np.concatenate((D,daz),axis=1)
                        Added_counter += 1
                        print(Added_counter)
                        #print('D',D.shape)
            else:
                g1 = d[0:15000,:,:]
                g2 = d[15000:30000,:,:]
                G = [g1,g2]
                for j in G:
                    ja = j[0::newSampling,:,:]
                    jb = j[1::newSampling,:,:]
                    jc = j[2::newSampling,:,:]
                    jd = j[3::newSampling,:,:]
                    je = j[4::newSampling,:,:]
                    #print(da)
                    #print(db)
                    #print(dc)
                    #print(dd)
                    #print(de)
                    al = ja.shape[0]
                    bl = jb.shape[0]
                    cl = jc.shape[0]
                    dl = jd.shape[0]
                    el = je.shape[0]
                    #print(al)
                    #print(bl)
                    #print(cl)
                    #print(dl)
                    #print(el)
                    seq = [al,bl,cl,dl,el]
                    things = [ja,jb,jc,jd,je]
                    for i in range(5):
                        ell = seq[i]
                        daz = things[i]
                        #print(ell)
                        if ell>nSamples:
                            #print(ell, "enough samples")
                            excess = ell - nSamples
                            #print('excess',excess)
                            daz = daz[0:-excess,:,:]
                            #print('new array', daz.shape)
                            D = np.concatenate((D,daz),axis=1)
                            Added_counter += 1
                            print(Added_counter)
                            #print('D',D.shape)
                        elif ell<nSamples:
                            continue
                            #print(ell, "NOT enough samples")
                        else:
                            D = np.concatenate((D,daz),axis=1)
                            Added_counter += 1
                            print(Added_counter)
                            #print('D',D.shape)

        print('D',D.shape)
        return D
    #end import_datums
        
        
    def addExperimentalNoise(self, imported_data, channelsList=list(),  initSample=0, endSample=-1, noise_ratio=1):
        
        channelsList = list(set(channelsList))  # Unique and sort elements
        nChannels = len(channelsList)
        
        if endSample == -1:  # If -1, substitute by the maximum last sample
           endSample = self.nSamples - 1
           
        #print(endSample)
        nSamplesIndex = endSample - initSample
        nSamples = nSamplesIndex + 1
        
        n = imported_data.shape[0]
        
        if n != nSamples:
            print('incorrectly sampled data')
            return
        
        m = imported_data.shape[1]
        sampled = np.random.randint(m, size = nChannels)
        #print(sampled)
        
        Noise_tensor = np.empty((nSamples,nChannels,2))
        scaledNoise_tensor = np.empty((nSamples,nChannels,2))
        
        for i in range(nChannels):
            Noise_tensor[:,i,:] = imported_data[:,sampled[i],:]
            
        #scaledNoise_tensor[:,:,0] = preprocessing.scale(Noise_tensor[:,:,0])
        #scaledNoise_tensor[:,:,1] = preprocessing.scale(Noise_tensor[:,:,1])
#         print("Noise_tensor")
#         print(Noise_tensor[1:5,:,1])
        
#         print("Small_Noise_tensor")
#         new_noise = noise_ratio*Noise_tensor
#         print(new_noise[1:5,:,1])
        
        self.__data[0:nSamples,channelsList,:] = self.__data[0:nSamples,channelsList,:] + noise_ratio*Noise_tensor
        
    #end addExperimentalNoise


    def execute(self, imported_datas=np.empty((3000,4,2)), Exertion = 0, boxVar=0, chanVar=0, type3 = 0, indv = 0, session = 0, Breath=0, Vaso=0, Heart=0, Gauss=0, Experi=0, Plot=0):
        '''
        Generates the synthetic fNIRS data from the properties
        information.
        This method calls :meth:`generateStimulusResult` for generating
        the new synthetic data.
        :return: A 3D data tensor
        :rtype: np.ndarray
        '''

        channelsList = list(range(0, self.nChannels))

        enableHbO2Channels = np.ones(self.nChannels, dtype=int) # every channel enabled to simulate  Oxy

        enableHHbChannels = np.ones(self.nChannels, dtype=int) # every channel enabled to simulate  Deoxy 

        boxCarList_OnsetDurations = [(35, 20), (105, 20), (175, 20), (245, 20)]


        boxCarList = list()
        for elem in boxCarList_OnsetDurations:
            boxCarList.append((elem[0], elem[0]+elem[1]))



        boxCarListSet = list(set(boxCarList))  # Unique and sort elements
        nBlocks = len(boxCarListSet)

        enableHbO2Blocks = np.ones(nBlocks, dtype=int) # all the blocks of the boxCar are enabled for the HbO2 signal

        enableHHbBlocks = np.ones(nBlocks, dtype=int) # all the blocks of the boxCar are enabled for the HHb signal
        
        Scores = np.array([[4,0],[0,2],[3,1],[4,0],[6,4],[5,1],[6,2],[3,1],[2,5],[4,1],[9,7],[8,4],[7,5],[5,4],[7,4],[9,6],[5,8],[9,5],[6,4],[10,3]])
        #if isHRF == 0:
        if type3 == 0:
            if Exertion == 2:
                if boxVar == 1:
                    bx1 = np.random.normal(1,0.3, 4)
                    bx1[bx1<0]=0
                    bx1=bx1.tolist()
                    boxcar_amp = bx1
                else:
                    boxcar_amp = [1]
            elif Exertion == 1:
                if boxVar == 1:
                    bx2 = np.random.normal(0.5,0.1, 4)
                    bx2[bx2<0]=0
                    bx2=bx2.tolist()
                    boxcar_amp = bx2
                else:
                    boxcar_amp = [0.5]
            else:
                boxcar_amp = [0]
        
        
        
            if chanVar == 1:
                ch1 = np.random.normal(1,0.1, 4)
                ch1[ch1<0]=0
                ch1=ch1.tolist()
                channel_amp = ch1
            else:
                channel_amp = [1]
        else:
            
            
            experts_dists_box = np.array([1,1,1,1])
            experts_dists_chan = np.array([1,0.5,0.5,1])
            novices_dists_box = np.array([1,1,1,1])
            novices_dists_chan = np.array([1,1.2,1.2,1])
            #print(novices_dists_box.shape)
            #print(novices_dists_chan.shape)
            Round_scores = Scores[:,session]
            Ind_scr = Round_scores[indv]

            a = np.random.normal(0,0.06)
            b = np.random.normal(0.1,0.06)
            c = np.random.normal(0.2,0.06)
            d = np.random.normal(0.3,0.06)
            A = np.array([a,b,c,d])
            #print(A.shape)

            e = np.random.normal(Ind_scr/10, 0.06)
            E = np.array([e, -e, -e, e])
            #print(E.shape)
            if indv<= 9:
                bx = np.add(novices_dists_box,A)
                boxcar_amp = bx.tolist()
                ch = np.add(novices_dists_chan,E)
                channel_amp = ch.tolist()
            else:
                bx = np.add(experts_dists_box,A)
                boxcar_amp = bx.tolist()
                ch = np.add(experts_dists_chan,E)
                channel_amp = ch.tolist()
        
        resetData = np.zeros((3000,4,2))
        
        self.data = resetData
        
        #if isHRF==0:
        self.addStimulusResult(channelsList, boxCarList,
                               initSample=0, endSample=-1,
                               tau_p=6, tau_d=10,
                               amplitudeScalingFactor=6,
                               enableHbO2Channels=enableHbO2Channels,
                               enableHHbChannels=enableHHbChannels,
                               enableHbO2Blocks=enableHbO2Blocks,
                               enableHHbBlocks=enableHHbBlocks, boxcar_amp = boxcar_amp, channel_amp=channel_amp)
                               

        # elif isHRF==1:
            # Breath=0 
            # Vaso=0 
            # Heart=0 
            # Gauss=0 
            # Experi=0 
            # Plot=0 
            # boxcar_amp = [0,0,0,0] 
            # channel_amp = [0,0,0,0]
            # baselin = np.zeros((350,1))
            # if Exertion == 0:
                # timestam = np.arange(0,35,0.1,dtype = float)
                # HRF1 = self.double_gamma_function(timestam, tau_p=6, tau_d=10, amplitudeScalingFactor=6)
                # HRF1 = np.transpose([HRF1])
                # HRF1 = HRF1*0
                # HRF1 = np.concatenate((baselin,HRF1))
                # HRF2 = -1/3*HRF1
                # oneChannel= np.dstack((HRF1,HRF2))
                # self.data = np.concatenate((oneChannel,oneChannel,oneChannel,oneChannel),axis=1)
            # elif Exertion == 1:
                # timestam = np.arange(0,35,0.1,dtype = float)
                # HRF1 = self.double_gamma_function(timestam, tau_p=6, tau_d=10, amplitudeScalingFactor=6)
                # HRF1 = np.transpose([HRF1])
                # HRF1 = HRF1*1/2
                # HRF1 = np.concatenate((baselin,HRF1))
                # HRF2 = -1/3*HRF1
                # oneChannel= np.dstack((HRF1,HRF2))
                # self.data = np.concatenate((oneChannel,oneChannel,oneChannel,oneChannel),axis=1)
            # elif Exertion == 2:
                # timestam = np.arange(0,35,0.1,dtype = float)
                # HRF1 = self.double_gamma_function(timestam, tau_p=6, tau_d=10, amplitudeScalingFactor=6)
                # HRF1 = np.transpose([HRF1])
                # HRF1 = np.concatenate((baselin,HRF1))
                # HRF2 = -1/3*HRF1
                # oneChannel= np.dstack((HRF1,HRF2))
                # self.data = np.concatenate((oneChannel,oneChannel,oneChannel,oneChannel),axis=1)
            

        #plotSyntheticfNIRS(self.data, title='Synthetic fNIRS', enableHbO2Channels=enableHbO2Channels, enableHHbChannels=enableHHbChannels)
        
        #if isHRF:
            # block2 = self.data[915:1665,:,:]
            # self.data = np.concatenate((block2,block2,block2,block2),axis=0)
            
        
        if Breath == 1:

            self.addBreathingRateNoise(channelsList, initSample=0, endSample=-1, frequencyResolutionStep = 0.01)
        

        #plotSyntheticfNIRS(self.data, title='Synthetic fNIRS + Breathing rate noise', enableHbO2Channels=enableHbO2Channels, enableHHbChannels=enableHHbChannels)
        
        if Heart == 1:

            self.addHeartRateNoise(channelsList, initSample=0, endSample=-1, frequencyResolutionStep = 0.01)

        #plotSyntheticfNIRS(self.data, title='Synthetic fNIRS + Noises: Breathing rate and Heart rate', enableHbO2Channels=enableHbO2Channels, enableHHbChannels=enableHHbChannels)
        
        if Vaso == 1:

            self.addVasomotionNoise(channelsList, initSample=0, endSample=-1, frequencyResolutionStep = 0.01)

        #plotSyntheticfNIRS(self.data, title='Synthetic fNIRS + Noises: Vasomotion', enableHbO2Channels=enableHbO2Channels, enableHHbChannels=enableHHbChannels)
        
        if Gauss ==1:

            self.addGaussianNoise(channelsList, initSample=0, endSample=-1)

        #plotSyntheticfNIRS(self.data, title='Synthetic fNIRS + Gaussian Noise', enableHbO2Channels=enableHbO2Channels, enableHHbChannels=enableHHbChannels)
        
        if Experi ==1:
        
            self.addExperimentalNoise(imported_datas, channelsList, initSample=0, endSample=-1, noise_ratio=3)
            
        if Plot ==1:
            if Experi==1:
                plotSyntheticfNIRS(self.data, title='SemiSynthetic fNIRS', enableHbO2Channels=enableHbO2Channels, enableHHbChannels=enableHHbChannels)

            else:

                plotSyntheticfNIRS(self.data, title='Synthetic fNIRS', enableHbO2Channels=enableHbO2Channels, enableHHbChannels=enableHHbChannels)

        #print(self.data)
        #print(self.data.shape)
        
        Outputs = [copy.deepcopy(self.data), boxcar_amp, channel_amp]

        return Outputs
    #end execute(self)



#class fNIRSSignalGenerator


def plotSyntheticfNIRS(tensor, title='', enableHbO2Channels=np.ones(1, dtype=int), enableHHbChannels=np.ones(1, dtype=int)):
    '''
    Quick rendering of the synthetic fNIRS data tensor.
    '''

    nChannels = tensor.shape[1]
    for iCh in range(0,nChannels):
        if enableHbO2Channels[iCh]:
            plt.plot(tensor[:,iCh,0]+20*iCh, color='red')
        if enableHHbChannels[iCh]:
            plt.plot(tensor[:,iCh,1]+20*iCh, color='blue')
    plt.title(title)
    plt.xlabel('Time [samples]')
    plt.ylabel('Channels [A.U.]')
    plt.show()

    return
#end plotSyntheticfNIRS(tensor)




def main(boxcar_amp = [1], channel_amp=[1]):
    # Specifying the channel location map for the EEG signal
    newId = 3
    newDescription = 'First New Config'
    newNChannels = 4
    newNOptodes = 4
    newChLocations = np.array([[1, 2, 0], [0, 1, 0], [2, 1, 0], [1, 0, 0]])
    newOptodesLocations = np.array([[0, 2, 0], [2, 2, 0], [0, 0, 0], [2, 0, 0]])
    newOptodesTypes = np.array([1, 2, 2, 1])  # Remember {0: Unknown, 1: Emission or source, 2: Detector}
    #newReferencePoints = dict({'Nz': np.array([0, -18.5, 0]), 'Iz': np.array([0, 18.5, 0]),
                               #'LPA': np.array([17.5, 0, 0]), 'RPA': np.array([-17.5, 0, 0]),
                               #'Cz': np.array([0, 0, 0])})
    newSurfacePositioningSystem = 'UI 10/20'
    newChSurfacePositions = tuple(('Fz', 'C3', 'C4', 'Cz'))
    newOptodesSurfacePositions = tuple(('FC5', 'CP3', 'FC6', 'CP4'))
    newChOptodeArrays = np.array([0, 0, 0, 0])
    newOptodesOptodeArrays = np.array([0, 0, 0, 0])
    newPairings = np.array([[0, 1], [0, 2], [3, 1], [3, 2]])

    NewChTopoArrangement = np.array([[1, 2, 0], [0, 1, 0], [2, 1, 0], [1, 0, 0]])
    NewOptodesTopoArrangement = np.array([[0, 2, 0], [2, 2, 0], [0, 0, 0], [2, 0, 0]])

    oaInfo = optodeArrayInfo(nChannels=newNChannels, nOptodes=newNOptodes, \
                            mode='HITACHI ETG-4000 2x2 optode array', typeOptodeArray='adult', \
                            chTopoArrangement=NewChTopoArrangement, \
                            optodesTopoArrangement=NewOptodesTopoArrangement)

    newOptodeArrays = np.array([oaInfo])
    
    #sg = fNIRSSignalGenerator(nSamples=6000, id=newId, description = newDescription, nChannels=newNChannels)

    sg = fNIRSSignalGenerator(nSamples = 3000, id = newId, description = newDescription,
                              nChannels = newNChannels, nOptodes  = newNOptodes,
                              chLocations = newChLocations, optodesLocations = newOptodesLocations,
                              optodesTypes = newOptodesTypes,
                              surfacePositioningSystem = newSurfacePositioningSystem,
                              chSurfacePositions = newChSurfacePositions,
                              optodesSurfacePositions = newOptodesSurfacePositions,
                              chOptodeArrays = newChOptodeArrays, optodesOptodeArrays = newOptodesOptodeArrays,
                              pairings = newPairings, optodeArrays = newOptodeArrays)


    #print(sg.samplingRate)
    # testing that constants can not receive other value
    #print("Valor de HBO2", sg.HBO2) # The value for HBO2 constant is 0
    #sg.HBO2 = 2
    #print("Nuevo Valor de HBO2", sg.HBO2)

    #print("Valor de HHB", sg.HHB) # The value for HHB constant is 1
    #sg.HHB = 3
    #print("Nuevo Valor de HHB", sg.HHB)

    #sg.showAttributesValues()
    im_dat = sg.import_datums(nSamples=3000)
    sg.execute(im_dat, boxcar_amp = boxcar_amp, channel_amp=channel_amp,  Breath=1, Vaso=1, Heart=1, Gauss=1, Experi=1, Plot=1)
    #print(sg.data)
    return
#end main()

def dataloading():
    newId = 3
    newDescription = 'First New Config'
    newNChannels = 4
    newNOptodes = 4
    newChLocations = np.array([[1, 2, 0], [0, 1, 0], [2, 1, 0], [1, 0, 0]])
    newOptodesLocations = np.array([[0, 2, 0], [2, 2, 0], [0, 0, 0], [2, 0, 0]])
    newOptodesTypes = np.array([1, 2, 2, 1])  # Remember {0: Unknown, 1: Emission or source, 2: Detector}
    #newReferencePoints = dict({'Nz': np.array([0, -18.5, 0]), 'Iz': np.array([0, 18.5, 0]),
                               #'LPA': np.array([17.5, 0, 0]), 'RPA': np.array([-17.5, 0, 0]),
                               #'Cz': np.array([0, 0, 0])})
    newSurfacePositioningSystem = 'UI 10/20'
    newChSurfacePositions = tuple(('Fz', 'C3', 'C4', 'Cz'))
    newOptodesSurfacePositions = tuple(('FC5', 'CP3', 'FC6', 'CP4'))
    newChOptodeArrays = np.array([0, 0, 0, 0])
    newOptodesOptodeArrays = np.array([0, 0, 0, 0])
    newPairings = np.array([[0, 1], [0, 2], [3, 1], [3, 2]])

    NewChTopoArrangement = np.array([[1, 2, 0], [0, 1, 0], [2, 1, 0], [1, 0, 0]])
    NewOptodesTopoArrangement = np.array([[0, 2, 0], [2, 2, 0], [0, 0, 0], [2, 0, 0]])

    oaInfo = optodeArrayInfo(nChannels=newNChannels, nOptodes=newNOptodes, \
                            mode='HITACHI ETG-4000 2x2 optode array', typeOptodeArray='adult', \
                            chTopoArrangement=NewChTopoArrangement, \
                            optodesTopoArrangement=NewOptodesTopoArrangement)

    newOptodeArrays = np.array([oaInfo])
    
    #sg = fNIRSSignalGenerator(nSamples=6000, id=newId, description = newDescription, nChannels=newNChannels)

    sg = fNIRSSignalGenerator(nSamples = 3000, id = newId, description = newDescription,
                              nChannels = newNChannels, nOptodes  = newNOptodes,
                              chLocations = newChLocations, optodesLocations = newOptodesLocations,
                              optodesTypes = newOptodesTypes,
                              surfacePositioningSystem = newSurfacePositioningSystem,
                              chSurfacePositions = newChSurfacePositions,
                              optodesSurfacePositions = newOptodesSurfacePositions,
                              chOptodeArrays = newChOptodeArrays, optodesOptodeArrays = newOptodesOptodeArrays,
                              pairings = newPairings, optodeArrays = newOptodeArrays)
    distsVecList = sg.import_distsVec()
    D = sg.import_datums(distsVecList,nSamples=3000)
    sg.execute(D, Exertion=2, Experi=1, Plot=0)
    
#end dataloading()


def score_dists(Scores=np.empty([20,2])):
    Round1 = np.empty([40,4])
    Round2 = np.empty([40,4])
    for j in range(2):
        for i in range(20):
            experts_dists_box = np.array([[1,1,1,1]])
            experts_dists_chan = np.array([[1,0.5,0.5,1]])
            novices_dists_box = np.array([[1,1,1,1]])
            novices_dists_chan = np.array([[1,1.2,1.2,1]])
            #print(novices_dists_box.shape)
            #print(novices_dists_chan.shape)
            Round_scores = Scores[:,j]
            Ind_scr = Round_scores[i]

            a = np.random.normal(0,0.06)
            b = np.random.normal(0.1,0.06)
            c = np.random.normal(0.2,0.06)
            d = np.random.normal(0.3,0.06)
            A = np.array([[a,b,c,d]])
            #print(A.shape)

            e = np.random.normal(Ind_scr/10, 0.06)
            E = np.array([[e, -e, -e, e]])
            #print(E.shape)
            if i<= 9:
                novices_dists_box = np.add(novices_dists_box,A)
                #print(novices_dists_box.shape)
                novices_dists_chan = np.add(novices_dists_chan,E)
                #print(novices_dists_chan.shape)
                if j==0:
                    Round1[2*i,:] = novices_dists_box
                    Round1[(2*i)+1,:] = novices_dists_chan
                else:
                    Round2[2*i,:] = novices_dists_box
                    Round2[(2*i)+1,:] = novices_dists_chan
            else:
                experts_dists_box = np.add(experts_dists_box,A)
                experts_dists_chan = np.add(experts_dists_chan,E)
                if j==0:
                    Round1[2*i,:] = experts_dists_box
                    Round1[(2*i)+1,:] = experts_dists_chan
                else:
                    Round2[2*i,:] = experts_dists_box
                    Round2[(2*i)+1,:] = experts_dists_chan
    List = [Round1, Round2]
    return Round1, Round2
            

                
Scores = np.array([[4,0],[0,2],[3,1],[4,0],[6,4],[5,1],[6,2],[3,1],[2,5],[4,1],[9,7],[8,4],[7,5],[5,4],[7,4],[9,6],[5,8],[9,5],[6,4],[10,3]])

BX1 = np.empty((10,4))
CH1 = np.empty((10,4))
BX2 = np.empty((10,4))
CH2 = np.empty((10,4))

if __name__ == '__main__':
    #bro()
    dataloading()
    #main([0.5],[1])
    #main([0],[1])
    #main([0.4260262, 0.7477428, 0.3427829, 0.8745029],[1])
    #main([1.2642387, 0.612275, 1.565875, 0.625262],[1])
    #main([0.5], [1.765250, 0.256938, 1.216929, 1.02362])
    #main([1], [1.73201, 0.221639, 1.22475, 1.05595])
    #main([1.265250, 0.556938, 0.916929, 1.02362],[1.33201, 0.721639, 1.22475, 1.05595])
    #Sessions = score_dists(Scores)
    #Session1 = Sessions[0]
    #Session2 = Sessions[1]
    #Session1 = np.array(Session1)
    #Session2 = np.array(Session2)
    #pd.DataFrame(Session1).to_csv("box_and_channel_distributions_session1.csv")
    #pd.DataFrame(Session2).to_csv("box_and_channel_distributions_session2.csv")
    #for k in range(20):
        #box = Session1[2*k,:]
        #chan = Session1[2*k+1,:]
        #box = box.tolist()
        #chan = chan.tolist()
        #M = main(box,chan)
        #M1 = M[:,:,0]
        #M2 = M[:,:,1]
        #pd.DataFrame(M1).to_csv("oxysession1_"+str(k)+".csv")
        #pd.DataFrame(M2).to_csv("deoxysession1_"+str(k)+".csv")

        #box2 = Session2[2*k,:]
        #chan2 = Session2[2*k+1,:]
        #box2 = box2.tolist()
        #chan2 = chan2.tolist()
        #M2 = main(box2,chan2)
        #M12 = M2[:,:,0]
        #M22 = M2[:,:,1]
        #pd.DataFrame(M12).to_csv("oxysession2_"+str(k)+".csv")
        #pd.DataFrame(M22).to_csv("deoxysession2_"+str(k)+".csv")
    #pd.DataFrame(Scores).to_csv("Task_Scores.csv")

    #for i in range(10):
        #print(i)
        #main()
        #bx1 = np.array([1,1,1,1])
        #bx1 = np.random.normal(1,0.3, 4)
        #bx1[bx1<0]=0
        #bx1=bx1.tolist()
        #ch1 = np.random.normal(1,0.1, 4)
        #ch1 = np.array([1,1,1,1])
        #ch1[ch1<0]=0
        #ch1=ch1.tolist()
        #print("bx1:", bx1)
        #print("ch1:", ch1)
        #c1 =main(boxcar_amp = bx1, channel_amp=ch1)
        #bx1 = np.array(bx1)
        #BX1[i,:]=bx1
        #ch1 = np.array(ch1)
        #CH1[i,:]=ch1
        #b1 = c1[:,:,1]
        #a1 = c1[:,:,0]
        #pd.DataFrame(a1).to_csv("synthoxyact_"+str(i)+".csv")
        #pd.DataFrame(b1).to_csv("sythdeoxyact_"+str(i)+".csv")


        #bx2 = np.array([0.5,0.5,0.5,0.5])      
        #bx2 = np.random.normal(0.5,0.1, 4)
        #bx2[bx2<0]=0
        #bx2=bx2.tolist()
        #ch2 = np.random.normal(1,0.1, 4)
        #ch2 = np.array([1,1,1,1])
        #ch2[ch2<0]=0
        #ch2=ch2.tolist()
        #print("bx2:", bx2)
        #print("ch2:", ch2)
        #c2 =main(boxcar_amp = bx2, channel_amp=ch2)
        #bx2 = np.array(bx2)
        #BX2[i,:]=bx2
        #ch2 = np.array(ch2)
        #CH2[i,:]=ch2
        #b2 = c2[:,:,1]
        #a2 = c2[:,:,0]
        #pd.DataFrame(a2).to_csv("synthoxyhalfact_"+str(i)+".csv")
        #pd.DataFrame(b2).to_csv("synthdeoxyhalfact_"+str(i)+".csv")

        #c3 =main(boxcar_amp = [0,0,0,0], channel_amp=[1,1,1,1])
        #b3 = c3[:,:,1]
        #a3 = c3[:,:,0]
        #pd.DataFrame(a3).to_csv("oxynact_"+str(i)+".csv")
        #pd.DataFrame(b3).to_csv("deoxynact_"+str(i)+".csv")

#pd.DataFrame(BX1).to_csv("ActRelative_Boxcar_Amplitudes.csv")
#pd.DataFrame(CH1).to_csv("ActRelative_Channel_Amplitudes.csv")
#pd.DataFrame(BX2).to_csv("HalfActRelative_Boxcar_Amplitudes.csv")
#pd.DataFrame(CH2).to_csv("HalfActRelative_Channel_Amplitudes.csv")

    


#print(multi_data)
#np.save('synth_test',multi_data)
    
