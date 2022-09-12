# File Name: __init__.py
# Description: Initialization for VeVaPy, allows importing of packages with
#  a single command. Also contains basic version and help information
# Author: Christopher Parker
# Created: Mon Jan 24, 2022 | 03:38P EST
# Last Modified: Mon Sep 12, 2022 | 02:12P EDT

__version__ = '0.1'

import matplotlib
matplotlib.use('inline')

import numpy as np
import scipy.integrate as sci
import scipy.optimize as sco
from scipy.interpolate import interp1d
import time
from IPython.display import clear_output
from functools import wraps
import matplotlib.pyplot as plt
import re

from VeVaPy import DEsolver
from VeVaPy import optimize
from VeVaPy.dataImport import data
from VeVaPy.visualize import Visualizer
