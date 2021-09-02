# File Name: Bangsgaard-Ottesen-2017.py
# Description: Code to run on the CCHMC HPC Cluster for the Bangsgaard & Ottesen 2017 Model
# Author: Christopher Parker
# Created: Wed Jul 29, 2020 | 06:43P EDT
# Last Modified: Sun Aug 02, 2020 | 05:44P EDT

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
import scipy.integrate as sci
from scipy.interpolate import interp1d
import scipy.optimize as sco
from decimal import Decimal
import time

start_time = time.time()
## Parameters and Initial Conditions
#
# initial conditions, based on control patient (f) concentrations at midnight
#    had to guess for CRH level, though

y0 = [2,8.725314,1.158798]

# insensitive parameters, kept fixed between subjects

a_2 = 1.7809e9
a_3 = 2.2803e4
a_4 = 1.7745e5
mu = 5.83e2
T = Decimal(1440)
N_c = Decimal(0.5217)
k = Decimal(5)
l = Decimal(6)
alpha = Decimal(300)
beta = Decimal(950)
eps = Decimal(0.01)

# parameters for control subject (f), listed in Table A1 and Table A2

a_0 = 3.9031e-4
a_1 = 6.839e12
a_5 = 4.617e-4
w_1 = 0.0337
w_2 = 0.0205
w_3 = 0.0238
delta = 83.8

# bounds for the parameters to be used in optimization, see above block of parameters for control subject (f) for 
#     the order of parameters in this array
bounds = ([0., 0.02], [6.5e12, 7e12], [0.0001, 0.00075], [0.03, 0.06], [0.007, 0.04], [0.008, 0.035], [50., 2000.])

# length of time over which we wish to integrate
timeLength = (0,1441)

t_start = -0.01
t_end = 1441
t_step = 0.01

## Put extracted data from control patient F (Bangsgaard & Ottesen, 2017) into arrays and smooth over neighboring 5 points
# generate arrays for the cortisol and ACTH data from control patient F in the Bangsgaard & Ottesen paper
patientFcortisol = np.genfromtxt("Bangsgaard-Ottesen-2017-patient-f-cortisol-data.txt")
patientFacth = np.genfromtxt("Bangsgaard-Ottesen-2017-patient-f-ACTH-data.txt")

# this function computes the moving average over the neighboring 5 points
def smoothing(a, n=5) :
    idx = int((n-1)/2)
    ret = np.cumsum(a, dtype=float)
    ret[idx+1:-idx] = ret[n:] - ret[:-n]
    ret[idx] = ret[idx+2]
    return ret[idx:-idx] / n

# create arrays for the smoothed data
patientFcortisol_smooth = patientFcortisol
patientFacth_smooth = patientFacth

# run the smoothing function on the raw data
# REMEMBER: need to re-extract the data from the files into the non-smooth arrays to make them non-smooth.
#     I'm still not sure why it's smoothing the original data when I only save the values from the smoothing function
#     into the smooth arrays
patientFcortisol_smooth[2:-2,1] = smoothing(patientFcortisol[:,1])
patientFacth_smooth[2:-2,1] = smoothing(patientFacth[:,1])

# convert the time scale to minutes so that it agrees with the ODEs

for i in range(len(patientFcortisol_smooth[:,0])):
    patientFcortisol_smooth[i,0] = patientFcortisol[i,0]*60
for i in range(len(patientFacth_smooth[:,0])):
    patientFacth_smooth[i,0] = patientFacth[i,0]*60

print("imported patient f data and smoothed")

## Put extracted data from control group (Carroll et al., 2007) into arrays and potentially smooth the data
# extract the data from text files into 145x2 arrays
carrollControlCortisol = np.genfromtxt("controlGroupCortisolCarroll.txt", dtype = float)
carrollHCDepressedCortisol = np.genfromtxt("HCDepressedCortisolCarroll.txt", dtype = float)
carrollLCDepressedCortisol = np.genfromtxt("LCDepressedCortisolCarroll.txt", dtype = float)

carrollControlACTH = np.genfromtxt("controlGroupACTHCarroll.txt", dtype = float)
carrollHCDepressedACTH = np.genfromtxt("HCDepressedACTHCarroll.txt", dtype = float)
carrollLCDepressedACTH = np.genfromtxt("LCDepressedACTHCarroll.txt", dtype = float)

# run smoothing if so desired
# REMEMBER: need to re-extract the data from the files into the non-smooth arrays to make them non-smooth.
#     I'm still not sure why it's smoothing the original data when I only save the values from the smoothing function
#     into the smooth arrays
carrollControlCortisol_smooth = carrollControlCortisol
carrollHCDepressedCortisol_smooth = carrollHCDepressedCortisol
carrollLCDepressedCortisol_smooth = carrollLCDepressedCortisol
carrollControlACTH_smooth = carrollControlACTH
carrollHCDepressedACTH_smooth = carrollHCDepressedACTH
carrollLCDepressedACTH_smooth = carrollLCDepressedACTH

carrollControlCortisol_smooth[2:-2,1] = smoothing(carrollControlCortisol[:,1])
carrollHCDepressedCortisol_smooth[2:-2,1] = smoothing(carrollHCDepressedCortisol[:,1])
carrollLCDepressedCortisol_smooth[2:-2,1] = smoothing(carrollLCDepressedCortisol[:,1])

carrollControlACTH_smooth[2:-2,1] = smoothing(carrollControlACTH[:,1])
carrollHCDepressedACTH_smooth[2:-2,1] = smoothing(carrollHCDepressedACTH[:,1])
carrollLCDepressedACTH_smooth[2:-2,1] = smoothing(carrollLCDepressedACTH[:,1])

l = 0
timeCarroll = np.zeros(len(carrollControlCortisol[:,0]))
for i in carrollControlCortisol[:,0]:
    timeCarroll[l] = i/60
    l += 1

print("imported carroll data and smoothed")

## Model Function -- Includes ODE Solver

def model(params, ics, t):
    # function which represents the circadian rhythm
    def c(t, delta):
        # for some reason, the Decimal object doesn't do modular arithmetic correctly, so it reports a negative number
        # mod 1440 as that negative number plus whatever multiple of 1440
        # so we add 1440 to it until it's positive, then take the mod
        t_m = Decimal(t-delta)
        while t_m < 0:
            t_m += 1440
        t_m = t_m%T
        
        ct = (N_c*((t_m**k/(t_m**k + alpha**k))*((T - t_m)**l/((T - t_m)**l + beta**l)) + eps))
        
        # check if we are getting properly bounded values for c(t)
        if not(0.005217 <= ct <= 1):
            print("C(t) is outside of the reasonable bounds")
        
        return float(ct)
    
    # function containing the system, to be called by solver
    def ode_system(t, y):
        # initialize array to hold ODE function values
        dy = np.zeros(3)
        
        # define parameter values
        [a_0, a_1, a_5, w_1, w_2, w_3, delta] = params
        
        # the ODE system itself
        dy[0] = a_0 + c(t, delta)*(a_1/(1 + a_2*y[2]**2))*(y[0]/(mu + y[0])) - w_1*y[0]
        dy[1] = (a_3*y[0])/(1 + a_4*y[2]) - w_2*y[1]
        dy[2] = a_5*y[1]**2 - w_3*y[2]
        
        return dy
    
    # solve the system with scipy.integrate.ode to see if it's any faster
    solver = sci.ode(ode_system)
    solver.set_integrator('lsoda')
    solver.set_initial_value(ics, t_start)
    
    ts = []
    ys = []
    
    while solver.successful() and solver.t < t_end:
        solver.integrate(solver.t + t_step)
        ts.append(solver.t)
        ys.append(solver.y)

    # solve the system with solve_ivp
    #timeSeries = sci.solve_ivp(ode_system, t, ics, t_eval=np.arange(0,1441,0.01), method='BDF')
    
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
    #idx = np.unique(simData[:,0], return_index = True)
    #idx = idx[1]
    #simData = simData[idx,:]
    
    # here, rick performs a cubic interpolation between time steps
    # I could either do this, or just compute the SSE between the raw data and computed data points without doing
    # the interpolation.
    spline_ACTH = interp1d(simData[:,0], simData[:,2], kind = 'cubic')
    spline_CORT = interp1d(simData[:,0], simData[:,3], kind = 'cubic')
    
    # compute the actual cost value for the current parameter set by finding SSE between raw data and splines
    # I can either do just cortisol for this, or take an average between cortisol and ACTH since I ha√e data for both
    # first, I'm going to try doing the average
    #
    # this is where we change the data set we are trying to match, so that it computes the cost based on whatever
    #     data set we put in as the x values into the spline and the y values to subtract
    #
    # should I consider splitting the data sets in half, and using only the first half as a "training" set
    #     to compute the cost function?
    acthSSE = np.sum((spline_ACTH(patientFcortisol_smooth[:,0]) - patientFcortisol_smooth[:,1])**2)
    cortSSE = np.sum((spline_CORT(patientFacth_smooth[:,0]) - patientFacth_smooth[:,1])**2)
    cost = (acthSSE+cortSSE)/2
    
    return cost

## Run the Optimization

# number of times to run the optimization
n = 5

# define an array to hold the population of parameter vectors
opt_pars = np.zeros((n, len(bounds)+1))

# initialize arrays to save simulation cortisol and ACTH data from each optimization
sims_cort = np.zeros((144102, n))
sims_acth = np.zeros((144102, n))
sims_crh = np.zeros((144102, n))

# loop n times, running the optimization each time
for i in range(0,n):
    
    print(f"Optimization Run #{i+1}")
    
    # call the differential evolution optimization function on the cost function
    res = sco.differential_evolution(cost_fun, bounds, disp = True, maxiter = 1000, popsize = 15)
    
    # alternatively, we can run the SHGO algorithm with the sampling_method = "sobol" flag to do global
    #     optimization with reporting all local minima, as well
    #res = sco.shgo(cost_fun, bounds, options = {"disp": True}, n = 100, iters = 1, sampling_method = "sobol")
    
    # plug the optimized parameters into the solver
    optimizedSimData = model(res.x, y0, timeLength)
    print(optimizedSimData.shape)
    
    # save CRH, cortisol and ACTH data into sims arrays
    sims_cort[:,i] = optimizedSimData[:,3]
    sims_acth[:,i] = optimizedSimData[:,2]
    sims_crh[:,i] = optimizedSimData[:,1]
    
    # save the cost function values and optimized parameters for each iteration into the array opt_pars
    opt_pars[i,0] = res.fun
    opt_pars[i,1:] = res.x

## Compile data, get means and standard deviations
a_0_mean = np.mean(opt_pars[:,1])
a_1_mean = np.mean(opt_pars[:,2])
a_5_mean = np.mean(opt_pars[:,3])
w_1_mean = np.mean(opt_pars[:,4])
w_2_mean = np.mean(opt_pars[:,5])
w_3_mean = np.mean(opt_pars[:,6])
delta_mean = np.mean(opt_pars[:,7])
param_means = (a_0_mean, a_1_mean, a_5_mean, w_1_mean, w_2_mean, w_3_mean, delta_mean)

a_0_std = np.std(opt_pars[:,1])
a_1_std = np.std(opt_pars[:,2])
a_5_std = np.std(opt_pars[:,3])
w_1_std = np.std(opt_pars[:,4])
w_2_std = np.std(opt_pars[:,5])
w_3_std = np.std(opt_pars[:,6])
delta_std = np.std(opt_pars[:,7])
param_stds = (a_0_std, a_1_std, a_5_std, w_1_std, w_2_std, w_3_std, delta_std)

## Save the parameter means and standard deviations to text files
### Patient F Data
np.savetxt('/users/xparcvr6/bangsgaard2017/param-means-patient-f.txt', param_means)
np.savetxt('/users/xparcvr6/bangsgaard2017/param-stds-patient-f.txt', param_stds)

## Save the Optimized Parameters to Text Files
### Patient F Data
np.savetxt('/users/xparcvr6/bangsgaard2017/opt-pars-patient-f.txt', opt_pars)
np.savetxt('/users/xparcvr6/bangsgaard2017/sims-crh-patient-f.txt', sims_crh)
np.savetxt('/users/xparcvr6/bangsgaard2017/sims-acth-patient-f.txt', sims_acth)
np.savetxt('/users/xparcvr6/bangsgaard2017/sims-cort-patient-f.txt', sims_cort)

## Compute total wall time
end_time = time.time()
wall_time = end_time - start_time
print("Walltime: ", wall_time)

