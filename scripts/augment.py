# Given files that contains a list of images, this script augments the
# image pair and writes the new image to the specified location.

# Parse command line arguments

import argparse

parser = argparse.ArgumentParser(description='Given files.')
parser.add_argument('-i', '--images', metavar='<path>', nargs=1,
                    required=True,
                    help='path to the root of the images directory'
                         ' (path to Family101_150x120)')
parser.add_argument('-p', '--permdir', metavar='<path>', nargs=1,
                    required=True,
                    help='path to the directory where perm files are stored')
parser.add_argument('-a', '--augmentdir', metavar='<path>', nargs=1,
                    required=True,
                    help='path to the directory where augmented images'
                         ' are stored')
parser.add_argument('-c', '--categories', metavar='<path>', nargs='+',
                    required=True,
                    help='list of categories to augment')

args = parser.parse_args()
images_dir = args.images[0]
perm_dir = args.permdir[0]
augment_dir = args.augmentdir[0]
categories = args.categories[0].split(',')

# Augment images for each category

from os.path import join, exists, basename, splitext
from os import makedirs

for category in categories:
    # Create output directory for category
    category_output_dir = join(augment_dir, category)
    if not exists(category_output_dir):
        makedirs(category_output_dir)

    input_file = open(join(perm_dir, category), 'r')
    for input_line in input_file:
        split_line = input_line.strip().split(' ')
        image1_path = join(images_dir, split_line[0])
        image2_path = join(images_dir, split_line[1])
        augmented_image_path = join(category_output_dir,
                                    splitext(basename(image1_path))[0]
                                    + '-' +
                                    splitext(basename(image2_path))[0]
                                    + '.jpg')

        # Augment the two images
        from PIL import Image

        image1 = Image.open(image1_path)
        image2 = Image.open(image2_path)
        # Creates a new empty image, RGB mode, and size 400 by 400.
        augmented_image = Image.new('RGB',
                                    (image1.size[0] + image2.size[0],
                                     max(image1.size[1], image2.size[1])))

        augmented_image.paste(image1, (0, 0))
        augmented_image.paste(image2, (image1.size[0], 0))

        augmented_image.save(augmented_image_path, 'JPEG')
