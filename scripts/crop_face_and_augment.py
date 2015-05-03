# Given files that contains a list of images, this script augments the
# image pair after cropping the facial regions and writes the new image
# to the specified location.


# Finds the largest box in a list of face boxes
def find_largest_face_box(face_boxes):
    if len(face_boxes) == 1:
        return face_boxes[0]
    else:
        largest_area = 0
        largest_face_box = face_boxes[0]
        for face_box in face_boxes:
            if face_box[2] * face_box[3] > largest_area:
                largest_area = face_box[2] * face_box[3]
                largest_face_box = face_box
        return largest_face_box


# Crops face region
def crop_face(image, box):
    (x, y, w, h) = box
    return image[y: y + h, x: x + w]

# Parse command line arguments

import argparse

parser = argparse.ArgumentParser(description='Given files that contains a'
                                             ' list of images, this script'
                                             ' augments the image pair after'
                                             ' cropping the facial regions'
                                             ' and writes the new image'
                                             ' to the specified location.')
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
parser.add_argument('-f', '--facecascade', metavar='<path>', nargs='+',
                    required=True,
                    help='path to the face cascade xml')
parser.add_argument('-o', '--original', action='store_true', default=False,
                    help='keep original images and do not crop')

args = parser.parse_args()
images_dir = args.images[0]
perm_dir = args.permdir[0]
augment_dir = args.augmentdir[0]
categories = args.categories[0].split(',')
cascade_path = args.facecascade[0]
keep_original = args.original

# Augment images for each category

from os.path import join, exists
from os import makedirs
from re import sub
from numpy import concatenate
from cv2 import CascadeClassifier, imread, cvtColor, COLOR_BGR2GRAY, resize
from cv2 import imwrite

for category in categories:
    print('Augmenting images under ' + category + ' category...')
    # Create output directory for category
    category_output_dir = join(augment_dir, category)
    if not exists(category_output_dir):
        makedirs(category_output_dir)

    input_file = open(join(perm_dir, category), 'r')
    for input_line in input_file:
        split_line = input_line.strip().split(' ')
        image1_id = sub('(/|\.)', '_', split_line[0])
        image2_id = sub('(/|\.)', '_', split_line[1])
        image1_path = join(images_dir, split_line[0])
        image2_path = join(images_dir, split_line[1])
        augmented_image_path = join(category_output_dir,
                                    image1_id + '_' + image2_id + '.jpg')

        # Detect faces in the two images
        # Create the haar cascade
        face_cascade = CascadeClassifier(cascade_path)
        # Read the two images
        image1 = imread(image1_path)
        image2 = imread(image2_path)
        if not keep_original:
            # Get gray scale image
            image1_gray = cvtColor(image1, COLOR_BGR2GRAY)
            image2_gray = cvtColor(image2, COLOR_BGR2GRAY)
            # Detect faces in the image
            image1_face_boxes = face_cascade.detectMultiScale(image1_gray)
            image2_face_boxes = face_cascade.detectMultiScale(image2_gray)
            if len(image1_face_boxes) != 0:
                # If more than two faces were found, take the largest window
                image1_face_box = find_largest_face_box(image1_face_boxes)
                # Crop face region
                image1_cropped = crop_face(image1, image1_face_box)
            else:
                # No face detected, just use the original image
                image1_cropped = image1

            if len(image2_face_boxes) != 0:
                # If more than two faces were found, take the largest window
                image2_face_box = find_largest_face_box(image2_face_boxes)
                # Crop face region
                image2_cropped = crop_face(image2, image2_face_box)
            else:
                # No face detected, just use the original image
                image2_cropped = image2
            image1 = image1_cropped
            image2 = image2_cropped

        # Resize larger of the two images to the smaller of the two
        if image1.shape[0] * image1.shape[1] \
                > image2.shape[0] * image2.shape[1]:
            image1 = resize(image1,
                            (image2.shape[1],
                             image2.shape[0]))
        else:
            image2 = resize(image2,
                            (image1.shape[1],
                             image1.shape[0]))
        # Augment the two images
        augmented_image = concatenate((image1, image2), axis=1)

        imwrite(augmented_image_path, augmented_image)
    print('Finished augmenting images under ' + category + ' category')
