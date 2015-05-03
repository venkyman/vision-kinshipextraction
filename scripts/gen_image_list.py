# Given the dataset's directory under the data directory, generates the
# corresponding file containing the list of all augmented images and their
# corresponding categories.

# Parse command line arguments

import argparse

parser = argparse.ArgumentParser(description='Given files.')
parser.add_argument('-d', '--datadir', metavar='<path>', nargs=1,
                    required=True,
                    help='path to the dataset\'s directory under the data'
                         ' directory')
parser.add_argument('-n', '--name', metavar='<path>', nargs=1,
                    required=True,
                    help='path to the name of the file that should contain'
                         ' the list')

args = parser.parse_args()
data_dir = args.datadir[0]
name = args.name[0]

# Generate result file for each dataset

from os import listdir
from os.path import basename, join, isdir
from numpy.random import shuffle

dataset_prefix = basename(data_dir)

image_category_pairs = []
category_counter = 0
category_map = {}
for category_dir in listdir(join(data_dir, data_dir)):
    if isdir(join(data_dir, category_dir)):
        category_map[category_dir] = category_counter
        category_prefix = join(dataset_prefix, category_dir)

        for image in listdir(join(data_dir, category_dir)):
            image_category_pairs.append((join(category_prefix, image),
                                        category_counter))

        category_counter += 1

# Write result
shuffle(image_category_pairs)
result_file = open(join(data_dir, name + '.txt'), 'w')
# Write comment line containing all the categories
result_file.write("# " + str(category_map) + '\n')
# Write each pair in a separate line
for image_category_pair in image_category_pairs:
    result_file.write(image_category_pair[0] + ' ' +
                      str(image_category_pair[1]) + '\n')
result_file.close()
