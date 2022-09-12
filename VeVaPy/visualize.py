# File Name: visualize.py
# Description: Contains a class for creating graphs of model simulations,
#  with or without real-world data displayed, also
# Author: Christopher Parker
# Created: Sat Aug 27, 2022 | 04:25P EDT
# Last Modified: Mon Sep 12, 2022 | 04:59P EDT

from IPython.display import clear_output
from functools import wraps
import numpy as np
import matplotlib.pyplot as plt
import re
import inspect


class Visualizer:
    """
    This class will walk the user through the inputs necessary to plot simulation
    data against real-world data for the purposes of model verification and 
    validation. 

    Because the module exists in a separate namespace than the code using it,
    we unfortunately need to pass in the dictionary containing the variables
    defined in the global namespace for the main code. This will allow the
    user to type in strings to input boxes and have that retrieve the values
    saved in variables
    """
    def __init__(self, globals_input):
        # I'm going to have the class get a bunch of inputs from the user here, so they don't have to pass arguments
        # Basically, that's because it would take a lot of arguments to get all the information needed, and this will
        #  make things more legible, and easier to understand.

        # This loop structure will keep requesting that the user input the indices of the variables to graph until
        #  the input is correct (must be integers >= 0)
        self.globals_dict = globals_input
        while True:
            try:
                # Tell the user what input to enter and then save that input into the variable self.var_indices
                self.var_indices = input("Indices (in the array y0) of the variables you wish to plot (\033[1mNote that Python indexing starts at 0!\033[0m): ")

                # Convert the user input into a list of integers by separating at the commas
                self.var_indices = [int(i) for i in list(self.var_indices.split(','))]

                # Ensure that all list entries are zero or greater, now that we know they are integers
                for entry in self.var_indices:
                    if entry < 0:
                        raise ValueError

            # If a ValueError is raised by the input function receiving an invalid value, then we print an error message
            #  and start back at the beginning of the while True loop
            except ValueError:
                # We use this function to clear the output in the Jupyter notebook often, so that it doesn't get cluttered,
                #  and remains easy to read
                clear_output()
                # Print the error message in bold (hence the strange escape codes at the start and end of this string)
                print("\033[1mInput must be an integer or a comma-separated list of integers, zero or greater and matching in number the input for number of graphs\033[0m")
                continue

            # Set a variable for the number of graphs requested, this will come in handy later
            self.num_graphs = len(self.var_indices)

            # We only break out of the while True loop if we don't go through except ValueError
            clear_output()
            break

        while True:
            try:
                # Ask the user for the name of the array containing data to plot
                self.array_name = input("Enter the name of the array to be graphed (simData_all for optimized simulations, data_no_opt for non-optimized)")
                # This line just checks if the name given by the user has been used somewhere in the code. If not,
                #  it will raise a KeyError, and we will try again.
                self.globals_dict[self.array_name]
            except KeyError:
                clear_output()
                # Print the error message in bold (hence the strange escape codes at the start and end of this string)
                print("\033[1mMust enter the name of a globally defined array\033[0m")
                continue
            clear_output()
            break

        while True:
            try:
                # Ask the user how many iterations of parameter optimization are contained in the array
                #  (Prompt the user to answer 0 for no parameter optimization)
                # This will raise a ValueError for anything other than an integer
                self.num_iters = int(input(f"Number of iterations of parameter optimization contained in {self.array_name} (Enter 0 for no optimization): "))

                # If the number given is negative, raise a ValueError, also
                if self.num_iters < 0:
                    raise ValueError

                # Check that the array has enough columns for the number of variables to be graphed
                try:
                    num_cols = len(self.globals_dict[self.array_name][0,:])
                    if num_cols < (self.num_graphs+1)*self.num_iters:
                        raise TypeError
                except TypeError:
                    clear_output()
                    print("""The array given does not have the proper number of columns for the graphs requested.
            It must contain the time steps in the first column, and then a column for each variable being graphed
            (and this same structure must be repeated for each iteration of parameter optimization).\n""")
                    continue
            # If a ValueError is raised by the input function receiving an invalid value, then we print an error message
            #  and start back at the beginning of the while True loop
            except ValueError:
                clear_output()
                # Print the error message in bold (hence the strange escape codes at the start and end of this string)
                print("\033[1mInput must be either a positive integer or zero.")
                continue
            # We only break out of the while True loop if we don't go through except ValueError
            clear_output()
            break

        while True:
            try:
                # Ask the user if they would like to include data from a real-world data set on the graphs, and the
                #  name of the data set if yes. Raises a ValueError if the input is not an integer
                self.real_data_flag = input("Graph real-world data along with simulations? (Y/N)")

                # If the input doesn't start with either y or n, we raise a ValueError. I'm only looking at the first
                #  letter to allow for typing "yes" or "no", also
                if self.real_data_flag[0].upper() != 'Y' and self.real_data_flag[0].upper() != 'N':
                    raise ValueError
            # If a ValueError is raised by the input function receiving an invalid value, then we print an error message
            #  and start back at the beginning of the while True loop
            except ValueError:
                clear_output()
                # Print the error message in bold (hence the strange escape codes at the start and end of this string)
                print("\033[1mInput must be either Y or N.")
                continue

            # If the user answered in the affirmative, set the flag to True
            if self.real_data_flag[0].upper() == 'Y':
                self.real_data_flag = True

            # If the user answered in the negative, set the flag to False
            elif self.real_data_flag[0].upper() == 'N':
                self.real_data_flag = False

                # Since no real-world data has been requested, we will just set the array name for each graph to ''
                #  to ensure we don't get any errors
                self.real_data_arrays = ['']*self.num_graphs

            # We only break out of the while True loop if we don't go through except ValueError
            clear_output()
            break

        if self.real_data_flag:
            # Define an empty list to hold any real-world data array names we might need
            self.real_data_arrays = []
            self.real_data_objects = []
            self.real_data_objectArrays = []
            self.real_data_col_numbers = []
            # If the user has indicated that they want real-world data included on one or more graphs, we need to get the
            #  arrays in which that data is stored from them and which graphs it should go on
            for i in range(self.num_graphs):
                while True:
                    try:
                        # Ask the user for the name of the first array containing real-world data
                        temp_array_name = input(f"Enter the name of real-world data array to show on graph #{i+1} (leave blank for none) and the column number of the data \
                        (\033[1mseparated by a comma!\033[0m 1 for all sets other than Nelson data): ")

                        # If the user leaves the input box blank, we skip to the next for loop iteration
                        if temp_array_name == "":
                            # Set these to "" so that it's clear that both the global namespace and object namespace
                            #  arrays are undefined in this case
                            temp_data_obj = ""
                            temp_data_array = ""
                            temp_column_number = ""
                            clear_output()
                            break

                        try:
                            # Split the array name from the column number, and make sure the column number is an integer
                            #  greater than 0
                            temp_array_name, temp_column_number = temp_array_name.split(',')

                            # This is a simple regex substitution to remove any whitespace, just in case the user
                            #  put in any spaces. Luckily int() removes them by default, so we don't need to worry
                            #  for the column number
                            temp_array_name = re.sub("\s", "", temp_array_name)
                            temp_column_number = int(temp_column_number)

                            if temp_column_number <=0:
                                raise ValueError

                        except ValueError:
                            clear_output()
                            # Print the error message in bold (hence the strange escape codes at the start and end of this string)
                            print("\033[1mRemember to enter the column number after the array name, separated by a comma\033[0m")
                            continue

                        # Check if the array is defined in the global namespace and make sure it has the proper number of
                        #  columns
                        self.globals_dict[temp_array_name][:,temp_column_number]

                        # If we make it to this statement, we know that the array given is in the global namespace,
                        #  not an object's namespace. So we will just define the object name variables as "", so that
                        #  while plotting we can check which type of array we are dealing with
                        temp_data_obj = ""
                        temp_data_array = ""

                    # If the array name is not defined in the global namespace, we need to check and see if it's an object
                    #  (such as one created from the dataImport module). These objects each have their own namespace, so
                    #  it takes a bit of extra manipulation to use them.
                    except KeyError:
                        # First, we try to split the name given by the user at a period (because an array contained
                        #  inside an instance of an object will have a name such as nelson.ACTH). The first string is the
                        #  name of an instance of an object, and the second is the array name that is hopefully contained in
                        #  the object.
                        try:
                            temp_data_obj, temp_data_array = temp_array_name.split('.')
                        # If there is no period, it will raise a ValueError, and we know that the user has input an invalid
                        #  array name, so we go back to the beginning of the while True loop
                        except ValueError:
                            clear_output()
                            # Print the error message in bold (hence the strange escape codes at the start and end of this string)
                            print("\033[1mMust enter the name of a globally defined array\033[0m")
                            continue
                        # This try statement could give us one of three different errors. If the object name given
                        #  is invalid (it doesn't have its own namespace), then it will raise a TypeError. If the
                        #  object name is valid, but has no array with the given name, then it will raise a KeyError.
                        #  If both names are valid, but the array doesn't have enough columns,
                        #  it will raise an IndexError.
                        try:
                            # Parts of this statement:
                            #     - self.globals_dict[temp_data_obj] gets the value of the variable associated with the name
                            #        stored in the string temp_data_obj
                            #     - vars() is the function to access the dictionary containing variable names and values
                            #        for the namespace of the object passed as an argument
                            #     - So by passing self.globals_dict[temp_data_obj], we are accessing the dictionary of the object
                            #        namespace of the variable named temp_data_obj
                            #     - Then we want to access a variable from the dictionary, so we index it with [temp_data_array],
                            #        which returns the value of the variable of the same name as the string stored in temp_data_array
                            #     - Now that we have the variable stored in the object and array names passed by the user, we check
                            #        to see if the column defined by temp_column_number exists, by indexing with [:,temp_column_number]
                            #        to access all rows of data contained in that column
                            #
                            # This statement is unfortunately complex, but I believe it is the best way to handle accessing arrays
                            #  stored in objects at the request of the user. We use the same format in the make_graphs function to access
                            #  the user-requested arrays for plotting.
                            vars(self.globals_dict[temp_data_obj])[temp_data_array][:,temp_column_number]
                            # At this point, we know that the array is in an object's namespace, so we will define
                            #  temp_array_name as "", so that we can check while plotting between global and object
                            #  namespace data sets
                            temp_array_name = ""
                        # First, we handle the TypeError, and tell the user that the object name is invalid.
                        except TypeError:
                            clear_output()
                            # Print the error message in bold (hence the strange escape codes at the start and end of this string)
                            print("\033[1mThe object name given is undefined. Make sure you've created an instance of the desired object!\033[0m")
                            continue
                        # Next, we handle the KeyError, and tell the user that the object has no array with the given name.
                        except KeyError:
                            clear_output()
                            # Print the error message in bold (hence the strange escape codes at the start and end of this string)
                            print("\033[1mThe object name given is valid, but doesn't contain the array you've requested!\033[0m")
                            continue
                        # Finally, we handle the IndexError, and tell the user that the array they want exists but isn't
                        #  the correct size for the column requested
                        except IndexError:
                            clear_output()
                            # Print the error message in bold (hence the strange escape codes at the start and end of this string)
                            print("\033[1mThe object and array names are both valid, but the array doesn't have the correct number of columns!\033[0m")
                            continue
                    # In this case, the variable requested by the user exists, but is not an array.
                    except TypeError:
                        clear_output()
                        # Print the error message in bold (hence the strange escape codes at the start and end of this string)
                        print("\033[1mYou've entered the name of a variable that exists, but is not an array! Remember that lists will not work here, you must use an array that contains the time steps in the first column and the data in another column\033[0m")
                        continue
                    # In this case, we know that the array defined by the user is in the global namespace, but doesn't
                    #  have the correct number of columns.
                    except IndexError:
                        clear_output()
                        # Print the error message in bold (hence the strange escape codes at the start and end of this string)
                        print("\033[1mThe array you've requested exists, but it doesn't have the correct number of columns!\033[0m")
                        continue


                    # We now break out of the while True loop. This point will be reached if we either don't go through
                    #  the except KeyError statement (the array name given is in the global namespace),
                    #  or if we do go through it and don't raise any further errors (the array name given is in an object's namespace).
                    clear_output()
                    break

                # Now that we have a temporary variable containing an array name that we know is defined in the global
                #  namespace, let's append it to the list of array names containing the real-world data to graph.
                # The list will also contain "" for those graphs with no real-world data (if any), this way we can
                #  just check later whether it has a legitimate array name in each index, and if so, we graph it on the
                #  corresponding graph index
                self.real_data_arrays.append(temp_array_name)
                self.real_data_objects.append(temp_data_obj)
                self.real_data_objectArrays.append(temp_data_array)
                self.real_data_col_numbers.append(temp_column_number)


    # This is a local decorator to check whether any of the optional arguments to make_graphs have been passed
    #  explicitly by the user. Basically, it checks the arguments passed to the function it's wrapped around and then
    #  passes on the ones explicitly defined by the user as an argument to the wrapped function.
    # Look up documentation on decorator functions in Python for more information on how this works.
    def __explicit_checker(f):
        varnames = inspect.getfullargspec(f)[0]
        # It seems like the new version of Python has broken functools, so I'll 
        #  replace this with a slightly more ugly version. We need to just tell 
        #  the decorator function that it's supposed to report the name and 
        #  docstring of the function being wrapped instead of its own.
        #@wraps(f)
        def wrapper(self, *a, **kw):
            kw['explicit_params'] = set(list(varnames[:len(a)]) + list(kw.keys()))
            return f(self, *a, **kw)

        # Here's the replacement of @wraps(f)
        wrapper.__name__ = f.__name__
        wrapper.__doc__ = f.__doc__
        return wrapper

    # Decorate the function with the __explicit_checker function, so that whenever this function is called, we are actually
    #  calling __explicit_checker first.
    @__explicit_checker
    def make_graphs(self, figure_size = (20,20), std_dev=False, xaxis_labels = [], yaxis_labels = [], sims_line_labels=["", "", "", ""], sims_line_colors=["blue", "blue", "blue", "blue"], std_labels=["Mean +- Standard Deviation", "Mean +- Standard Deviation", "Mean +- Standard Deviation", "Mean +- Standard Deviation"], real_data_labels = ["", "", "", ""], real_data_colors = ["orange", "orange", "orange", "orange"], legend_locs=["lower right", "lower right", "lower right", "lower right"], graph_titles=[], savefile = "", explicit_params=None):
        """
        This method is what the user will call to actually create and display/save the graphs. It can take optional
        arguments that allow for making the graphs more presentable (things like axis labels and line styles/colors).

        The optional arguments are all passed in the form of lists with one entry per graph being created. So for graphs
        of CRH, ACTH and cortisol, if you wanted to pass titles for the graphs reflecting that fact, you'd use
            graph_titles = ["CRH Concentration", "ACTH Concentration", "Cortisol Concentration"]

        The full list of optional arguments to the function is as follows:
            sims_line_labels (to define labels for the simulated lines on each graph)
            sims_line_colors (to change the color of the simulated lines on each graph)
            std_labels (to define labels for the +- standard deviation shaded area)
            real_data_labels (to define labels for the real-world data on each graph, include list entries for
                each graph, with or without real-world data plotted)
            real_data_colors (to define line colors for the real-world data on each graph, again only include list entries
                for graphs with real-world data plotted)
            legend_locs (to change the location that the legend is displayed on each graph, if labels are added for the lines.
                Options for location are: "upper left", "upper right", "lower left", and "lower right")
            graph_titles (to add titles above the graphs)
            xaxis_labels (to change the labels on the x-axis)
            yaxis_labels (to change the labels on the y-axis)
            figure_size (to change the width and height of the figure, must be a tuple)
        """
        # Define the list of arrays we will fill with the organized data we want to plot. For no optimization runs,
        #  we will have num_iters = 0, so just replace it with 1 in this case so we have the properly sized array
        if self.num_iters > 0:
            self.sims = [np.zeros((len(self.globals_dict[self.array_name][:,0]), self.num_iters))]*self.num_graphs
        else:
            self.sims = [np.zeros((len(self.globals_dict[self.array_name][:,0]), 1))]*self.num_graphs

        # If we are plotting a parameter optimization run with more than one iteration, we need to gather the data in
        #  an organized fashion
        if self.num_iters > 1:
            # Loop through the variables the user has requested we graph
            for index, entry in enumerate(self.var_indices):
                # This may look a bit complex, but what we are doing is gathering the columns for each variable together.
                #  Before this, each variable is in columns like 1, 5, 9, etc. and we want to fix that so we can plot more easily
                #  So this statement loops through each column from the variable's first column (entry + 1) until the last column
                #  in the array, going by the number of columns per iteration each time (total columns/number of iterations)
                self.sims[index] = [self.globals_dict[self.array_name][:,i] for i in range(entry+1,len(self.globals_dict[self.array_name][0,:]),len(self.globals_dict[self.array_name][0,:]/self.num_iters))]
        # If we are plotting a parameter optimization run with a single iteration, or a simulation without optimization,
        #  put the data into self.sims, also
        else:
            for index, entry in enumerate(self.var_indices):
                self.sims[index] = self.globals_dict[self.array_name][:,entry+1]


        # Now that we have all of the data we want to graph organized and ready, we can define the figure and set the
        #  number of subplots in it to the number of variables the user has requested we graph
        fig, axes = plt.subplots(nrows = self.num_graphs, figsize = figure_size)

        # If the user is making multiple graphs, we do the following (where we loop through the subplots in the
        #  figure)
        if self.num_graphs > 1:
            # Next, we loop through the number of graphs requested by the user, and create them.
            for index, entry in enumerate(self.sims):
                # If we have multiple iterations, we will need to graph the mean (and optionally +- standard deviation),
                #  so check the number of iterations
                if self.num_iters > 1:
                    # Here we plot the mean over all iterations
                    axes[index].plot(self.globals_dict[self.array_name][:,0], np.mean(entry, axis = 0), label = sims_line_labels[index], color = sims_line_colors[index])

                    # Check if the user wants to plot the mean +- standard deviation, if so add it to the graph
                    if std_dev:
                        axes[index].fill_between(self.globals_dict[self.array_name][:,0], np.mean(entry, axis = 0) - np.std(entry, axis = 0), np.mean(entry, axis = 0) + np.std(entry, axis = 0), alpha = 0.3, label = std_labels[index])

                # If we have 0 or 1 iteration of parameter optimization, we can simply plot the data without taking mean
                #  or worrying about standard deviation
                else:
                    axes[index].plot(self.globals_dict[self.array_name][:,0], entry, label = sims_line_labels[index], color = sims_line_colors[index])

                # Now we check if the user has requested to plot any real-world data contained in the global namespace
                #  on this subplot, and graph it if so
                if self.real_data_arrays[index]:
                    axes[index].plot(self.globals_dict[self.real_data_arrays[index]][:,0], self.globals_dict[self.real_data_arrays[index]][:,self.real_data_col_numbers[index]], label = real_data_labels[index], color = real_data_colors[index])
                # If the user hasn't requested real-world data contained in the global namespace, we check if they have
                #  requested real-world data contained in an object's namespace. If so, we graph it.
                elif self.real_data_objects[index]:
                    axes[index].plot(vars(self.globals_dict[self.real_data_objects[index]])[self.real_data_objectArrays[index]][:,0], vars(self.globals_dict[self.real_data_objects[index]])[self.real_data_objectArrays[index]][:,self.real_data_col_numbers[index]], label = real_data_labels[index], color = real_data_colors[index])

                # Check if the user specified labels for the lines being graphed, if so we turn on the legend
                if 'sims_line_labels' in explicit_params:
                    try:
                        axes[index].legend(loc = legend_locs[index], shadow = True, fancybox = True)
                    except TypeError:
                        print("\033[1mMake sure you have passed a list with one entry per variable graphed for legend_locs\033[0m")
                # Check if the user specified x-axis labels, if so we turn them on
                if 'xaxis_labels' in explicit_params:
                    try:
                        axes[index].set(xlabel = xaxis_labels[index])
                    except TypeError:
                        print("\033[1mMake sure you have passed a list with one entry per variable graphed for xaxis_labels\033[0m")
                # Check if the user specified y-axis labels, if so we turn them on
                if 'yaxis_labels' in explicit_params:
                    try:
                        axes[index].set(ylabel = yaxis_labels[index])
                    except TypeError:
                        print("\033[1mMake sure you have passed a list with one entry per variable graphed for yaxis_labels\033[0m")
                # Check if the user specified titles for the graphs, if so we turn them on
                if 'graph_titles' in explicit_params:
                    try:
                        axes[index].set(title = graph_titles[index])
                    except TypeError:
                        print("\033[1mMake sure you have passed a list with one entry per variable graphed for graph_titles\033[0m")
        # If there's only one graph to make, do basically the same as above, just don't iterate through multiple
        #  variables and subplots
        else:
            if self.num_iters > 1:
                # Here we plot the mean over all iterations
                axes.plot(self.globals_dict[self.array_name][:,0], np.mean(self.sims[0], axis = 0), label = sims_line_labels[0], color = sims_line_colors[0])

                # Check if the user wants to plot the mean +- standard deviation, if so add it to the graph
                if std_dev:
                    axes.fill_between(self.globals_dict[self.array_name][:,0], np.mean(self.sims[0], axis = 0) - np.std(self.sims[0], axis = 0), np.mean(self.sims[0], axis = 0) + np.std(self.sims[0], axis = 0), alpha = 0.3, label = std_labels[0])
            # If we have 0 or 1 iteration of parameter optimization, we can simply plot the data without taking mean
            #  or worrying about standard deviation
            else:
                axes.plot(self.globals_dict[self.array_name][:,0], self.sims[0], label = sims_line_labels[0], color = sims_line_colors[0])

            # Now we check if the user has requested to plot any real-world data contained in the global namespace,
            #  and graph it if so
            if self.real_data_arrays[0]:
                axes.plot(self.globals_dict[self.real_data_arrays[0]][:,0], self.globals_dict[self.real_data_arrays[0]][:,self.real_data_col_numbers[0]], label = real_data_labels[0], color = real_data_colors[0])
            # If the user hasn't requested real-world data contained in the global namespace, we check if they have
            #  requested real-world data contained in an object's namespace. If so, we graph it.
            elif self.real_data_objects[0]:
                axes.plot(vars(self.globals_dict[self.real_data_objects[0]])[self.real_data_objectArrays[0]][:,0], vars(self.globals_dict[self.real_data_objects[0]])[self.real_data_objectArrays[0]][:,self.real_data_col_numbers[0]], label = real_data_labels[0], color = real_data_colors[0])

            # Check if the user specified labels for the lines being graphed, if so we turn on the legend
            if 'sims_line_labels' in explicit_params:
                try:
                    axes.legend(loc = legend_locs[0], shadow = True, fancybox = True)
                except TypeError:
                    print("\033[1mDespite only graphing a single variable, you still need to pass legend_locs as a list with one entry, sorry!\033[0m")
            # Check if the user specified x-axis labels, if so we turn them on
            if 'xaxis_labels' in explicit_params:
                try:
                    axes.set(xlabel = xaxis_labels[0])
                except TypeError:
                    print("\033[1mDespite only graphing a single variable, you still need to pass xaxis_labels as a list with one entry, sorry!\033[0m")
            # Check if the user specified y-axis labels, if so we turn them on
            if 'yaxis_labels' in explicit_params:
                try:
                    axes.set(ylabel = yaxis_labels[0])
                except TypeError:
                    print("\033[1mDespite only graphing a single variable, you still need to pass yaxis_labels as a list with one entry, sorry!\033[0m")
            # Check if the user specified titles for the graphs, if so we turn them on
            if 'graph_titles' in explicit_params:
                try:
                    axes.set(title = graph_titles[0])
                except TypeError:
                    print("\033[1mDespite only graphing a single variable, you still need to pass graph_titles as a list with one entry, sorry!\033[0m")

        # If the user has defined a filename, save the generated graphs with it
        if 'savefile' in explicit_params:
            plt.savefig(savefile, dpi=300)


