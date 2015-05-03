# This script generates relationship permutations of 9 categories
# (father_son, son_father, father_daughter, daughter_father, mother_son,
# son_mother, mother_daughter, daughter_mother, none) from the KinFaceW-(I/II)
# dataset


# Define FaceImage class
class FaceImage:
    def __init__(self, relation_id, family_id, role_id, image_id, path):
        self.relation_id = relation_id
        self.family_id = family_id
        self.role_id = role_id
        self.image_id = image_id
        self.path = path

# KinFaceW-I relation type to our relation type map
relation_id_map = {
    'father-dau': 'father_daughter',
    'father-son': 'father_son',
    'mother-dau': 'mother_daughter',
    'mother-son': 'mother_son'
}

# Parse command line arguments

import argparse
from os import listdir, makedirs
from os.path import join, exists, basename

parser = argparse.ArgumentParser(description='Process KinFaceW-1 dataset'
                                             ' and generate pairwise positive'
                                             ' and negative images.')
parser.add_argument('-d', '--dataset', metavar='<path>', nargs=1,
                    required=True,
                    help='path to the root of the dataset directory'
                         ' (path to KinFaceW-(I/II))')
parser.add_argument('-p', '--permdir', metavar='<path>', nargs=1,
                    required=True,
                    help='path to the directory where perm files are stored')

args = parser.parse_args()
dataset_dir = args.dataset[0]
perm_dir = args.permdir[0]

# Iterate through the images directory

face_images = []
for kinface_relation_id in relation_id_map.keys():
    relation_id = relation_id_map[kinface_relation_id]
    relation_images_dir = join(dataset_dir, 'images', kinface_relation_id)
    for image_id in listdir(relation_images_dir):
        if image_id != 'Thumbs.db':
            split_image_id = image_id.split('.')[0].split('_')
            family_id = split_image_id[1]
            role_id = split_image_id[2]
            path = join('images', kinface_relation_id, image_id)
            face_images.append(FaceImage(relation_id, family_id, role_id,
                                         image_id, path))

# Prepare output files

if not exists(perm_dir):
    makedirs(perm_dir)

father_son_file = open(join(perm_dir, 'father_son'), 'a')
son_father_file = open(join(perm_dir, 'son_father'), 'a')
father_daughter_file = open(join(perm_dir, 'father_daughter'), 'a')
daughter_father_file = open(join(perm_dir, 'daughter_father'), 'a')
mother_son_file = open(join(perm_dir, 'mother_son'), 'a')
son_mother_file = open(join(perm_dir, 'son_mother'), 'a')
mother_daughter_file = open(join(perm_dir, 'mother_daughter'), 'a')
daughter_mother_file = open(join(perm_dir, 'daughter_mother'), 'a')
none_file = open(join(perm_dir, 'none'), 'a')

# Generate all relationship permutations and write to files

for i in range(0, len(face_images)):
    for j in range(i + 1, len(face_images)):
        image1 = face_images[i]
        image2 = face_images[j]

        if image1.role_id == '2':
            image1, image2 = image2, image1

        # If the two images belong to the same relation and family, create
        # relationship entry
        same_relation = (image1.relation_id == image2.relation_id)
        same_family = (image1.family_id == image2.family_id)
        if same_relation:
            if same_family:
                if image1.relation_id == 'father_son':
                    father_son_file.write(image1.path + ' ' +
                                          image2.path + '\n')
                    son_father_file.write(image2.path + ' ' +
                                          image1.path + '\n')
                elif image1.relation_id == 'father_daughter':
                    father_daughter_file.write(image1.path + ' ' +
                                               image2.path + '\n')
                    daughter_father_file.write(image2.path + ' ' +
                                               image1.path + '\n')
                elif image1.relation_id == 'mother_son':
                    mother_son_file.write(image1.path + ' ' +
                                          image2.path + '\n')
                    son_mother_file.write(image2.path + ' ' +
                                          image1.path + '\n')
                elif image1.relation_id == 'mother_daughter':
                    mother_daughter_file.write(image1.path + ' ' +
                                               image2.path + '\n')
                    daughter_mother_file.write(image2.path + ' ' +
                                               image1.path + '\n')
                else:
                    raise Exception(str(vars(image1)) + ' and ' +
                                    str(vars(image2)) + ' are incompatible')
            else:
                none_file.write(image1.path + ' ' + image2.path + '\n')
                none_file.write(image2.path + ' ' + image1.path + '\n')
    if (i + 1) % 100 == 0:
        print('First ' + str(i + 1) + ' iterations completed!')

# Close all open files

father_son_file.close()
son_father_file.close()
father_daughter_file.close()
daughter_father_file.close()
mother_son_file.close()
son_mother_file.close()
mother_daughter_file.close()
daughter_mother_file.close()
none_file.close()
