# File Name: costFunc.py
# Description: this module will contain the function for computing cost, 
#  although I'm not sure how reliably I'll be able to do that for all 6 models
#  as it currently has quite few hardcoded variables
# Author: Christopher Parker
# Created: Tue Jan 25, 2022 | 09:26P EST
# Last Modified:

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
#                           GNU GPL LICENSE                            #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
#                                                                      #
# Copyright Christopher Parker 2017 <cjp65@case.edu>                   #
#                                                                      #
# This program is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# This program is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         #
# GNU General Public License for more details.                         #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with this program. If not, see <http://www.gnu.org/licenses/>. #
#                                                                      #
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

import numpy as np
from scipy.interpolate import interp1d

def cost(params, time_ACTH, data_ACTH, time_CORT, data_CORT, simData):
    # Compute the means of ACTH and CORT data arrays
    mean_ACTH = np.mean(data_ACTH)
    mean_CORT = np.mean(data_CORT)

    # Normalize the simData arrays by the mean values of data set to be matched
    simNorm_ACTH = simData[:,2]/mean_ACTH
    simNorm_CORT = simData[:,3]/mean_CORT

    # Normalize the data set to be matched, as well
    dataNorm_ACTH = data_ACTH/mean_ACTH
    dataNorm_CORT = data_CORT/mean_CORT

    # Now, we interpolate between the simulated data points, to ensure we have
    #  a simulated data point at the exact time of each real-world data point
    # We are currently doing a linear interpolation, although we could also
    #  choose to do cubic. however, I don't think it makes a huge amount of
    #  difference in this context
    spline_ACTH = interp1d(simData[:,0], simNorm_ACTH, kind = 'linear')
    spline_CORT = interp1d(simData[:,0], simNorm_CORT, kind = 'linear')

    # We use a try/except loop to ensure that we don't run into an error that
    #  causes the entire simulation to fail and have to start over
    try:
        # Compute the cost value for the current parameter set by finding the
        #  SSE between raw data and splines.
        acthSSE = np.sum((spline_ACTH(time_ACTH) - dataNorm_ACTH)**2)
        cortSSE = np.sum((spline_CORT(time_CORT) - dataNorm_CORT)**2)

        # When we are matching data that includes ACTH values, we define cost
        #  as the average of the ACTH and CORT SSEs.
        cost = (acthSSE + cortSSE)/2

        # If the data we are matching does not include ACTH values, we simply
        #  define cost as the SSE of the CORT array
        # cost = cortSSE

        return cost
    except ValueError:
        # In the case that we encounter a ValueError, this means that the ODE
        #  solver quit before computing all time steps up to t_end. The error
        #  arises when we attempt to plug in a time value after where the 
        #  solver quit to spline_ACTH or spline_CORT. So we catch the
        #  ValueError here, and let the user know that the ODE solver exited
        #  early.
        print("ODE solver did not make it through all data points.")
