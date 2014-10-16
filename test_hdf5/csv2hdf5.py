#!/usr/bin/env python
#
# Read a text file and copy the contents to a HDF5 file with one
# dataset for each column. Dataset names are taken from column
# headings in the input file.
#
import h5py
import getopt
import sys
import string
from numpy import *

def print_usage():
    print """
Usage: csv2hdf5.py -i <infile> -o <outfile> [-t <column_types>] [-d]
       [-g <group>] [-a] [-s <separator>]

Reads a text file and outputs the columns as HDF5 datasets.

OPTIONS

-i <infile>       The name of the input file
-o <outfile>      The name of the output file
-t <column_types> A string which specifiles the data type of each column.
                  Can also be used to skip columns (see below).
-d                If this is set the input file is read and the types
                  and names of the output datasets are reported but no output
                  will be written.
-g <group name>   Specifies the name of the group in the HDF5 file
                  which the output should be written to. The group will be
                  created if necessary.
-a                If this is set the output datasets will be appended to
                  the output file, which must already exist. Without
                  this flag the output file will be created and must NOT
                  already exist.
-s                Specifies the character used to separate columns. If not
                  set, it is assumed that columns are separated by one or more
                  whitespace characters. Note that this is not the same as
                  setting the separator to be a single space character.
-n                Specifies the names of the columns. Should be a string with
                  the names separated by commas. Columns to be skipped (i.e.
                  those with an x in the type string) should be omitted.
                  Overrides column names in the file.

DATA TYPES

The HDF5 data type to use for each column is guessed by reading the first
part of the file. This can be overridden with the -t option. If -t is used
<column_types> should be a string with one character for each column, where
the character indicates the data type to use for that column:

i: 4 byte integer
l: 8 byte long integer
f: 4 byte floating point
x: indicates that the corresponding column should be skipped

DATASET NAMES

If the -n flag is not used dataset names are taken from column headings
in the input file. Comment lines are assumed to start with '#', and it is
assumed that the last comment line at the top of the file contains the
column names.

"""

input_buffer_size = 100000000
hdf5_chunk_size   = 100000

def main():

    type_name = {}
    type_name['i'] = "integer"
    type_name['l'] = "long"
    type_name['f'] = "real"
    type_name['x'] = "skip"

    # Get command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "dao:i:t:g:s:n:", "")
    except getopt.GetoptError, err:
        print_usage()
        print str(err)
        print
        sys.exit(2)
        
    infilename   = None
    outfilename  = None
    typestring   = None
    dryrun       = False
    add_datasets = False
    separator    = None
    groupname    = ""
    column_names = None
    for (name,value) in opts:
        if name == "-o":
            outfilename = value
        elif name == "-i":
            infilename = value
        elif name == "-t":
            typestring = value
        elif name == "-d":
            dryrun = True
        elif name == "-a":
            add_datasets = True
        elif name == "-g":
            groupname = value
        elif name == "-s":
            separator = value
        elif name == "-n":
            column_names = value.split(",")

    if not(infilename):
        print_usage()
        print "Please specify an input filename with the -i option"
        print
        sys.exit(2)
    if not(outfilename) and not(dryrun):
        print_usage()
        print "Please specify an output filename with the -o option"
        print
        sys.exit(2)

    # Count header lines
    csvfile = open(infilename)
    nline = 0
    line  = csvfile.readline().lstrip()
    while line[0] == '#':
        nline = nline + 1
        line = csvfile.readline().lstrip()

    # Read last header line
    csvfile.seek(0)
    for i in range(nline):
        last_header = csvfile.readline().lstrip()
        
    # Record where data starts
    data_start = csvfile.tell()

    # Get column names
    if column_names == None:
        # Take names from header
        if nline == 0:
            print "File must have column headers if -n flag is not used"
            sys.exit(1)
        column_names = last_header.lstrip('#').split(separator)
    elif typestring != None:
        # If typestring is set need to take into account
        # any columns to be skipped (typestring=x)
        new_names = []
        i = 0
        for t in typestring:
            if t != "x":
                new_names.append(column_names[i])
                i = i + 1
            else:
                new_names.append(None)
        column_names = new_names

    # No. of columns
    ncols = len(column_names)

    # Make string for use with -n flag
    namestring = ""
    for name in column_names:
        if name != None:
            namestring = namestring + name + ","
    namestring = namestring.rstrip(',')

    if not(typestring):
        # Guess types by reading some lines
        lines = csvfile.readlines(100000)

        # Use rows to guess type of each column        
        is_int   = [True for x in range(ncols)]
        is_float = [True for x in range(ncols)]
        unknown  = [True for x in range(ncols)]
        max_val  = [0    for x in range(ncols)]
        for line in lines:
            thisline = line.split(separator)
            for i in range(ncols):
                field = thisline[i]
                try:
                    data = int(field)
                except ValueError:
                    is_int[i] = False
                else:
                    max_val[i] = max(max_val[i], abs(data))
                try:
                    data = float(field)
                except ValueError:
                    is_float[i] = False
                else:
                    max_val[i] = max(max_val[i], abs(data))

        # Check for columns we can't interpret
        for i in range(ncols):
            unknown[i] = not(is_int[i]) and not(is_float[i])
        if any(unknown):
            print "Unable to determine type for column"
            sys.exit(4)

        # Decide data types
        dtypes   = []
        for i in range(ncols):
            if is_int[i]:
                # Use 64 bit integers for large values
                if max_val[i] < (2**31)-1:
                    dtype = 'i'
                else:
                    dtype = 'l'
            else:
                dtype = 'f'
            dtypes.append(dtype)
        typestring = string.join(dtypes,'')
    else:
        # Get types from type string
        dtypes = []
        for i in range(ncols):
            dtypes.append(typestring[i:i+1])

    # Go back to start of file
    csvfile.seek(data_start)

    # Summary of columns
    print
    print "Columns to read:"
    print
    for i in range(ncols):
        print "{icol:5} : {name:20} {dtype:10} => {dset:40}".format(icol=i,
                                                                    name=column_names[i],
                                                                    dtype=type_name[dtypes[i]],
                                                                    dset=groupname + "/" + column_names[i])
    print
    print "Type string for -t option : ",typestring
    print
    print "Column names for -n option: ",namestring
    print

    if dryrun:
        print "Stopping because -d flag is set"
        sys.exit(0)

    # Open or create the output file
    if add_datasets:
        # Open existing file in writeable mode
        try:
            hdf5file  = h5py.File(outfilename, 'r+')
        except h5py.H5Error:
            print "Unable to open file: ",outfilename
            sys.exit(1)
    else:
        # Create file, fail if it already exists
        try:
            hdf5file  = h5py.File(outfilename, 'w-')
        except h5py.H5Error:
            print "Unable to create new file: ",outfilename
            sys.exit(1)

    # Make sure the group exists
    if groupname != "":
        try:
            hdf5file.create_group(groupname)
        except h5py.H5Error:
            pass

    # Create new datasets
    datasets = []
    for i in range(ncols):
        if dtypes[i] != 'x':
            dsname = groupname + "/" + column_names[i]
            if dtypes[i] == "i":
                dtype = int32
            elif dtypes[i] == "l":
                dtype = int64
            else:
                dtype = float32
            try:
                ds = hdf5file.create_dataset(dsname, shape=(0,), dtype=dtype,
                                             chunks=(hdf5_chunk_size,), maxshape=(None,),
                                             compression='gzip',
                                             compression_opts=6)
            except h5py.H5Error:
                print "Unable to create dataset: ", dsname
                hdf5file.close()
                sys.exit(5)
        else:
            ds = None
        datasets.append(ds)

    # Read the data and copy it to the hdf5 file
    count  = 0
    while(True):
        # Read some lines
        text = csvfile.readlines(input_buffer_size)
        # Split the lines into fields
        lines = []
        for line in text:
            if line.lstrip()[0] != '#':
                lines.append(line.split(separator))
        # Write out these lines
        nread = len(lines)
        if nread > 0:
            for i in range(ncols):
                if dtypes[i] != 'x':
                    try:
                        if dtypes[i] == 'i':
                            data = [int32(line[i]) for line in lines]
                        elif dtypes[i] == 'l':
                            data = [int64(line[i]) for line in lines]
                        elif dtypes[i] == 'f':
                            data = [float32(line[i]) for line in lines]
                    except ValueError:
                        print "Unable to interpret",line[i],"as type",
                        type_name[dtypes[i]]
                        sys.exit(10)
                    ds = datasets[i]
                    # Increase size of dataset
                    ds.resize((count+nread,))
                    # Write the data
                    ds[count:count+nread] = data
            count = count + nread
        else:
            break

    hdf5file.close()

    print "Wrote",count,"lines to",outfilename

if __name__ == "__main__":
    main()
