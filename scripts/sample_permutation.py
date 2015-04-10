# This script samples the permutations of a particular category

# Parse command line arguments

import argparse

parser = argparse.ArgumentParser(description='Sample a given permutation.')
parser.add_argument('-p', '--permdir', metavar='<path>', nargs=1,
                    required=True,
                    help='path to the directory where perm files are stored')
parser.add_argument('-c', '--category', metavar='<path>', nargs=1,
                    required=True,
                    help='Category to sample')
parser.add_argument('-s', '--samplesize', metavar='<path>', nargs=1,
                    required=True,
                    help='Size of the sample')

args = parser.parse_args()
perm_dir = args.permdir[0]
category = args.category[0]
sample_size = int(args.samplesize[0])

# Count the number of lines

from os.path import join

n_lines = 0
with open(join(perm_dir, category), 'r') as category_file:
    for line in category_file:
        n_lines += 1

print('Finished counting number of lines')###

# Generate random permutation of unique line numbers

from numpy.random import random_sample
from numpy import unique
import numpy

assert(sample_size < n_lines)

lines_to_include = []
while len(lines_to_include) != sample_size:
    # To increase the chances of unique sample generation, try with a
    # multiple of the sample size
    lines_to_include = unique((random_sample(
        5 * sample_size) * (n_lines - 1)).astype(int))
    lines_to_include = lines_to_include[:sample_size]

lines_to_include = numpy.sort(lines_to_include).tolist()

# Write the appropriate lines to the sample file

line_no = 0
sample_file = open(join(perm_dir, category + '_sample'), 'w')
with open(join(perm_dir, category), 'r') as category_file:
    next_line_no = lines_to_include.pop(0)
    for line in category_file:
        if line_no == next_line_no:
            sample_file.write(line)
            if lines_to_include:
                next_line_no = lines_to_include.pop(0)
            else:
                break
        line_no += 1

# Close open resources

category_file.close()
sample_file.close()
