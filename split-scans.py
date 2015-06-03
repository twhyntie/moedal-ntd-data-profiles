#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 MoEDAL - Splitting the NTD scans

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

if __name__ == "__main__":

    print("*")
    print("*==================================*")
    print("* MoEDAL - Splitting the NTD scans *")
    print("*==================================*")

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
    lg.basicConfig(filename=os.path.join(outputpath, 'log_split-scans.log'), filemode='w', level=level)

    print("*")
    print("* Input path          : '%s'" % (datapath))
    print("* Output path         : '%s'" % (outputpath))
    print("*")

    ## The base name of the image file.
    bn = os.path.basename(datapath)

    # The image as a NumPy array.
    img = mpimg.imread(datapath)

    lg.info(" * Image '%s' dimensions: %s" % (bn, str(img.shape)))

    # Show the image (uncomment to do so).
    #plt.imshow(img)
    #plt.show()

    # Note that for the first images, the row and column limits
    # had to be hard-coded as the images were not split/joined
    # in a uniform manner. It still works though! :-)

    ## The row limits.
    row_limits = [65, 129, 194, 258, 323, 387, 452, 516]

    ## The column limits.
    col_limits = [1, 66, 130, 195, 259, 324, 389, 453, 518, 582, 647, 711]

    lg.info(" * Row    limits: %s" % str(row_limits))
    lg.info(" * Column limits: %s" % str(col_limits))

    # Split the montage into rows.
    row_imgs = np.split(img, row_limits)

    # Loop over the rows.
    for i, row_im in enumerate(row_imgs):

        # Split the row into the images.
        imgs = np.split(row_im, col_limits, axis=1)

        ## A vertical black line - artefact of the montage process?
        vert_line = imgs[0]

        # Remove the black line at the start of the row...
        imgs = imgs[1:]

        #...and add it to the last image.
        imgs[11] = np.concatenate((imgs[11], vert_line), axis=1)

        # Loop over the images.
        for j, im in enumerate(imgs):

            # Save the images.
            mpimg.imsave(os.path.join(outputpath, "00000_%02d_%02d.png" % (i, j)), im)
