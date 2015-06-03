#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 MoEDAL - Create the NTD scans subject set manifest.

 See the README.md file and the GitHub wiki for more information.

 http://moedal.web.cern.ch

"""

# Import the code needed to manage files.
import os, glob

#...for parsing the arguments.
import argparse

#...for the logging.
import logging as lg

if __name__ == "__main__":

    print("*")
    print("*=========================================*")
    print("* MoEDAL - Creating the NTD scan manifest *")
    print("*=========================================*")

    # Get the datafile path from the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("inputPath",       help="Path to the input dataset.")
    parser.add_argument("outputPath",      help="The path for the output files.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The path to the data file.
    datapath = args.inputPath

    # Check if the output directory exists. If it doesn't, quit.
    if not os.path.isdir(datapath):
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
    lg.basicConfig(filename=os.path.join(outputpath, 'log_create-manifest.log'), filemode='w', level=level)

    print("*")
    print("* Input path          : '%s'" % (datapath))
    print("* Output path         : '%s'" % (outputpath))
    print("*")

    ## The manifest string - including header row.
    ms = "id,row_id,col_id,magnification,filename\n"

    # Loop over the scans.
    for i, fn in enumerate(sorted(glob.glob(os.path.join(datapath, "*.png")))):

        ## The base name.
        bn = os.path.basename(fn)

        ## The scan ID. TODO - formalise this definition...
        my_id = bn.split(".")[0]

        # Extract the metadata from the ID. FIXME.
        file_id, row_id, col_id = my_id.split("_")

        # Add the metadata to the manifest string.
        ms += "%s,%d,%d,5,%s\n" % (my_id, int(row_id), int(col_id), bn)

    # Write the manifest file.
    with open(os.path.join(outputpath, "manifest.csv"), "w") as mf:
        mf.write(ms)
