# File Name: optimize.py
# Description: Contains the function to run parameter optimization algorithms
#  based on user inputs and return the cost function value, as well as the cost
#  function definitions that can be used.
# Author: Christopher Parker
# Created: Thu Aug 25, 2022 | 03:19P EDT
# Last Modified: Mon Sep 12, 2022 | 04:58P EDT

import scipy.optimize as sco
from scipy.interpolate import interp1d
import time
import numpy as np

# This function contains the main loop used for running iterations of 
#  parameter optimization algorithms.
# Non-optional arguments are: the cost function to use, the model function to use,
#  the data sets to optimize against, the initial conditions and the bounds on
#  parameters to optimize.
# Users can also optionally specify the number of iterations of the parameter
#  optimization algorithm to run, the algorithm to use (options include
#  differential_evolution, shgo, basinhopping and dual_annealing), the maximum
#  number of iterations of the algorithm to run INSIDE EACH FULL ITERATION, the
#  population size for the algorithm, the indices of the initial condition array
#  that are being optimized and the initial parameters to use (only for
#  basinhopping algorithm).
def run(cost_fun, model, data_to_match, y0, bounds, num_iter=5, \
        algorithm="differential_evolution", \
        maxiter=999, popsize=1, ICopt_indices = [], x0 = []):

    # Check the system clock time at the start of the loop so that we can keep
    #  track of how long the full run takes.
    start_time = time.time()

    # Run the parameter optimization algorithm num_iter times in a for loop
    for i in range(0,num_iter):

        # Let the user know which iteration the program is currently working on
        print(f"Optimization Run #{i+1}")

        # Check the algorithm the user wants to run, and call it
        if algorithm=="differential_evolution":
            res = sco.differential_evolution(cost_fun, bounds, \
                    maxiter = maxiter, disp = True, popsize = popsize)
        elif algorithm=="shgo":
            res = sco.shgo(cost_fun, bounds, options = {"f_min": 0.1, \
                            "maxiter": None, "minimize_every_iter": True, \
                            "local_iter": False, "disp": True}, iters = 3)
        elif algorithm=="basinhopping":
            res = sco.basinhopping(cost_fun, x0, niter = maxiter)
        elif algorithm=="dual_annealing":
            res = sco.dual_annealing(cost_fun, bounds)

        # Save the optimized initial conditions from the algorithm into the
        #  array y0 so that we can use it to re-run the model
        for index,entry in enumerate(ICopt_indices):
            y0[entry] = res.x[index]

        # We need to re-run the model with the optimized parameters to get the
        #  full variable concentration arrays, because we do not get this info
        #  from the parameter optimization algorithms themselves
        optimizedSimData = model(res.x[len(ICopt_indices):], y0)

        # Check if it's the first time through the loop
        if i == 0:
            # If it is, then initialize arrays to hold all of the concentration
            #  data and the optimized parameter values for all iterations
            simData_all = optimizedSimData
            opt_pars = np.hstack((res.fun, res.x[len(ICopt_indices):]))
        else:
            # If it's not the first time through the loop, then just add on to
            #  the arrays created in the first loop
            simData_all = np.hstack((simData_all, optimizedSimData))
            opt_pars_tmp = np.hstack((res.fun, res.x[len(ICopt_indices):]))
            opt_pars = np.vstack((opt_pars, opt_pars_tmp))

    # Check the clock time now that we've completed the loop
    end_time = time.time()
    # Report the total runtime
    print(f"Runtime: {end_time - start_time} seconds")

    # Return the optimized parameters from each iteration, and all of the
    #  concentration data from running the model with those optimized parameters
    return opt_pars, simData_all

# This function takes the time steps and data points for the real-world ACTH 
#  and cortisol concentration values you're optimizing against as well as the 
#  data from a simulation with the model and returns the cost for the parameter 
#  set used.
# There are optional arguments for ACTH_index and CORT_index in case the model
#  equations are ordered differently from the standard. That way the user can
#  pass the indices of ACTH and CORT as they are defined in y (or y0)
def SSE_cost(time_ACTH, data_ACTH, time_CORT, data_CORT, simData, 
             ACTH_index = 1, CORT_index = 2):
    # Compute the means of ACTH and CORT data arrays
    mean_ACTH = np.mean(data_ACTH)
    mean_CORT = np.mean(data_CORT)

    # Normalize the simData arrays by the mean values of data set to be matched.
    # We use ACTH_index and CORT_index plus 1 because the first column is the time
    # steps
    simNorm_ACTH = simData[:,ACTH_index+1]/mean_ACTH
    simNorm_CORT = simData[:,CORT_index+1]/mean_CORT

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

        # We define cost as the average of the ACTH and CORT SSEs.
        cost = (acthSSE + cortSSE)/2

        return cost

    except ValueError:
        # In the case that we encounter a ValueError, this means that the ODE
        #  solver quit before computing all time steps up to t_end. The error
        #  arises when we attempt to plug in a time value after where the 
        #  solver quit to spline_ACTH or spline_CORT. So we catch the
        #  ValueError here, and let the user know that the ODE solver exited
        #  early.
        print("ODE solver did not make it through all data points.")


# This is similar to the function above, but does not take ACTH concentration
#  data as an input. So you'd use this one if your real-world data only has
#  cortisol concentrations
def SSE_cost_noACTH(time_CORT, data_CORT, simData, CORT_index = 2):
    # Compute the mean of the CORT data array
    mean_CORT = np.mean(data_CORT)

    # Normalize the simData array by the mean value of data set to be matched
    simNorm_CORT = simData[:,CORT_index+1]/mean_CORT

    # Normalize the data set to be matched, as well
    dataNorm_CORT = data_CORT/mean_CORT

    # Now, we interpolate between the simulated data points, to ensure we have
    #  a simulated data point at the exact time of each real-world data point
    # We are currently doing a linear interpolation, although we could also
    #  choose to do cubic. however, I don't think it makes a huge amount of
    #  difference in this context
    spline_CORT = interp1d(simData[:,0], simNorm_CORT, kind = 'linear')

    # We use a try/except loop to ensure that we don't run into an error that
    #  causes the entire simulation to fail and have to start over
    try:
        # As the data we are matching does not include ACTH values, we simply
        #  define cost as the SSE between raw data and splines of the CORT array
        cost = np.sum((spline_CORT(time_CORT) - dataNorm_CORT)**2)

        return cost

    except ValueError:
        # In the case that we encounter a ValueError, this means that the ODE
        #  solver quit before computing all time steps up to t_end. The error
        #  arises when we attempt to plug in a time value after where the 
        #  solver quit to spline_CORT. So we catch the ValueError here, and let 
        #  the user know that the ODE solver exited early.
        print("ODE solver did not make it through all data points.")

# We also need to define cost functions for using the minimum and maximum
#  distance between the simulation and real-world data.
#  
# Here, we use the maximum distance
def max_cost(time_ACTH, data_ACTH, time_CORT, data_CORT, simData,
             ACTH_index = 1, CORT_index = 2):
    # Compute the means of ACTH and CORT data arrays
    mean_ACTH = np.mean(data_ACTH)
    mean_CORT = np.mean(data_CORT)

    # Normalize the simData arrays by the mean values of data set to be matched
    simNorm_ACTH = simData[:,ACTH_index+1]/mean_ACTH
    simNorm_CORT = simData[:,CORT_index+1]/mean_CORT

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
        #  maximum distance between the simulations and data for each of ACTH 
        #  and CORT
        acthMAX = np.amax((spline_ACTH(time_ACTH) - dataNorm_ACTH)**2)
        cortMAX = np.amax((spline_CORT(time_CORT) - dataNorm_CORT)**2)

        # We define cost as the maximum of the maximums that we just found above
        cost = np.amax([acthMAX, cortMAX])

        return cost

    except ValueError:
        # In the case that we encounter a ValueError, this means that the ODE
        #  solver quit before computing all time steps up to t_end. The error
        #  arises when we attempt to plug in a time value after where the 
        #  solver quit to spline_ACTH or spline_CORT. So we catch the
        #  ValueError here, and let the user know that the ODE solver exited
        #  early.
        print("ODE solver did not make it through all data points.")

# And here we compute the cost based on the maximum distance for data sets that
#  only contain cortisol data
def max_cost_noACTH(time_CORT, data_CORT, simData, CORT_index = 2):
    # Compute the mean of the CORT data array
    mean_CORT = np.mean(data_CORT)

    # Normalize the simData array by the mean value of data set to be matched
    simNorm_CORT = simData[:,CORT_index+1]/mean_CORT

    # Normalize the data set to be matched, as well
    dataNorm_CORT = data_CORT/mean_CORT

    # Now, we interpolate between the simulated data points, to ensure we have
    #  a simulated data point at the exact time of each real-world data point
    # We are currently doing a linear interpolation, although we could also
    #  choose to do cubic. however, I don't think it makes a huge amount of
    #  difference in this context
    spline_CORT = interp1d(simData[:,0], simNorm_CORT, kind = 'linear')

    # We use a try/except loop to ensure that we don't run into an error that
    #  causes the entire simulation to fail and have to start over
    try:
        # As the data we are matching does not include ACTH values, we simply
        #  define cost as the maximum distance between raw data and splines 
        #  of the CORT array
        cost = np.amax((spline_CORT(time_CORT) - dataNorm_CORT)**2)

        return cost

    except ValueError:
        # In the case that we encounter a ValueError, this means that the ODE
        #  solver quit before computing all time steps up to t_end. The error
        #  arises when we attempt to plug in a time value after where the 
        #  solver quit to spline_CORT. So we catch the ValueError here, and let 
        #  the user know that the ODE solver exited early.
        print("ODE solver did not make it through all data points.")
