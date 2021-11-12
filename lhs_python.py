#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 14:17:57 2017

@author: johntrimmer
If you have questions, feel free to send me an email: jtrimme2@illinois.edu
"""

import numpy as np
import copy
from doe_lhs import *
from scipy import stats
import matplotlib.pyplot as plt

# LHS function to generate uniform distribution
def lhs_uniform(xmin, xmax, nsample):
    lhd = lhs(1, samples = nsample) # Generates n samples for each variable
    start = xmin  # defines the starting location of the distribution, at xmin
    width = xmax - xmin  # defines the total width of the distribution, from xmin to xmax
    lhd = stats.uniform.ppf(lhd, loc = start, scale = width)  # scales lhd to correspond to starting location and width
    return lhd

# LHS function to generate triangular distribution
def lhs_triangle(xmin, probable, xmax, nsample):
    lhd = lhs(1, samples = nsample) # Generates n samples for each variable
    start = xmin  # defines the starting location of the distribution, at xmin
    width = xmax - xmin  # defines the total width of the distribution, from xmin to xmax
    mode_loc = (probable - xmin) / (xmax - xmin)  # defines the location of the most probable value
    lhd = stats.triang.ppf(lhd, mode_loc, loc = start, scale = width)  # scales lhd to generate triangular distribution
    return lhd

# LHS function to generate normal distribution
#   optionally, xmin and xmax can be specified to truncate the distribution;
#   if they are not specified, the distribution will not be truncated
def lhs_normal(mean, stdev, nsample, xmin = -np.inf, xmax = np.inf):
    lhd = lhs(1, samples = nsample) # Generates n samples for each variable
    if np.isnan(xmin):
        xmin = -np.inf  # if xmin is not a number, set equal to default value (-inf)
    if np.isnan(xmax):
        xmax = np.inf  # if xmax is not a number, set equal to default value (inf)
    a = (xmin - mean) / stdev  # defines the location of the minimum value relative to standard normal distribution
    b = (xmax - mean) / stdev  # defines the location of the maximum value relative to standard normal distribution
    lhd = stats.truncnorm.ppf(lhd, a, b, loc = mean, scale = stdev)
    return lhd

