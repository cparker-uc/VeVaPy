# File Name: ODEsolver.py
# Description: this file will contain a function that performs the ODE solver
#   steps to improve readability in the model notebooks
# Author: Christopher Parker
# Created: Mon Jan 24, 2022 | 03:39P EST
# Last Modified: Thu Jan 27, 2022 | 09:31P EST

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

import scipy.integrate as sci
import numpy as np

def solve(ode_system, ics, t_start, t_step, t_end, y_index0 = 0, y_index1 = 1, y_index2 = 2, tau0 = 0, tau1 = 0, tau2 = 0, delay = [False, False, False], delay_rough = False):
    # Define global variables for delayed ACTH and CORT values.
    if delay[0] or delay[1] or delay[2]:
        global delayedCRH, delayedACTH, delayedCORT
        delayedCRH = ics[y_index0]
        delayedACTH = ics[y_index1]
        delayedCORT = ics[y_index2]
        # These variables will be used to hold the previous index in the time
        #  array at which we found the delayed values of ACTH and CORT, resp.
        t_index0 = 0
        t_index1 = 0
        t_index2 = 0

    # Initialize empty arrays for storing values of ts and ys.
    ts = []
    ys = []

    solver = sci.ode(ode_system)
    solver.set_integrator('vode', method='bdf', atol=3e-12, rtol=1e-12, nsteps=100000)
    solver.set_initial_value(ics, t_start)

    while solver.successful() and solver.t < t_end:
        # We also check whether the delay_rough flag is set, and depending on this
        #  we either run the normal version of the delay functions or the _rough
        #  version.
        # If the user sets the index 0 delay flag to True, we compute the delayed 
        #  value of CRH
        if delay[0] and delay_rough:
            delayedCRH, t_index0 = delay_CRH_rough(solver.t, tau0, ts, ys, ics, t_index0, y_index0)
        elif delay[0] and not delay_rough:
            delayedCRH, t_index0 = delay_CRH(solver.t, tau0, ts, ys, ics, t_index0, y_index0)

        # If the user sets the index 1 delay flag to True, we compute
        #  the delayed value of ACTH
        if delay[1] and delay_rough:
            delayedACTH, t_index1 = delay_ACTH_rough(solver.t, tau1, ts, ys, ics, t_index1, y_index1)
        elif delay[1] and not delay_rough:
            delayedACTH, t_index1 = delay_ACTH(solver.t, tau1, ts, ys, ics, t_index1, y_index1)

        # If the user sets the index 2 delay flag to True, we compute the delayed
        #  value of CORT
        if delay[2] and delay_rough:
            delayedCORT, t_index2 = delay_CORT_rough(solver.t, tau2, ts, ys, ics, t_index2, y_index2)
        elif delay[2] and not delay_rough:
            delayedCORT, t_index2 = delay_CORT(solver.t, tau2, ts, ys, ics, t_index2, y_index2)


        solver.integrate(solver.t + t_step)
        ts.append(solver.t)
        ys.append(solver.y)

    # reshape the output from sci.ode to an array with the times in the first
    #  column
    ts = np.reshape(ts, (len(ts), 1))
    ys = np.vstack(ys)
    timeSeries = np.hstack((ts, ys))

    return timeSeries

# Let's put all of the code to determine the delayed value of ACTH into a 
#  function to keep everything readable.
def delay_ACTH(t, tau1, ts, ys, ics, t_index1, y_index1):
    # t_round is equal to t rounded down to the nearest multiple of 0.01.
    # This is necessary because as the ODE solver is running, it uses much 
    #  smaller steps than 0.01 at times (especially when the system is 
    #  very stiff).
    t_round = t - t%0.01

    # Generate an array of values near to t_round - tau1, in case we skipped 
    #  the exact time step.
    #t_tau1 = np.arange(t_round - tau1 - 0.01, t_round - tau1 + 0.01, 0.01)
    t_tau1 = np.arange(t_round - tau1, t_round - tau1 + 0.01, 0.01)

    # First, we check if t_round is greater than tau1.
    # If it isn't, we will just use the initial time point of y[1] until it is.
    if t_round > tau1:
        # This for statement iterates through the array of previously solved 
        #  time steps (saved in the array ts).
        for ts_index, ts_item in enumerate(ts[t_index1:]):
            # First, try to match the exact time step t - tau1.
            if (ts_item - ts_item%0.01) == (t_round - tau1 - (t_round - tau1)%0.01):
                # Now that we have found the correct time step for the delay, 
                #  we set a variable delayedACTH to the value of y[1] from the delayed 
                #  time step, and set t_index1 to the index in ts at which we 
                #  found it.
                delayedACTH = ys[ts_index + t_index1][y_index1]
                t_index1 = ts_index + t_index1

                # end the for loop now that we have found a match
                break
        # If we didn't find an exact match, try finding a match within 
        #  0.01 minutes of the exact time.
        else:
            for ts_index, ts_item in enumerate(ts[t_index1:]):
                # Let's try using a double for loop so that we can round both 
                #  the value from ts and the value of t - tau1 because we seem 
                #  to be suffering from lots of rounding error because 
                #  computers can't handle floats exactly.
                for ttau1_item in t_tau1:
                    # Check if we have a solved time step within 0.01 minutes 
                    #  of t - tau1 (we may not have an exact match, it seems to 
                    #  iterate more than 0.01 in a step at times).
                    # Note that we round ts_item and ttau1_item down to the 
                    #  nearest multiple of 0.01 because of rounding error.
                    if (ts_item - ts_item%0.01) == (ttau1_item - ttau1_item%0.01):
                        # Now that we have found the correct time step for the 
                        #  delay, we set a variable delayedACTH to the value of y[1] 
                        #  from the delayed time step, and set t_index1 to the 
                        #  index in ts at which we found it.

                        delayedACTH = ys[ts_index + t_index1][y_index1]
                        t_index1 = ts_index + t_index1

                        # End the for loop early now that we have found a match.
                        break
                # This is a useful bit of code to break out of a double for 
                #  loop if we succeeded in doing what we wanted. If the code 
                #  makes it to the break inside the if statement, we do not run 
                #  this else statement and instead break out of the outer for 
                #  loop. If we do not make it to the break inside the if 
                #  statement, we run the else statement and continue to the 
                #  next step of the outer for loop, skipping the break below.
                else:
                    continue

                break

            # Same idea as explained above, if we don't break out of the for 
            #  loop, run this code.
            # If we are running this, it means we didn't find a match 
            #  within 0.01 of t - tau1.
            else:
                # Expand the range of values around the delayed time step we 
                #  are willing to accept.
                #t_tau1 = np.arange(t_round - tau1 - 0.1, t_round - tau1 + 0.1, 0.01)
                t_tau1 = np.arange(t_round - tau1, t_round - tau1 + 0.1, 0.01)

                # Now we simply run the same for loop as above.
                for ts_index, ts_item in enumerate(ts[t_index1:]):
                    for ttau1_item in t_tau1:
                        if (ts_item - ts_item%0.01) == (ttau1_item - ttau1_item%0.01):
                            delayedACTH = ys[ts_index + t_index1][y_index1]
                            t_index1 = ts_index + t_index1

                            break
                    else:
                        continue
                    break

                # If we don't have a match within 0.1 minutes, set delayedACTH 
                #  to the initial value for ACTH and tell the user that there's
                #  a problem.
                #
                # Comment this code out if expanding the search range further 
                #  by uncommenting the code below.
                else:
                    delayedACTH = ics[y_index1]
                    print("No match for y[{}] delayed by tau1 within 0.1 minutes".format(y_index1))

    # If t_round <= tau1, just use the initial value for y[1]
    else:
        delayedACTH = ics[y_index1]

    return delayedACTH, t_index1

# In case any model needs to use delayed values for CRH, we will include a 
#  function here to find those--it will be just like the ACTH delay function
def delay_CRH(t, tau0, ts, ys, ics, t_index0, y_index0):
    t_round = t - t%0.01
    t_tau0 = np.arange(t_round - tau0 - 0.5, t_round - tau0 + 0.5, 0.5)

    if t_round > tau0:
        for ts_index, ts_item in enumerate(ts[t_index0:]):
            if (ts_item - ts_item%0.5) == (t_round - tau0 - (t_round - tau0)%0.5):
                delayedCRH = ys[ts_index + t_index0][y_index0]
                t_index0 = ts_index + t_index0
                break
        else:
            for ts_index, ts_item in enumerate(ts[t_index0:]):
                for ttau0_item in t_tau0:
                    if (ts_item - ts_item%0.5) == (ttau0_item - ttau0_item%0.5):
                        delayedCRH = ys[ts_index + t_index0][y_index0]
                        t_index0 = ts_index + t_index0
                        break
                else:
                    continue
                break
            else:
                t_tau0 = np.arange(t_round - tau0 - 1, t_round - tau0 + 1, 0.5)
                for ts_index, ts_item in enumerate(ts[t_index0:]):
                    for ttau0_item in t_tau0:
                        if (ts_item - ts_item%0.5) == (ttau0_item - ttau0_item%0.5):
                            delayedCRH = ys[ts_index + t_index0][y_index0]
                            t_index0 = ts_index + t_index0
                            break
                    else:
                        continue
                    break
                else:
                    delayedCRH = ics[y_index0]
                    print("No match for y[{}] delayed by tau0 within 1 minute.".format(y_index0))
    else:
        delayedCRH = ics[y_index0]

    return delayedCRH

# Same as delay_ACTH, but for tau2 now (which is a longer delay) and now we are 
#  concerned with setting y[2], since the tau2 delay is the delay in 
#  cortisol action.
def delay_CORT(t, tau2, ts, ys, ics, t_index2, y_index2):
    t_round = t - t%0.01
    #t_tau2 = np.arange(t_round - tau2 - 0.01, t_round - tau2 + 0.01, 0.01)
    t_tau2 = np.arange(t_round - tau2, t_round - tau2 + 0.01, 0.01)

    if t_round > tau2:
        for ts_index, ts_item in enumerate(ts[t_index2:]):
            if (ts_item - ts_item%0.01) == (t_round - tau2 - (t_round - tau2)%0.01):
                delayedCORT = ys[ts_index + t_index2][y_index2]
                t_index2 = ts_index + t_index2
                break
        else:
            for ts_index, ts_item in enumerate(ts[t_index2:]):
                for ttau2_item in t_tau2:
                    if (ts_item - ts_item%0.01) == (ttau2_item - ttau2_item%0.01):
                        delayedCORT = ys[ts_index + t_index2][y_index2]
                        t_index2 = ts_index + t_index2
                        break
                else:
                    continue
                break
            else:
                #t_tau2 = np.arange(t_round - tau2 - 0.1, t_round - tau2 + 0.1, 0.01)
                t_tau2 = np.arange(t_round - tau2, t_round - tau2 + 0.1, 0.01)
                for ts_index, ts_item in enumerate(ts[t_index2:]):
                    for ttau2_item in t_tau2:
                        if (ts_item - ts_item%0.01) == (ttau2_item - ttau2_item%0.01):
                            delayedCORT = ys[ts_index + t_index2][y_index2]
                            t_index2 = ts_index + t_index2
                            break
                    else:
                        continue
                    break
                else:
                    delayedCORT = ics[y_index2]
                    print("No match for y[{}] delayed by tau2 within 0.1 minutes".format(y_index2))

    # if t_round <= tau2, just use the initial value for y[2]
    else:
        delayedCORT = ics[y_index2]

    return delayedCORT, t_index2

# These functions check fewer time steps around t_round - tau1 in order to improve
#  runtime. Other than using %0.5 instead of %0.01, the functions are identical.
def delay_ACTH_rough(t, tau1, ts, ys, ics, t_index1, y_index1):
    t_round = t - t%0.5
    t_tau1 = np.arange(t_round - tau1 - 0.5, t_round - tau1 + 0.5, 0.5)

    if t_round > tau1:
        for ts_index, ts_item in enumerate(ts[t_index1:]):
            if (ts_item - ts_item%0.5) == (t_round - tau1 - (t_round - tau1)%0.5):
                delayedACTH = ys[ts_index + t_index1][y_index1]
                t_index1 = ts_index + t_index1
                break
        else:
            for ts_index, ts_item in enumerate(ts[t_index1:]):
                for ttau1_item in t_tau1:
                    if (ts_item - ts_item%0.5) == (ttau1_item - ttau1_item%0.5):
                        delayedACTH = ys[ts_index + t_index1][y_index1]
                        t_index1 = ts_index + t_index1
                        break
                else:
                    continue
                break
            else:
                t_tau1 = np.arange(t_round - tau1 - 1, t_round - tau1 + 1, 0.5)

                for ts_index, ts_item in enumerate(ts[t_index1:]):
                    for ttau1_item in t_tau1:
                        if (ts_item - ts_item%0.5) == (ttau1_item - ttau1_item%0.5):
                            delayedACTH = ys[ts_index + t_index1][y_index1]
                            t_index1 = ts_index + t_index1
                            break
                    else:
                        continue
                    break
                else:
                    delayedACTH = ics[y_index1]
                    print("No match for y[{}] delayed by tau1 within 1 minute.".format(y_index1))
    else:
        delayedACTH = ics[y_index1]

    return delayedACTH, t_index1

def delay_CRH_rough(t, tau0, ts, ys, ics, t_index0, y_index0):
    t_round = t - t%0.5
    t_tau0 = np.arange(t_round - tau0 - 0.5, t_round - tau0 + 0.5, 0.5)

    if t_round > tau0:
        for ts_index, ts_item in enumerate(ts[t_index0:]):
            if (ts_item - ts_item%0.5) == (t_round - tau0 - (t_round - tau0)%0.5):
                delayedCRH = ys[ts_index + t_index0][y_index0]
                t_index0 = ts_index + t_index0
                break
        else:
            for ts_index, ts_item in enumerate(ts[t_index0:]):
                for ttau0_item in t_tau0:
                    if (ts_item - ts_item%0.5) == (ttau0_item - ttau0_item%0.5):
                        delayedCRH = ys[ts_index + t_index0][y_index0]
                        t_index0 = ts_index + t_index0
                        break
                else:
                    continue
                break
            else:
                t_tau0 = np.arange(t_round - tau0 - 1, t_round - tau0 + 1, 0.5)
                for ts_index, ts_item in enumerate(ts[t_index0:]):
                    for ttau0_item in t_tau0:
                        if (ts_item - ts_item%0.5) == (ttau0_item - ttau0_item%0.5):
                            delayedCRH = ys[ts_index + t_index0][y_index0]
                            t_index0 = ts_index + t_index0
                            break
                    else:
                        continue
                    break
                else:
                    delayedCRH = ics[y_index0]
                    print("No match for y[{}] delayed by tau0 within 1 minute.".format(y_index0))
    else:
        delayedCRH = ics[y_index0]

    return delayedCRH, t_index0

def delay_CORT_rough(t, tau2, ts, ys, ics, t_index2, y_index2):
    t_round = t - t%0.5
    t_tau2 = np.arange(t_round - tau2 - 0.5, t_round - tau2 + 0.5, 0.5)

    if t_round > tau2:
        for ts_index, ts_item in enumerate(ts[t_index2:]):
            if (ts_item - ts_item%0.5) == (t_round - tau2 - (t_round - tau2)%0.5):
                delayedCORT = ys[ts_index + t_index2][y_index2]
                t_index2 = ts_index + t_index2
                break
        else:
            for ts_index, ts_item in enumerate(ts[t_index2:]):
                for ttau2_item in t_tau2:
                    if (ts_item - ts_item%0.5) == (ttau2_item - ttau2_item%0.5):
                        delayedCORT = ys[ts_index + t_index2][y_index2]
                        t_index2 = ts_index + t_index2
                        break
                else:
                    continue
                break
            else:
                t_tau2 = np.arange(t_round - tau2 - 1, t_round - tau2 + 1, 0.5)
                for ts_index, ts_item in enumerate(ts[t_index2:]):
                    for ttau2_item in t_tau2:
                        if (ts_item - ts_item%0.5) == (ttau2_item - ttau2_item%0.5):
                            delayedCORT = ys[ts_index + t_index2][y_index2]
                            t_index2 = ts_index + t_index2
                            break
                    else:
                        continue
                    break
                else:
                    delayedCORT = ics[y_index2]
                    print("No match for y[{}] delayed by tau2 within 1 minute.".format(y_index2))
    else:
        delayedCORT = ics[y_index2]

    return delayedCORT, t_index2