# File Name: dataImport.py
# Description: Define a class which contains all of the HPA axis data we have
# collected from the literature. The user can create an instance of the class
# for each data set they wish to use in their code
# Author: Christopher Parker
# Created: Wed Aug 17, 2022 | 02:17P EDT
# Last Modified: Mon Sep 12, 2022 | 04:58P EDT

import numpy as np

class data:
    """
    Imports HPA axis data sets into an object based on which set name is passed.
    Options for set names are:
        - Yehuda (Contains CORT data for MDD, PTSD and healthy control subjects)
        - Carroll (Contains ACTH & CORT data for high-cortisol MDD, low-cortisol
            MDD and healthy control subjects)
        - Golier (Contains ACTH & CORT data for trauma-exposed PTSD,
            trauma-exposed non-PTSD, and healthy control subjects)
        - Bremner (Contains CORT data for abused PTSD, non-abused PTSD, and
            healthy control subjects.)
        - Nelson (Contains ACTH & CORT data for melancholic MDD, atypical MDD,
            uncategorized MDD, and healthy control subjects undergoing
            Trier Social Stress Tests)

    Data sets are imported with time scale in hours by default. To change scale
    to minutes, add "minutes" as the second argument when creating an instance
    of the data class.

    For example:
        nelson = data("nelson", "minutes")
    """
    def __init__(self, dataSet="none", scale="hours"):
        if dataSet.lower() == "yehuda":
            self.yehuda(scale)
        elif dataSet.lower() == "carroll":
            self.carroll(scale)
        elif dataSet.lower() == "golier":
            self.golier(scale)
        elif dataSet.lower() == "bremner":
            self.bremner(scale)
        elif dataSet.lower() == "nelson":
            self.nelson(scale)
        elif dataSet.lower() == "patientf":
            self.patientF(scale)
        else:
            print("Default data set is TSST data in MDD patients from Nelson. To use a different data set, pass the name of the set when creating a new data object.")
            print("For example, data(\"carroll\").")
            print("\nUse help(data) in a Jupyter notebook for documentation including all data set options.")
            self.nelson(scale)


    def __smoothing(self, a, n = 5):
        idx = int((n - 1)/2)
        ret = np.cumsum(a, dtype = float)
        ret[idx + 1:-idx] = ret[n:] - ret[:-n]
        ret[idx] = ret[idx + 2]
        return ret[idx:-idx]/n


    def yehuda(self, scale):
        """
        Contains CORT data for MDD, PTSD and healthy control subjects in the following arrays:
            - controlCortisol
            - depressedCortisol
            - PTSDCortisol

        Each data set can also be retrieved in smoothed form, with each point averaged over the nearest
        5 data points.
        Simply add _smooth to the end of the variable name.

        For example:
            controlCortisol_smooth.
        """
        self.controlCortisol = np.genfromtxt("VeVaPy/data_files/Yehuda-1996-control-cortisol.txt")
        self.PTSDCortisol = np.genfromtxt("VeVaPy/data_files/Yehuda-1996-PTSD-cortisol.txt")
        self.depressedCortisol = np.genfromtxt("VeVaPy/data_files/Yehuda-1996-depressed-cortisol.txt")

        self.controlCortisol_smooth = self.controlCortisol
        self.PTSDCortisol_smooth = self.PTSDCortisol
        self.depressedCortisol_smooth = self.depressedCortisol

        self.controlCortisol_smooth[2:-2,1] = self.__smoothing(self.controlCortisol[:,1])
        self.PTSDCortisol_smooth[2:-2,1] = self.__smoothing(self.PTSDCortisol[:,1])
        self.depressedCortisol_smooth[2:-2,1] = self.__smoothing(self.depressedCortisol[:,1])

        self.controlCortisol = np.genfromtxt("VeVaPy/data_files/Yehuda-1996-control-cortisol.txt")
        self.PTSDCortisol = np.genfromtxt("VeVaPy/data_files/Yehuda-1996-PTSD-cortisol.txt")
        self.depressedCortisol = np.genfromtxt("VeVaPy/data_files/Yehuda-1996-depressed-cortisol.txt")

        # the data time scale is minutes, so convert it to hours when requested
        if scale.lower() == "hours":
            self.controlCortisol[:,0] = np.divide(self.controlCortisol[:,0], 60)
            self.PTSDCortisol[:,0] = np.divide(self.PTSDCortisol[:,0], 60)
            self.depressedCortisol[:,0] = np.divide(self.depressedCortisol[:,0], 60)

            self.controlCortisol_smooth[:,0] = np.divide(self.controlCortisol_smooth[:,0], 60)
            self.PTSDCortisol_smooth[:,0] = np.divide(self.PTSDCortisol_smooth[:,0], 60)
            self.depressedCortisol_smooth[:,0] = np.divide(self.depressedCortisol_smooth[:,0], 60)

    def carroll(self, scale):
        """
        Contains ACTH & CORT data for high-cortisol MDD, low-cortisol MDD, and
        healthy control subjects in the following arrays:
            - controlCortisol, controlACTH
            - HCDepressedCortisol, HCDepressedACTH
            - LCDepressedCortisol, LCDepressedACTH

        Each data set can also be retrieved in smoothed form, with each point
        averaged over the nearest 5 data points.
        Simply add _smooth to the end of the variable name.

        For example:
            controlCortisol_smooth

        Each data set can also be retrieved with the data points rearranged so
        that the data runs from 10AM to 10AM, which matches how the Yehuda data
        is arranged. This is useful for looking at data sets side by side to
        see how the circadian and ultradian rhythms compare.
        Simply add _rearr to the end of the variable name (but before _smooth,
        if present)

        For example:
            controlCortisol_rearr or controlCortisol_rearr_smooth
        """

        self.controlCortisol = np.genfromtxt("VeVaPy/data_files/Carroll-2007-controlGroupCortisol.txt", dtype = float)
        self.HCDepressedCortisol = np.genfromtxt("VeVaPy/data_files/Carroll-2007-HCDepressedCortisol.txt", dtype = float)
        self.LCDepressedCortisol = np.genfromtxt("VeVaPy/data_files/Carroll-2007-LCDepressedCortisol.txt", dtype = float)

        self.controlACTH = np.genfromtxt("VeVaPy/data_files/Carroll-2007-controlGroupACTH.txt", dtype = float)
        self.HCDepressedACTH = np.genfromtxt("VeVaPy/data_files/Carroll-2007-HCDepressedACTH.txt", dtype = float)
        self.LCDepressedACTH = np.genfromtxt("VeVaPy/data_files/Carroll-2007-LCDepressedACTH.txt", dtype = float)

        self.controlCortisol_rearr = np.vstack((self.controlCortisol[60:,:], self.controlCortisol[0:60,:]))
        self.HCDepressedCortisol_rearr = np.vstack((self.HCDepressedCortisol[60:,:], self.HCDepressedCortisol[0:60,:]))
        self.LCDepressedCortisol_rearr = np.vstack((self.LCDepressedCortisol[60:,:], self.LCDepressedCortisol[0:60,:]))

        self.controlACTH_rearr = np.vstack((self.controlACTH[60:,:], self.controlACTH[0:60,:]))
        self.HCDepressedACTH_rearr = np.vstack((self.HCDepressedACTH[60:,:], self.HCDepressedACTH[0:60,:]))
        self.LCDepressedACTH_rearr = np.vstack((self.LCDepressedACTH[60:,:], self.LCDepressedACTH[0:60,:]))

        self.controlCortisol_smooth = self.controlCortisol
        self.HCDepressedCortisol_smooth = self.HCDepressedCortisol
        self.LCDepressedCortisol_smooth = self.LCDepressedCortisol

        self.controlACTH_smooth = self.controlACTH
        self.HCDepressedACTH_smooth = self.HCDepressedACTH
        self.LCDepressedACTH_smooth = self.LCDepressedACTH

        self.controlCortisol_rearr_smooth = self.controlCortisol_rearr
        self.HCDepressedCortisol_rearr_smooth = self.HCDepressedCortisol_rearr
        self.LCDepressedCortisol_rearr_smooth = self.LCDepressedCortisol_rearr

        self.controlACTH_rearr_smooth = self.controlACTH_rearr
        self.HCDepressedACTH_rearr_smooth = self.HCDepressedACTH_rearr
        self.LCDepressedACTH_rearr_smooth = self.LCDepressedACTH_rearr

        self.controlCortisol_smooth[2:-2,1] = self.__smoothing(self.controlCortisol[:,1])
        self.HCDepressedCortisol_smooth[2:-2,1] = self.__smoothing(self.HCDepressedCortisol[:,1])
        self.LCDepressedCortisol_smooth[2:-2,1] = self.__smoothing(self.HCDepressedCortisol[:,1])

        self.controlACTH_smooth[2:-2,1] = self.__smoothing(self.controlACTH[:,1])
        self.HCDepressedACTH_smooth[2:-2,1] = self.__smoothing(self.HCDepressedACTH[:,1])
        self.LCDepressedACTH_smooth[2:-2,1] = self.__smoothing(self.LCDepressedACTH[:,1])

        self.controlCortisol_rearr_smooth[2:-2,1] = self.__smoothing(self.controlCortisol_rearr[:,1])
        self.HCDepressedCortisol_rearr_smooth[2:-2,1] = self.__smoothing(self.HCDepressedCortisol_rearr[:,1])
        self.LCDepressedCortisol_rearr_smooth[2:-2,1] = self.__smoothing(self.LCDepressedCortisol_rearr[:,1])

        self.controlACTH_rearr_smooth[2:-2,1] = self.__smoothing(self.controlACTH_rearr[:,1])
        self.HCDepressedACTH_rearr_smooth[2:-2,1] = self.__smoothing(self.HCDepressedACTH_rearr[:,1])
        self.LCDepressedACTH_rearr_smooth[2:-2,1] = self.__smoothing(self.LCDepressedACTH_rearr[:,1])

        self.controlCortisol = np.genfromtxt("VeVaPy/data_files/Carroll-2007-controlGroupCortisol.txt", dtype = float)
        self.HCDepressedCortisol = np.genfromtxt("VeVaPy/data_files/Carroll-2007-HCDepressedCortisol.txt", dtype = float)
        self.LCDepressedCortisol = np.genfromtxt("VeVaPy/data_files/Carroll-2007-LCDepressedCortisol.txt", dtype = float)

        self.controlACTH = np.genfromtxt("VeVaPy/data_files/Carroll-2007-controlGroupACTH.txt", dtype = float)
        self.HCDepressedACTH = np.genfromtxt("VeVaPy/data_files/Carroll-2007-HCDepressedACTH.txt", dtype = float)
        self.LCDepressedACTH = np.genfromtxt("VeVaPy/data_files/Carroll-2007-LCDepressedACTH.txt", dtype = float)

        self.controlCortisol_rearr = np.vstack((self.controlCortisol[60:,:], self.controlCortisol[0:60,:]))
        self.HCDepressedCortisol_rearr = np.vstack((self.HCDepressedCortisol[60:,:], self.HCDepressedCortisol[0:60,:]))
        self.LCDepressedCortisol_rearr = np.vstack((self.LCDepressedCortisol[60:,:], self.LCDepressedCortisol[0:60,:]))

        self.controlACTH_rearr = np.vstack((self.controlACTH[60:,:], self.controlACTH[0:60,:]))
        self.HCDepressedACTH_rearr = np.vstack((self.HCDepressedACTH[60:,:], self.HCDepressedACTH[0:60,:]))
        self.LCDepressedACTH_rearr = np.vstack((self.LCDepressedACTH[60:,:], self.LCDepressedACTH[0:60,:]))

        # change the time values of the rearranged sets so that 0 minutes is now 10AM
        #  like the non-rearranged sets
        for i in range(len(self.controlCortisol)):
            self.controlCortisol_rearr[i,0] = self.controlCortisol[i,0]
            self.controlACTH_rearr[i,0] = self.controlACTH[i,0]
            self.HCDepressedCortisol_rearr[i,0] = self.HCDepressedCortisol[i,0]
            self.HCDepressedACTH_rearr[i,0] = self.HCDepressedACTH[i,0]
            self.LCDepressedCortisol_rearr[i,0] = self.LCDepressedCortisol[i,0]
            self.LCDepressedACTH_rearr[i,0] = self.LCDepressedACTH[i,0]

            self.controlCortisol_rearr_smooth[i,0] = self.controlCortisol[i,0]
            self.controlACTH_rearr_smooth[i,0] = self.controlACTH[i,0]
            self.HCDepressedCortisol_rearr_smooth[i,0] = self.HCDepressedCortisol[i,0]
            self.HCDepressedACTH_rearr_smooth[i,0] = self.HCDepressedACTH[i,0]
            self.LCDepressedCortisol_rearr_smooth[i,0] = self.LCDepressedCortisol[i,0]
            self.LCDepressedACTH_rearr_smooth[i,0] = self.LCDepressedACTH[i,0]

        if scale.lower() == "hours":
            self.controlCortisol[:,0] = np.divide(self.controlCortisol[:,0], 60)
            self.controlACTH[:,0] = np.divide(self.controlACTH[:,0], 60)
            self.HCDepressedCortisol[:,0] = np.divide(self.HCDepressedCortisol[:,0], 60)
            self.HCDepressedACTH[:,0] = np.divide(self.HCDepressedACTH[:,0], 60)
            self.LCDepressedCortisol[:,0] = np.divide(self.LCDepressedCortisol[:,0], 60)
            self.LCDepressedACTH[:,0] = np.divide(self.LCDepressedACTH[:,0], 60)

            self.controlCortisol_smooth[:,0] = np.divide(self.controlCortisol_smooth[:,0], 60)
            self.controlACTH_smooth[:,0] = np.divide(self.controlACTH_smooth[:,0], 60)
            self.HCDepressedCortisol_smooth[:,0] = np.divide(self.HCDepressedCortisol_smooth[:,0], 60)
            self.HCDepressedACTH_smooth[:,0] = np.divide(self.HCDepressedACTH_smooth[:,0], 60)
            self.LCDepressedCortisol_smooth[:,0] = np.divide(self.LCDepressedCortisol_smooth[:,0], 60)
            self.LCDepressedACTH_smooth[:,0] = np.divide(self.LCDepressedACTH_smooth[:,0], 60)

            self.controlCortisol_rearr[:,0] = np.divide(self.controlCortisol_rearr[:,0], 60)
            self.controlACTH_rearr[:,0] = np.divide(self.controlACTH_rearr[:,0], 60)
            self.HCDepressedCortisol_rearr[:,0] = np.divide(self.HCDepressedCortisol_rearr[:,0], 60)
            self.HCDepressedACTH_rearr[:,0] = np.divide(self.HCDepressedACTH_rearr[:,0], 60)
            self.LCDepressedCortisol_rearr[:,0] = np.divide(self.LCDepressedCortisol_rearr[:,0], 60)
            self.LCDepressedACTH_rearr[:,0] = np.divide(self.LCDepressedACTH_rearr[:,0], 60)

            self.controlCortisol_rearr_smooth[:,0] = np.divide(self.controlCortisol_rearr_smooth[:,0], 60)
            self.controlACTH_rearr_smooth[:,0] = np.divide(self.controlACTH_rearr_smooth[:,0], 60)
            self.HCDepressedCortisol_rearr_smooth[:,0] = np.divide(self.HCDepressedCortisol_rearr_smooth[:,0], 60)
            self.HCDepressedACTH_rearr_smooth[:,0] = np.divide(self.HCDepressedACTH_rearr_smooth[:,0], 60)
            self.LCDepressedCortisol_rearr_smooth[:,0] = np.divide(self.LCDepressedCortisol_rearr_smooth[:,0], 60)
            self.LCDepressedACTH_rearr_smooth[:,0] = np.divide(self.LCDepressedACTH_rearr_smooth[:,0], 60)


    def golier(self, scale):
        """
        Contains ACTH & CORT data for trauma-exposed PTSD, trauma-exposed
        non-PTSD, and healthy control subjects in the following arrays:
            - PTSDCortisol, PTSDACTH
            - nonPTSDTraumaExposedCortisol, nonPTSDTraumaExposedACTH
            - nonPTSDNonExposedCortisol, nonPTSDNonExposedACTH

        Each data set can also be retrieved in smoothed form, with each point
        averaged over the nearest 5 data points.
        Simply add _smooth to the end of the variable name.

        For example:
            PTSDCortisol_smooth.

        Each data set can also be retrieved with the data points rearranged so
        that the data runs from 10AM to 10AM, which matches how the Yehuda data
        is arranged. This is useful for looking at data sets side by side to
        see how the circadian and ultradian rhythms compare.
        Simply add _rearr to the end of the variable name (but before _smooth,
        if present)

        For example:
            PTSDCortisol_rearr or PTSDCortisol_rearr_smooth
        """

        self.PTSDCortisol = np.genfromtxt("VeVaPy/data_files/Golier-2007-PTSD-cortisol.txt", dtype = float)
        self.nonPTSDTraumaExposedCortisol = np.genfromtxt("VeVaPy/data_files/Golier-2007-non-PTSD-trauma-exposed-cortisol.txt", dtype = float)
        self.nonPTSDNonExposedCortisol = np.genfromtxt("VeVaPy/data_files/Golier-2007-non-exposed-control-cortisol.txt", dtype = float)

        self.PTSDACTH = np.genfromtxt("VeVaPy/data_files/Golier-2007-PTSD-ACTH.txt", dtype = float)
        self.nonPTSDTraumaExposedACTH = np.genfromtxt("VeVaPy/data_files/Golier-2007-non-PTSD-trauma-exposed-ACTH.txt", dtype = float)
        self.nonPTSDNonExposedACTH = np.genfromtxt("VeVaPy/data_files/Golier-2007-non-exposed-control-ACTH.txt", dtype = float)

        # rearrange the arrays so that they start at 10AM like the Yehuda data sets
        self.PTSDCortisol_rearr = np.vstack((self.PTSDCortisol[7:,:], self.PTSDCortisol[0:7,:]))
        self.nonPTSDTraumaExposedCortisol_rearr = np.vstack((self.nonPTSDTraumaExposedCortisol[7:,:], self.nonPTSDTraumaExposedCortisol[0:7,:]))
        self.nonPTSDNonExposedCortisol_rearr = np.vstack((self.nonPTSDNonExposedCortisol[7:,:], self.nonPTSDNonExposedCortisol[0:7,:]))

        self.PTSDACTH_rearr = np.vstack((self.PTSDACTH[3:,:], self.PTSDACTH[0:3,:]))
        self.nonPTSDTraumaExposedACTH_rearr = np.vstack((self.nonPTSDTraumaExposedACTH[3:,:], self.nonPTSDTraumaExposedACTH[0:3,:]))
        self.nonPTSDNonExposedACTH_rearr = np.vstack((self.nonPTSDNonExposedACTH[3:,:], self.nonPTSDNonExposedACTH[0:3,:]))

        # create the smoothed arrays
        self.PTSDCortisol_smooth = self.PTSDCortisol
        self.nonPTSDTraumaExposedCortisol_smooth = self.nonPTSDTraumaExposedCortisol
        self.nonPTSDNonExposedCortisol_smooth = self.nonPTSDNonExposedCortisol
        self.PTSDACTH_smooth = self.PTSDACTH
        self.nonPTSDTraumaExposedACTH_smooth = self.nonPTSDTraumaExposedACTH
        self.nonPTSDNonExposedACTH_smooth = self.nonPTSDNonExposedACTH

        self.PTSDCortisol_smooth[2:-2,1] = self.__smoothing(self.PTSDCortisol[:,1])
        self.nonPTSDTraumaExposedCortisol_smooth[2:-2,1] = self.__smoothing(self.nonPTSDTraumaExposedCortisol[:,1])
        self.nonPTSDNonExposedCortisol_smooth[2:-2,1] = self.__smoothing(self.nonPTSDNonExposedCortisol[:,1])

        self.PTSDACTH_smooth[2:-2,1] = self.__smoothing(self.PTSDACTH[:,1])
        self.nonPTSDTraumaExposedACTH_smooth[2:-2,1] = self.__smoothing(self.nonPTSDTraumaExposedACTH[:,1])
        self.nonPTSDNonExposedACTH_smooth[2:-2,1] = self.__smoothing(self.nonPTSDNonExposedACTH[:,1])

        self.PTSDCortisol_rearr_smooth = self.PTSDCortisol_rearr
        self.nonPTSDTraumaExposedCortisol_rearr_smooth = self.nonPTSDTraumaExposedCortisol_rearr
        self.nonPTSDNonExposedCortisol_rearr_smooth = self.nonPTSDNonExposedCortisol_rearr
        self.PTSDACTH_rearr_smooth = self.PTSDACTH_rearr
        self.nonPTSDTraumaExposedACTH_rearr_smooth = self.nonPTSDTraumaExposedACTH_rearr
        self.nonPTSDNonExposedACTH_rearr_smooth = self.nonPTSDNonExposedACTH_rearr

        self.PTSDCortisol_rearr_smooth[2:-2,1] = self.__smoothing(self.PTSDCortisol_rearr[:,1])
        self.nonPTSDTraumaExposedCortisol_rearr_smooth[2:-2,1] = self.__smoothing(self.nonPTSDTraumaExposedCortisol_rearr[:,1])
        self.nonPTSDNonExposedCortisol_rearr_smooth[2:-2,1] = self.__smoothing(self.nonPTSDNonExposedCortisol_rearr[:,1])

        self.PTSDACTH_rearr_smooth[2:-2,1] = self.__smoothing(self.PTSDACTH_rearr[:,1])
        self.nonPTSDTraumaExposedACTH_rearr_smooth[2:-2,1] = self.__smoothing(self.nonPTSDTraumaExposedACTH_rearr[:,1])
        self.nonPTSDNonExposedACTH_rearr_smooth[2:-2,1] = self.__smoothing(self.nonPTSDNonExposedACTH_rearr[:,1])

        # re-run the genfromtxt() commands because the smoothing overwrites the non-smoothed
        #  arrays also, for some reason
        self.PTSDCortisol = np.genfromtxt("VeVaPy/data_files/Golier-2007-PTSD-cortisol.txt", dtype = float)
        self.nonPTSDTraumaExposedCortisol = np.genfromtxt("VeVaPy/data_files/Golier-2007-non-PTSD-trauma-exposed-cortisol.txt", dtype = float)
        self.nonPTSDNonExposedCortisol = np.genfromtxt("VeVaPy/data_files/Golier-2007-non-exposed-control-cortisol.txt", dtype = float)

        self.PTSDACTH = np.genfromtxt("VeVaPy/data_files/Golier-2007-PTSD-ACTH.txt", dtype = float)
        self.nonPTSDTraumaExposedACTH = np.genfromtxt("VeVaPy/data_files/Golier-2007-non-PTSD-trauma-exposed-ACTH.txt", dtype = float)
        self.nonPTSDNonExposedACTH = np.genfromtxt("VeVaPy/data_files/Golier-2007-non-exposed-control-ACTH.txt", dtype = float)

        # rearrange the arrays so that they start at 10AM like the Yehuda data sets
        self.PTSDCortisol_rearr = np.vstack((self.PTSDCortisol[7:,:], self.PTSDCortisol[0:7,:]))
        self.nonPTSDTraumaExposedCortisol_rearr = np.vstack((self.nonPTSDTraumaExposedCortisol[7:,:], self.nonPTSDTraumaExposedCortisol[0:7,:]))
        self.nonPTSDNonExposedCortisol_rearr = np.vstack((self.nonPTSDNonExposedCortisol[7:,:], self.nonPTSDNonExposedCortisol[0:7,:]))

        self.PTSDACTH_rearr = np.vstack((self.PTSDACTH[3:,:], self.PTSDACTH[0:3,:]))
        self.nonPTSDTraumaExposedACTH_rearr = np.vstack((self.nonPTSDTraumaExposedACTH[3:,:], self.nonPTSDTraumaExposedACTH[0:3,:]))
        self.nonPTSDNonExposedACTH_rearr = np.vstack((self.nonPTSDNonExposedACTH[3:,:], self.nonPTSDNonExposedACTH[0:3,:]))

        # change the time values of the rearranged sets so that 0 minutes is now 10AM
        #  like the non-rearranged sets
        for i in range(len(self.PTSDCortisol[:,0])):
            self.PTSDCortisol_rearr[i,0] = self.PTSDCortisol[i,0]
            self.PTSDCortisol_rearr_smooth[i,0] = self.PTSDCortisol[i,0]
            self.nonPTSDTraumaExposedCortisol_rearr[i,0] = self.nonPTSDTraumaExposedCortisol[i,0]
            self.nonPTSDTraumaExposedCortisol_rearr_smooth[i,0] = self.nonPTSDTraumaExposedCortisol[i,0]
            self.nonPTSDNonExposedCortisol_rearr[i,0] = self.nonPTSDNonExposedCortisol[i,0]
            self.nonPTSDNonExposedCortisol_rearr_smooth[i,0] = self.nonPTSDNonExposedCortisol[i,0]

        for i in range(len(self.PTSDACTH[:,0])):
            self.PTSDACTH_rearr[i,0] = self.PTSDACTH[i,0]
            self.PTSDACTH_rearr_smooth[i,0] = self.PTSDACTH[i,0]
            self.nonPTSDTraumaExposedACTH_rearr[i,0] = self.nonPTSDTraumaExposedACTH[i,0]
            self.nonPTSDTraumaExposedACTH_rearr_smooth[i,0] = self.nonPTSDTraumaExposedACTH[i,0]
            self.nonPTSDNonExposedACTH_rearr[i,0] = self.nonPTSDNonExposedACTH[i,0]
            self.nonPTSDNonExposedACTH_rearr_smooth[i,0] = self.nonPTSDNonExposedACTH[i,0]

        if scale.lower() == "minutes":
            self.PTSDCortisol[:,0] = np.multiply(self.PTSDCortisol[:,0], 60)
            self.PTSDACTH[:,0] = np.multiply(self.PTSDACTH[:,0], 60)
            self.nonPTSDTraumaExposedCortisol[:,0] = np.multiply(self.nonPTSDTraumaExposedCortisol[:,0], 60)
            self.nonPTSDTraumaExposedACTH[:,0] = np.multiply(self.nonPTSDTraumaExposedACTH[:,0], 60)
            self.nonPTSDNonExposedCortisol[:,0] = np.multiply(self.nonPTSDNonExposedCortisol[:,0], 60)
            self.nonPTSDNonExposedACTH[:,0] = np.multiply(self.nonPTSDNonExposedACTH[:,0], 60)

            self.PTSDCortisol_smooth[:,0] = np.multiply(self.PTSDCortisol_smooth[:,0], 60)
            self.PTSDACTH_smooth[:,0] = np.multiply(self.PTSDACTH_smooth[:,0], 60)
            self.nonPTSDTraumaExposedCortisol_smooth[:,0] = np.multiply(self.nonPTSDTraumaExposedCortisol_smooth[:,0], 60)
            self.nonPTSDTraumaExposedACTH_smooth[:,0] = np.multiply(self.nonPTSDTraumaExposedACTH_smooth[:,0], 60)
            self.nonPTSDNonExposedCortisol_smooth[:,0] = np.multiply(self.nonPTSDNonExposedCortisol_smooth[:,0], 60)
            self.nonPTSDNonExposedACTH_smooth[:,0] = np.multiply(self.nonPTSDNonExposedACTH_smooth[:,0], 60)

            self.PTSDCortisol_rearr[:,0] = np.multiply(self.PTSDCortisol_rearr[:,0], 60)
            self.PTSDACTH_rearr[:,0] = np.multiply(self.PTSDACTH_rearr[:,0], 60)
            self.nonPTSDTraumaExposedCortisol_rearr[:,0] = np.multiply(self.nonPTSDTraumaExposedCortisol_rearr[:,0], 60)
            self.nonPTSDTraumaExposedACTH_rearr[:,0] = np.multiply(self.nonPTSDTraumaExposedACTH_rearr[:,0], 60)
            self.nonPTSDNonExposedCortisol_rearr[:,0] = np.multiply(self.nonPTSDNonExposedCortisol_rearr[:,0], 60)
            self.nonPTSDNonExposedACTH_rearr[:,0] = np.multiply(self.nonPTSDNonExposedACTH_rearr[:,0], 60)

            self.PTSDCortisol_rearr_smooth[:,0] = np.multiply(self.PTSDCortisol_rearr_smooth[:,0], 60)
            self.PTSDACTH_rearr_smooth[:,0] = np.multiply(self.PTSDACTH_rearr_smooth[:,0], 60)
            self.nonPTSDTraumaExposedCortisol_rearr_smooth[:,0] = np.multiply(self.nonPTSDTraumaExposedCortisol_rearr_smooth[:,0], 60)
            self.nonPTSDTraumaExposedACTH_rearr_smooth[:,0] = np.multiply(self.nonPTSDTraumaExposedACTH_rearr_smooth[:,0], 60)
            self.nonPTSDNonExposedCortisol_rearr_smooth[:,0] = np.multiply(self.nonPTSDNonExposedCortisol_rearr_smooth[:,0], 60)
            self.nonPTSDNonExposedACTH_rearr_smooth[:,0] = np.multiply(self.nonPTSDNonExposedACTH_rearr_smooth[:,0], 60)


    def bremner(self, scale):
        """
        Contains CORT data for high-cortisol MDD, low-cortisol MDD, and healthy
        control subjects in the following arrays:
            - abusedPTSDCortisol
            - nonAbusedPTSDCortisol
            - nonAbusedNonPTSDCortisol

        Each data set can also be retrieved in smoothed form, with each point
        averaged over the nearest 5 data points.
        Simply add _smooth to the end of the variable name.

        For example:
            abusedPTSDCortisol_smooth

        Each data set can also be retrieved with the data points rearranged so
        that the data runs from 10AM to 10AM, which matches how the Yehuda data
        is arranged. This is useful for looking at data sets side by side to
        see how the circadian and ultradian rhythms compare.
        Simply add _rearr to the end of the variable name (but before _smooth,
        if present)

        For example:
            abusedPTSDCortisol_rearr or abusedPTSDCortisol_rearr_smooth
        """

        self.abusedPTSDCortisol = np.genfromtxt("VeVaPy/data_files/Bremner-2007-abused-PTSD-cortisol.txt", dtype = float)
        self.nonAbusedPTSDCortisol = np.genfromtxt("VeVaPy/data_files/Bremner-2007-non-abused-PTSD-cortisol.txt", dtype = float)
        self.nonAbusedNonPTSDCortisol = np.genfromtxt("VeVaPy/data_files/Bremner-2007-non-abused-non-PTSD-cortisol.txt", dtype = float)

        # rearrange the data so that we start at 10AM like the Yehuda data
        self.abusedPTSDCortisol_rearr = np.vstack((self.abusedPTSDCortisol[68:,:], self.abusedPTSDCortisol[0:68,:]))
        self.nonAbusedPTSDCortisol_rearr = np.vstack((self.nonAbusedPTSDCortisol[68:,:], self.nonAbusedPTSDCortisol[0:68,:]))
        self.nonAbusedNonPTSDCortisol_rearr = np.vstack((self.nonAbusedNonPTSDCortisol[68:,:], self.nonAbusedNonPTSDCortisol[0:68,:]))

        # create the smoothed arrays
        self.abusedPTSDCortisol_smooth = self.abusedPTSDCortisol
        self.abusedPTSDCortisol_rearr_smooth = self.abusedPTSDCortisol_rearr
        self.nonAbusedPTSDCortisol_smooth = self.nonAbusedPTSDCortisol
        self.nonAbusedPTSDCortisol_rearr_smooth = self.nonAbusedPTSDCortisol_rearr
        self.nonAbusedNonPTSDCortisol_smooth = self.nonAbusedNonPTSDCortisol
        self.nonAbusedNonPTSDCortisol_rearr_smooth = self.nonAbusedNonPTSDCortisol_rearr

        self.abusedPTSDCortisol_smooth[2:-2,1] = self.__smoothing(self.abusedPTSDCortisol[:,1])
        self.abusedPTSDCortisol_rearr_smooth[2:-2,1] = self.__smoothing(self.abusedPTSDCortisol_rearr[:,1])
        self.nonAbusedPTSDCortisol_smooth[2:-2,1] = self.__smoothing(self.nonAbusedPTSDCortisol[:,1])
        self.nonAbusedPTSDCortisol_rearr_smooth[2:-2,1] = self.__smoothing(self.nonAbusedPTSDCortisol_rearr[:,1])
        self.nonAbusedNonPTSDCortisol_smooth[2:-2,1] = self.__smoothing(self.nonAbusedNonPTSDCortisol[:,1])
        self.nonAbusedNonPTSDCortisol_rearr_smooth[2:-2,1] = self.__smoothing(self.nonAbusedNonPTSDCortisol_rearr[:,1])

        # re-run the genfromtxt() commands because the smoothing overwrites the non-smoothed
        #  arrays for some reason
        self.abusedPTSDCortisol = np.genfromtxt("VeVaPy/data_files/Bremner-2007-abused-PTSD-cortisol.txt", dtype = float)
        self.nonAbusedPTSDCortisol = np.genfromtxt("VeVaPy/data_files/Bremner-2007-non-abused-PTSD-cortisol.txt", dtype = float)
        self.nonAbusedNonPTSDCortisol = np.genfromtxt("VeVaPy/data_files/Bremner-2007-non-abused-non-PTSD-cortisol.txt", dtype = float)

        # rearrange the data so that we start at 10AM like the Yehuda data
        self.abusedPTSDCortisol_rearr = np.vstack((self.abusedPTSDCortisol[68:,:], self.abusedPTSDCortisol[0:68,:]))
        self.nonAbusedPTSDCortisol_rearr = np.vstack((self.nonAbusedPTSDCortisol[68:,:], self.nonAbusedPTSDCortisol[0:68,:]))
        self.nonAbusedNonPTSDCortisol_rearr = np.vstack((self.nonAbusedNonPTSDCortisol[68:,:], self.nonAbusedNonPTSDCortisol[0:68,:]))

        # change the time steps of the rearranged arrays so that we start at 0
        for i in range(len(self.abusedPTSDCortisol[:,0])):
            self.abusedPTSDCortisol_rearr[i,0] = self.abusedPTSDCortisol[i,0]
            self.abusedPTSDCortisol_rearr_smooth[i,0] = self.abusedPTSDCortisol[i,0]
            self.nonAbusedPTSDCortisol_rearr[i,0] = self.nonAbusedPTSDCortisol[i,0]
            self.nonAbusedPTSDCortisol_rearr_smooth[i,0] = self.nonAbusedPTSDCortisol[i,0]
            self.nonAbusedNonPTSDCortisol_rearr[i,0] = self.nonAbusedNonPTSDCortisol[i,0]
            self.nonAbusedNonPTSDCortisol_rearr_smooth[i,0] = self.nonAbusedNonPTSDCortisol[i,0]

        if scale.lower() == "minutes":
            self.abusedPTSDCortisol[:,0] = np.multiply(self.abusedPTSDCortisol[:,0], 60)
            self.nonAbusedPTSDCortisol[:,0] = np.multiply(self.nonAbusedPTSDCortisol[:,0], 60)
            self.nonAbusedNonPTSDCortisol[:,0] = np.multiply(self.nonAbusedNonPTSDCortisol[:,0], 60)

            self.abusedPTSDCortisol_smooth[:,0] = np.multiply(self.abusedPTSDCortisol_smooth[:,0], 60)
            self.nonAbusedPTSDCortisol_smooth[:,0] = np.multiply(self.nonAbusedPTSDCortisol_smooth[:,0], 60)
            self.nonAbusedNonPTSDCortisol_smooth[:,0] = np.multiply(self.nonAbusedNonPTSDCortisol_smooth[:,0], 60)

            self.abusedPTSDCortisol_rearr[:,0] = np.multiply(self.abusedPTSDCortisol_rearr[:,0], 60)
            self.nonAbusedPTSDCortisol_rearr[:,0] = np.multiply(self.nonAbusedPTSDCortisol_rearr[:,0], 60)
            self.nonAbusedNonPTSDCortisol_rearr[:,0] = np.multiply(self.nonAbusedNonPTSDCortisol_rearr[:,0], 60)

            self.abusedPTSDCortisol_rearr_smooth[:,0] = np.multiply(self.abusedPTSDCortisol_rearr_smooth[:,0], 60)
            self.nonAbusedPTSDCortisol_rearr_smooth[:,0] = np.multiply(self.nonAbusedPTSDCortisol_rearr_smooth[:,0], 60)
            self.nonAbusedNonPTSDCortisol_rearr_smooth[:,0] = np.multiply(self.nonAbusedNonPTSDCortisol_rearr_smooth[:,0], 60)

    def nelson(self, scale):
        """
        The data in these sets is over a 2 hour and 20 minute period, and the
        patients underwent Trier Social Stress Tests at the 30 minute mark. As
        such, the data for most patients contains a pronounced spike in ACTH &
        CORT at that point and then returns to baseline afterwards.

        Contains mean ACTH & CORT data for melancholic MDD, atypical MDD,
        uncategorized MDD and healthy control subjects in the following arrays:
            - melancholicCortisol, melancholicACTH
            - atypicalCortisol, atypicalACTH
            - uncategorizedCortisol, uncategorizedACTH
            - healthyCortisol, healthyACTH

        Also contains data for each individual patient in the following arrays:
            - cortisol
            - ACTH

        The first column of Cortisol and ACTH is the time values, the second
        column is the mean values of all patients, and each subsequent column
        is an individual patient. There are 58 patients in the data set.

        For example:
            cortisol[11] is Patient ID 10's cortisol concentrations
            ACTH[59] is Patient ID 58's ACTH concentrations.
        """

        __ACTH_data = np.genfromtxt("VeVaPy/data_files/tsst_acth_nelson.txt")
        __cortisol_data = np.genfromtxt("VeVaPy/data_files/tsst_cort_nelson.txt")
        __subtypes = np.genfromtxt("VeVaPy/data_files/nelson-MDD-subtypes.txt")

        __ACTH_mean = np.zeros(11)
        __cortisol_mean = np.zeros(11)
        self.ACTH = np.zeros((11,60))
        self.cortisol = np.zeros((11,60))

        # compute the mean of all patients' ACTH and cortisol concentrations at each
        #  data point
        for i in range(len(__ACTH_data[1,:])-1):
            __ACTH_mean[i] = np.mean(__ACTH_data[:,i+1])
            __cortisol_mean[i] = np.mean(__cortisol_data[:,i+1])

        # create an array of the time points we have concentrations for in minutes
        __t_nelson = np.array([0, 15, 30, 40, 50, 65, 80, 95, 110, 125, 140])

        # put the time points in the first column of our ACTH and cortisol arrays
        #  and the mean of all patients' concentrations in the second column
        for i in range(len(__t_nelson)):
            self.ACTH[i,0] = __t_nelson[i]
            self.ACTH[i,1] = __ACTH_mean[i]

            self.cortisol[i,0] = __t_nelson[i]
            self.cortisol[i,1] = __cortisol_mean[i]

        # in the remaining columns, we put the concentrations at each data point for
        #  all remaining patients (one patient per column)
        for i in range(len(__ACTH_data)):
            for j in range(len(__t_nelson)):
                self.ACTH[j,i+2] = __ACTH_data[i,j+1]
                self.cortisol[j,i+2] = __cortisol_data[i,j+1]

        # Make lists of the indices in the ACTH and CORT arrays at which each
        #  subtype of patients are found
        __atypical_indices = []
        __melancholic_indices = []
        __neither_indices = []
        __healthy_indices = []

        for index, item in enumerate(__subtypes[:,1]):
            if item == 1:
                __atypical_indices.append(index)
            elif item == 2:
                __melancholic_indices.append(index)
            elif item == 3:
                __neither_indices.append(index)
            elif item == 4:
                __healthy_indices.append(index)

        # create lists of the indices in the ACTH and CORT arrays for each subtype
        #  (we need to shift by 2 columns, because of the time column and mean
        #  concentrations columns), and the patient IDs of the patients in each
        #  subtype
        __atypical_ids = []
        __melancholic_ids = []
        __neither_ids = []
        __healthy_ids = []
        for idx, item in enumerate(__atypical_indices):
            __atypical_indices[idx] += 2
            __atypical_ids.append(__subtypes[item,0])
        for idx, item in enumerate(__melancholic_indices):
            __melancholic_indices[idx] += 2
            __melancholic_ids.append(__subtypes[item,0])
        for idx, item in enumerate(__neither_indices):
            __neither_indices[idx] += 2
            __neither_ids.append(__subtypes[item,0])
        for idx, item in enumerate(__healthy_indices):
            __healthy_indices[idx] += 2
            __healthy_ids.append(__subtypes[item,0])

        # create lists of the patients' data arrays for ACTH & CORT for each subtype

        # create lists of arrays of atypical patient CORT and ACTH data
        __atypicalCortisolList = []
        __atypicalACTHList = []
        for idx in __atypical_indices:
            __atypicalCortisolList.append(self.cortisol[:,idx])
            __atypicalACTHList.append(self.ACTH[:,idx])

        # combine the lists of arrays into 2d arrays and transpose them so that
        #  each patients' data is in a column
        self.atypicalCortisol = np.vstack(__atypicalCortisolList)
        self.atypicalCortisol = np.transpose(self.atypicalCortisol)
        self.atypicalCortisol = np.insert(self.atypicalCortisol, 0, self.cortisol[:,0], axis = 1) # insert time in first column

        self.atypicalACTH = np.vstack(__atypicalACTHList)
        self.atypicalACTH = np.transpose(self.atypicalACTH)
        self.atypicalACTH = np.insert(self.atypicalACTH, 0, self.ACTH[:,0], axis = 1) # insert time in first column

        # create lists of arrays of melancholic patient CORT and ACTH data
        __melancholicCortisolList = []
        __melancholicACTHList = []
        for idx in __melancholic_indices:
            __melancholicCortisolList.append(self.cortisol[:,idx])
            __melancholicACTHList.append(self.ACTH[:,idx])

        # combine the lists of arrays into 2d arrays and transpose them so that
        #  each patients' data is in a column
        self.melancholicCortisol = np.vstack(__melancholicCortisolList)
        self.melancholicCortisol = np.transpose(self.melancholicCortisol)
        self.melancholicCortisol = np.insert(self.melancholicCortisol, 0, self.cortisol[:,0], axis = 1) # insert time in first column

        self.melancholicACTH = np.vstack(__melancholicACTHList)
        self.melancholicACTH = np.transpose(self.melancholicACTH)
        self.melancholicACTH = np.insert(self.melancholicACTH, 0, self.ACTH[:,0], axis = 1) # insert time in first column

        # create lists of arrays of neither atypical nor melancholic MDD patient CORT and ACTH data
        __neitherCortisolList = []
        __neitherACTHList = []
        for idx in __neither_indices:
            __neitherCortisolList.append(self.cortisol[:,idx])
            __neitherACTHList.append(self.ACTH[:,idx])

        # combine the lists of arrays into 2d arrays and transpose them so that
        #  each patients' data is in a column
        self.neitherCortisol = np.vstack(__neitherCortisolList)
        self.neitherCortisol = np.transpose(self.neitherCortisol)
        self.neitherCortisol = np.insert(self.neitherCortisol, 0, self.cortisol[:,0], axis = 1) # insert time in first column

        self.neitherACTH = np.vstack(__neitherACTHList)
        self.neitherACTH = np.transpose(self.neitherACTH)
        self.neitherACTH = np.insert(self.neitherACTH, 0, self.ACTH[:,0], axis = 1) # insert time in first column

        # create lists of arrays of healthy patient CORT and ACTH data
        __healthyCortisolList = []
        __healthyACTHList = []
        for idx in __healthy_indices:
            __healthyCortisolList.append(self.cortisol[:,idx])
            __healthyACTHList.append(self.ACTH[:,idx])

        # combine the lists of arrays into 2d arrays and transpose them so that
        #  each patients' data is in a column
        self.healthyCortisol = np.vstack(__healthyCortisolList)
        self.healthyCortisol = np.transpose(self.healthyCortisol)
        self.healthyCortisol = np.insert(self.healthyCortisol, 0, self.cortisol[:,0], axis = 1) # insert time in first column

        self.healthyACTH = np.vstack(__healthyACTHList)
        self.healthyACTH = np.transpose(self.healthyACTH)
        self.healthyACTH = np.insert(self.healthyACTH, 0, self.ACTH[:,0], axis = 1) # insert time in first column

        # compute means of all patients in each subtype of depression, all control patients,
        # and all subtypes of depression combined

        # initialize empty arrays to fill with mean values
        self.healthyCortisol_mean = np.zeros((len(self.healthyCortisol[:,0]), 1))
        self.healthyACTH_mean = np.zeros((len(self.healthyACTH[:,0]), 1))
        self.depressedCortisol_mean = np.zeros((len(self.melancholicCortisol[:,0]), 1))
        self.depressedACTH_mean = np.zeros((len(self.melancholicACTH[:,0]), 1))
        self.melancholicCortisol_mean = np.zeros((len(self.melancholicCortisol[:,0]), 1))
        self.melancholicACTH_mean = np.zeros((len(self.melancholicACTH[:,0]), 1))
        self.atypicalCortisol_mean = np.zeros((len(self.atypicalCortisol[:,0]), 1))
        self.atypicalACTH_mean = np.zeros((len(self.atypicalACTH[:,0]), 1))
        self.neitherCortisol_mean = np.zeros((len(self.neitherCortisol[:,0]), 1))
        self.neitherACTH_mean = np.zeros((len(self.neitherACTH[:,0]), 1))

        # loop through each time step and add the sum of all patients' values at that time step
        for i in range(len(self.healthyCortisol[:,0])):
            self.healthyCortisol_mean[i] += np.sum(self.healthyCortisol[i, 1:])
            self.depressedCortisol_mean[i] += np.sum(self.melancholicCortisol[i, 1:])
            self.melancholicCortisol_mean[i] += np.sum(self.melancholicCortisol[i, 1:])
            self.depressedCortisol_mean[i] += np.sum(self.atypicalCortisol[i, 1:])
            self.atypicalCortisol_mean[i] += np.sum(self.atypicalCortisol[i, 1:])
            self.depressedCortisol_mean[i] += np.sum(self.neitherCortisol[i, 1:])
            self.neitherCortisol_mean[i] += np.sum(self.neitherCortisol[i, 1:])

            self.healthyACTH_mean[i] += np.sum(self.healthyACTH[i, 1:])
            self.depressedACTH_mean[i] += np.sum(self.melancholicACTH[i, 1:])
            self.melancholicACTH_mean[i] += np.sum(self.melancholicACTH[i, 1:])
            self.depressedACTH_mean[i] += np.sum(self.atypicalACTH[i, 1:])
            self.atypicalACTH_mean[i] += np.sum(self.atypicalACTH[i, 1:])
            self.depressedACTH_mean[i] += np.sum(self.neitherACTH[i, 1:])
            self.neitherACTH_mean[i] += np.sum(self.neitherACTH[i, 1:])

        # divide by the number of patients for each set to get the mean
        self.healthyCortisol_mean = self.healthyCortisol_mean/15
        self.healthyCortisol_mean = np.insert(self.healthyCortisol_mean, 0, self.cortisol[:,0], axis = 1) # insert time in first column
        self.healthyACTH_mean = self.healthyACTH_mean/15
        self.healthyACTH_mean = np.insert(self.healthyACTH_mean, 0, self.ACTH[:,0], axis = 1) # insert time in first column

        self.depressedCortisol_mean = self.depressedCortisol_mean/43
        self.depressedCortisol_mean = np.insert(self.depressedCortisol_mean, 0, self.cortisol[:,0], axis = 1) # insert time in first column
        self.depressedACTH_mean = self.depressedACTH_mean/43
        self.depressedACTH_mean = np.insert(self.depressedACTH_mean, 0, self.ACTH[:,0], axis = 1) # insert time in first column

        self.melancholicCortisol_mean = self.melancholicCortisol_mean/15
        self.melancholicCortisol_mean = np.insert(self.melancholicCortisol_mean, 0, self.cortisol[:,0], axis = 1) # insert time in first column
        self.melancholicACTH_mean = self.melancholicACTH_mean/15
        self.melancholicACTH_mean = np.insert(self.melancholicACTH_mean, 0, self.ACTH[:,0], axis = 1) # insert time in first column

        self.atypicalCortisol_mean = self.atypicalCortisol_mean/14
        self.atypicalCortisol_mean = np.insert(self.atypicalCortisol_mean, 0, self.cortisol[:,0], axis = 1) # insert time in first column
        self.atypicalACTH_mean = self.atypicalACTH_mean/14
        self.atypicalACTH_mean = np.insert(self.atypicalACTH_mean, 0, self.ACTH[:,0], axis = 1) # insert time in first column

        self.neitherCortisol_mean = self.neitherCortisol_mean/14
        self.neitherCortisol_mean = np.insert(self.neitherCortisol_mean, 0, self.cortisol[:,0], axis = 1) # insert time in first column
        self.neitherACTH_mean = self.neitherACTH_mean/14
        self.neitherACTH_mean = np.insert(self.neitherACTH_mean, 0, self.ACTH[:,0], axis = 1) # insert time in first column

        if scale.lower() == "hours":
            self.cortisol[:,0] = np.divide(self.cortisol[:,0], 60)
            self.ACTH[:,0] = np.divide(self.ACTH[:,0], 60)
            self.depressedCortisol_mean[:,0] = np.divide(self.depressedCortisol_mean[:,0], 60)
            self.depressedACTH_mean[:,0] = np.divide(self.depressedACTH_mean[:,0], 60)
            self.atypicalCortisol[:,0] = np.divide(self.atypicalCortisol[:,0], 60)
            self.atypicalCortisol_mean[:,0] = np.divide(self.atypicalCortisol_mean[:,0], 60)
            self.atypicalACTH[:,0] = np.divide(self.atypicalACTH[:,0], 60)
            self.atypicalACTH_mean[:,0] = np.divide(self.atypicalACTH_mean[:,0], 60)
            self.melancholicCortisol[:,0] = np.divide(self.melancholicCortisol[:,0], 60)
            self.melancholicCortisol_mean[:,0] = np.divide(self.melancholicCortisol_mean[:,0], 60)
            self.melancholicACTH[:,0] = np.divide(self.melancholicACTH[:,0], 60)
            self.melancholicACTH_mean[:,0] = np.divide(self.melancholicACTH_mean[:,0], 60)
            self.neitherCortisol[:,0] = np.divide(self.neitherCortisol[:,0], 60)
            self.neitherCortisol_mean[:,0] = np.divide(self.neitherCortisol_mean[:,0], 60)
            self.neitherACTH[:,0] = np.divide(self.neitherACTH[:,0], 60)
            self.neitherACTH_mean[:,0] = np.divide(self.neitherACTH_mean[:,0], 60)
            self.healthyCortisol[:,0] = np.divide(self.healthyCortisol[:,0], 60)
            self.healthyCortisol_mean[:,0] = np.divide(self.healthyCortisol_mean[:,0], 60)
            self.healthyACTH[:,0] = np.divide(self.healthyACTH[:,0], 60)
            self.healthyACTH_mean[:,0] = np.divide(self.healthyACTH_mean[:,0], 60)

    def patientF(self, scale):
        """
        Import the data for "Patient F" from the paper by Bangsgaard & Ottesen
        (2017) and save the data to separate arrays for cortisol and ACTH
        concentration data.

        Contains cortisol and ACTH data in the following arrays:
            - cortisol
            - ACTH

        Also create smoothed versions of these arrays with _smooth at the end
        of the variable name.

        For example:
            cortisol_smooth
        """
        self.cortisol = np.genfromtxt("VeVaPy/data_files/Bangsgaard-Ottesen-2017-patient-f-cortisol-data.txt", dtype = float)
        self.ACTH = np.genfromtxt("VeVaPy/data_files/Bangsgaard-Ottesen-2017-patient-f-ACTH-data.txt", dtype = float)

        self.cortisol_smooth = self.cortisol
        self.ACTH_smooth = self.ACTH

        self.cortisol_smooth[2:-2,1] = self.__smoothing(self.cortisol[:,1])
        self.ACTH_smooth[2:-2,1] = self.__smoothing(self.ACTH[:,1])

        self.cortisol = np.genfromtxt("VeVaPy/data_files/Bangsgaard-Ottesen-2017-patient-f-cortisol-data.txt", dtype = float)
        self.ACTH = np.genfromtxt("VeVaPy/data_files/Bangsgaard-Ottesen-2017-patient-f-ACTH-data.txt", dtype = float)

        if scale.lower() == "minutes":
            self.cortisol[:,0] = np.multiply(self.cortisol[:,0], 60)
            self.ACTH[:,0] = np.multiply(self.ACTH[:,0], 60)

            self.cortisol_smooth[:,0] = np.multiply(self.cortisol_smooth[:,0], 60)
            self.ACTH_smooth[:,0] = np.multiply(self.ACTH_smooth[:,0], 60)
