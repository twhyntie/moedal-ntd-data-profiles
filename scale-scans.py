#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 MoEDAL - Scaling the NTD scans.

 See the README.md file and the GitHub wiki for more information.

 http://moedal.web.cern.ch

"""

# Import the code needed to manage files.
import os, glob

#...for parsing the arguments.
import argparse

#...for the logging.
import logging as lg

#...for the plotting.
import matplotlib.pyplot as plt

#...for the image manipulation.
import matplotlib.image as mpimg

#...for the MATH.
import numpy as np

import scipy.ndimage.interpolation as inter

if __name__ == "__main__":

    print("*")
    print("*================================*")
    print("* MoEDAL - Scaling the NTD scans *")
    print("*================================*")

    # Get the datafile path from the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("inputPath",       help="Path to the input dataset.")
    parser.add_argument("outputPath",      help="The path for the output files.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The path to the data file.
    datapath = args.inputPath

    # Check if the output directory exists. If it doesn't, quit.
    if not os.path.exists(datapath):
        raise IOError("* ERROR: input file '%s' does not exist!" % (datapath))

    ## The output path.
    outputpath = args.outputPath

    # Check if the output directory exists. If it doesn't, quit.
    if not os.path.isdir(outputpath):
        raise IOError("* ERROR: '%s' output directory does not exist!" % (outputpath))

    # Set the logging level.
    if args.verbose:
        level=lg.DEBUG
    else:
        level=lg.INFO

    # Configure the logging.
    lg.basicConfig(filename=os.path.join(outputpath, 'log_scale-scans.log'), filemode='w', level=level)

    print("*")
    print("* Input path          : '%s'" % (datapath))
    print("* Output path         : '%s'" % (outputpath))
    print("*")

    ## The scale factor.
    scale = 6.0

    # Loop over the individual scan images.
    for i, fn in enumerate(sorted(glob.glob(os.path.join(datapath, "*.png")))):

        ## The base name.
        bn = os.path.basename(fn)

        ## The scan image to be scaled.
        img = mpimg.imread(fn)

        # The scaled image - no interpolation or pre-filtering.
        zoom_img = inter.zoom(img, (scale, scale, 1.0), order=0, prefilter=False)

        # Save the image.
        mpimg.imsave(os.path.join(outputpath, bn), zoom_img)

        #break
