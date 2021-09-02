# File Name: Sriram-2012.py
# Description: Sriram et al. (2012) HPA axis model
# Author: Christopher Parker
# Created: Fri Aug 21, 2020 | 09:05P EDT
# Last Modified: Fri Aug 21, 2020 | 09:39P EDT

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
import matplotlib.pyplot as plt
import scipy.integrate as sci
from PyDSTool import *
import scipy.optimize as sco
from scipy import optimize
from scipy.interpolate import interp1d
import mpld3
from tabulate import tabulate

## Parameters and Initial Conditions

# it looks, based on the XPP file from the authors, like they start CRH, ACTH, CORT and GR at 0 each and just run
# the solver until they reach some steady state

y0 = [1,1,12,2]

# or we can initialize the parameters that stay the same as the literature 
# values and optimize all parameters

V_S3 = 1.58 # reported as 1.58-5
K_m1 = 2
K_P2 = 0.3 # reported as 0.3-1.8
V_S4 = 1.58 # reported as 1.58-5
K_m2 = 2
K_P3 = 0.3 # reported as 0.3-1.8
V_S5 = 1.58 # reported as 1.58-5
K_m3 = 2
K_d1 = 0.173
K_d2 = 0.035
K_d3 = 0.009
n1 = 5
n2 = 4
K_b = 0.01 # no literature value reported
G_tot = 2 # no literature value reported
V_S2 = 0 # reported as 0-1
K1 = 1
K_d5 = 0.01

# here are the bounds used for all of the parameters, assuming we want to optimize more than just k_stress and k_i
bounds = [(5,20), (0.5,3), (3,4), (1,2), (7,11), (0.5,1.5), (0.08,2), (0.5,1.2), (0.001,0.008), (0.03,0.08), (0.002,0.005), (0.001,0.01), (0.1,0.5), (4,6), (4,6), (0.008,0.05), (2,5), (0.01,0.07), (0.2,0.7), (0.04,0.09)]

# length of time over which we wish to integrate
timeLength = (0,24.01)

# time interval and step definition, based on XPP model from authors
t_start = 0
t_end = 24.01
t_step = 0.01

## Put Raw Data Into Arrays

yehudaControlCortisol = np.genfromtxt("yehuda-control-cortisol.txt")
yehudaPTSDCortisol = np.genfromtxt("yehuda-PTSD-cortisol.txt")
yehudaDepressedCortisol = np.genfromtxt("yehuda-depressed-cortisol.txt")

# convert time scales to hours for the raw data, because the model is in terms of hours
for i in range(len(yehudaControlCortisol)):
    yehudaControlCortisol[i,0] = yehudaControlCortisol[i,0]/60
    yehudaPTSDCortisol[i,0] = yehudaPTSDCortisol[i,0]/60
    yehudaDepressedCortisol[i,0] = yehudaDepressedCortisol[i,0]/60

## Smooth Data, If Desired

# this function computes the moving average over the neighboring 5 points
#def smoothing(a, n=5) :
    #idx = int((n-1)/2)
    #ret = np.cumsum(a, dtype=float)
    #ret[idx+1:-idx] = ret[n:] - ret[:-n]
    #ret[idx] = ret[idx+2]
    #return ret[idx:-idx] / n
#
#yehudaControlCortisol_smooth = yehudaControlCortisol
#yehudaPTSDCortisol_smooth = yehudaPTSDCortisol
#yehudaDepressedCortisol_smooth = yehudaDepressedCortisol
#
#yehudaControlCortisol_smooth[2:-2,1] = smoothing(yehudaControlCortisol[:,1])
#yehudaPTSDCortisol_smooth[2:-2,1] = smoothing(yehudaPTSDCortisol[:,1])
#yehudaDepressedCortisol_smooth[2:-2,1] = smoothing(yehudaDepressedCortisol[:,1])

## Model Function -- Includes ODE Solver

def model(params, ics, t):
    def ode_system(t, y):
        dy = np.zeros(4)

        [k_stress, k_i, V_S3, K_m1, K_P2, V_S4, K_m2, K_P3, V_S5, K_m3, K_d1, K_d2, K_d3, n1, n2, K_b, G_tot, V_S2, K1, K_d5] = params
        dy[0] = k_stress*(k_i**n2/(k_i**n2 + y[3]**n2)) - V_S3*(y[0]/(K_m1 + y[0])) - K_d1*y[0]
        dy[1] = K_P2*y[0]*(k_i**n2/(k_i**n2 + y[3]**n2)) - V_S4*(y[1]/(K_m2 + y[1])) - K_d2*y[1]
        dy[2] = K_P3*y[1] - V_S5*(y[2]/(K_m3 + y[2])) - K_d3*y[2]
        dy[3] = K_b*y[2]*(G_tot - y[3]) + V_S2*(y[3]**n1/(K1**n1 + y[3]**n1)) - K_d5*y[3]

        return dy

    # solve the system with scipy.integrate.ode to see if it's any faster
    solver = sci.ode(ode_system)
    solver.set_integrator('vode', method='bdf', atol=3e-16, rtol=1e-14)
    solver.set_initial_value(ics, t_start)

    ts = []
    ys = []

    while solver.successful() and solver.t < t_end:
        solver.integrate(solver.t + t_step)
        ts.append(solver.t)
        ys.append(solver.y)

    # reshape the output frome ode to an array with the times on the first column
    ts = np.reshape(ts, (len(ts),1))
    ys = np.vstack(ys)
    timeSeries = np.hstack((ts, ys))
    return timeSeries

## Cost Function Definition

def cost_fun(params):
    # call the solve function
    simData = model(params, y0, timeLength)

    # this is where Rick makes sure we only have unique values for t, so no time step is repeated
    # I'll include it commented out here, and see if it changes anything later
    idx = np.unique(simData[:,0], return_index = True)
    idx = idx[1]
    simData = simData[idx,:]

    # here, rick performs a cubic interpolation between time steps
    # I could either do this, or just compute the SSE between the raw data and computed data points without doing
    # the interpolation (as long as every raw data point is hit by the time steps the model computes)
    #spline_ACTH = interp1d(simData[:,0], simData[:,2], kind = 'cubic')
    spline_CORT = interp1d(simData[:,0], simData[:,3], kind = 'cubic')

    # compute the actual cost value for the current parameter set by finding SSE between raw data and splines
    # this is where we change the data set we are trying to match, so that it computes the cost based on whatever
    #     data set we put in as the x values into the spline and the y values to subtract
    #acthSSE = np.sum((spline_ACTH(patientFacth_smooth[:,0]) - patientFacth_smooth[:,1])**2)
    cortSSE = np.sum((spline_CORT(yehudaControlCortisol[:,0]) - yehudaControlCortisol[:,1])**2)

    # if i run it with acth data, also, can make cost the average of cortisol and ACTH SSEs
    #cost = (acthSSE+cortSSE)/2
    # for now though, cost is just the SSE of cortisol data and simulation
    cost = cortSSE

    return cost

## Run the Optimization

# number of times to run the optimization
n = 10

# define an array to hold the population of parameter vectors
opt_pars = np.zeros((n, len(bounds)+1))

# initialize arrays to save simulation cortisol and ACTH data from each optimization
sims_cort = np.zeros((2401, n))
sims_acth = np.zeros((2401, n))
sims_crh = np.zeros((2401, n))
sims_gr = np.zeros((2401, n))

%%time

# loop n times, running the optimization each time
for i in range(0,n):

    print(f"Optimization Run #{i+1}")

    # call the differential evolution optimization function on the cost function
    res = sco.differential_evolution(cost_fun, bounds, maxiter = None, disp = True, popsize = 1, workers = 8, updating = "deferred")

    # alternatively, we can run the SHGO algorithm with the sampling_method = "sobol" flag to do global
    #     optimization with reporting all local minima, as well
    #res = sco.shgo(cost_fun, bounds, callback=callback_fun(*shgo_iter_steps), options = {"f_min": 0.1, "maxiter": None, "minimize_every_iter": True, "local_iter": False, "disp": True}, iters = 3)
    #res = sco.basinhopping(cost_fun, x0, niter = 1000)
    #res = sco.dual_annealing(cost_fun, bounds)

    # plug the optimized parameters into the solver
    optimizedSimData = model(res.x, y0, timeLength)

    # save CRH, cortisol and ACTH data into sims arrays
    sims_gr[:,i] = optimizedSimData[:,4]
    sims_cort[:,i] = optimizedSimData[:,3]
    sims_acth[:,i] = optimizedSimData[:,2]
    sims_crh[:,i] = optimizedSimData[:,1]

    # save the cost function values and optimized parameters for each iteration into the array opt_pars
    opt_pars[i,0] = res.fun
    opt_pars[i,1:] = res.x

## Save Output to File

np.savetxt('sriram-opt-pars-yehudaControl-10-all-params.txt', opt_pars)

np.savetxt('sriram-sims-gr-yehudaControl-10-all-params.txt', sims_gr)
np.savetxt('sriram-sims-crh-yehudaControl-10-all-params.txt', sims_crh)
np.savetxt('sriram-sims-acth-yehudaControl-10-all-params.txt', sims_acth)
np.savetxt('sriram-sims-cort-yehudaControl-10-all-params.txt', sims_cort)

## Compute Means and Std Devations of Parameters and Output as Table

k_stress_mean = np.mean(opt_pars[:,1])
k_stress_std = np.std(opt_pars[:,1])
k_i_mean = np.mean(opt_pars[:,2])
k_i_std = np.std(opt_pars[:,2])

print(tabulate([["k_stress", "%f +- %f" % (k_stress_mean, k_stress_std)], ["k_i", "%f +- %f" % (k_i_mean, k_i_std)]], headers = ["Parameter", "Mean +- Standard Deviation"]))

np.savetxt('sriram-param-means-stds-yehudaControl-10-all-params.txt', [k_stress_mean, k_stress_std, k_i_mean, k_i_std])


