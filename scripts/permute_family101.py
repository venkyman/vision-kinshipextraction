# This script generates relationship permutations of 13 categories
# (father_son, son_father, father_daughter, daughter_father, mother_son,
# son_mother, mother_daughter, daughter_mother, sisters, brothers,
# sister_brother, brother_sister, none) from the family 101 dataset


# Define FaceImage class
class FaceImage:
    def __init__(self, family_id, house_id, role_id, name, image_id):
        self.family_id = family_id
        self.house_id = house_id
        self.role_id = role_id
        self.name = name
        self.image_id = image_id

# Parse command line arguments

import argparse
from os import listdir, makedirs
from os.path import join, isdir, exists

parser = argparse.ArgumentParser(description='Process Family101 dataset'
                                             ' and generate pairwise positive'
                                             ' and negative images.')
parser.add_argument('-f', '--families', metavar='<path>', nargs=1,
                    required=True,
                    help='path to the text file containing information'
                         ' about families (path to FAMILY101.txt)')
parser.add_argument('-d', '--dataset', metavar='<path>', nargs=1,
                    required=True,
                    help='path to the root of the dataset directory'
                         ' (path to Family101_150x120)')
parser.add_argument('-p', '--permdir', metavar='<path>', nargs=1,
                    required=True,
                    help='path to the directory where perm files are stored')

args = parser.parse_args()
families = args.families[0]
dataset_dir = args.dataset[0]
perm_dir = args.permdir[0]

# Parse text file into list of face images

families_contents = open(families).read()

face_images = []
for entry in families_contents.split('\r\n'):
    split_entries = entry.split('\t')
    # Ignore empty lines
    if len(split_entries) >= 3:
        if split_entries[1] == 'FAMI':
            family_id = split_entries[2]
        else:
            house_id = split_entries[0]
            role_id = split_entries[1]
            name = split_entries[2]
            images_path = join(dataset_dir, family_id, name)
            # Some entries don't have images, ignore them
            if isdir(images_path):
                for image_id in listdir(join(dataset_dir, family_id, name)):
                    if not image_id.startswith('.'):
                        face_images.append(FaceImage(family_id, house_id,
                                                     role_id, name, image_id))

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
sisters_file = open(join(perm_dir, 'sisters'), 'a')
brothers_file = open(join(perm_dir, 'brothers'), 'a')
sister_brother_file = open(join(perm_dir, 'sister_brother'), 'a')
brother_sister_file = open(join(perm_dir, 'brother_sister'), 'a')
none_file = open(join(perm_dir, 'none'), 'a')

# Generate all relationship permutations and write to files

for i in range(0, len(face_images)):
    for j in range(i + 1, len(face_images)):
        image1 = face_images[i]
        image2 = face_images[j]

        image1_path = join(image1.family_id, image1.name, image1.image_id)
        image2_path = join(image2.family_id, image2.name, image2.image_id)

        # If the two images belong to the same family and house, create
        # relationship entry
        if image1.family_id == image2.family_id:
            same_house = (image1.house_id == image2.house_id)
            diff_name = (image1.name != image2.name)
            if same_house and diff_name:
                if image1.role_id == 'HUSB' and image2.role_id == 'SONN':
                    father_son_file.write(image1_path + ' ' +
                                          image2_path + '\n')
                    son_father_file.write(image2_path + ' ' +
                                          image1_path + '\n')
                elif image1.role_id == 'SONN' and image2.role_id == 'HUSB':
                    father_son_file.write(image2_path + ' ' +
                                          image1_path + '\n')
                    son_father_file.write(image1_path + ' ' +
                                          image2_path + '\n')
                elif image1.role_id == 'HUSB' and image2.role_id == 'DAUG':
                    father_daughter_file.write(image1_path + ' ' +
                                               image2_path + '\n')
                    daughter_father_file.write(image2_path + ' ' +
                                               image1_path + '\n')
                elif image1.role_id == 'DAUG' and image2.role_id == 'HUSB':
                    father_daughter_file.write(image2_path + ' ' +
                                               image1_path + '\n')
                    daughter_father_file.write(image1_path + ' ' +
                                               image2_path + '\n')
                elif image1.role_id == 'WIFE' and image2.role_id == 'SONN':
                    mother_son_file.write(image1_path + ' ' +
                                          image2_path + '\n')
                    son_mother_file.write(image2_path + ' ' +
                                          image1_path + '\n')
                elif image1.role_id == 'SONN' and image2.role_id == 'WIFE':
                    mother_son_file.write(image2_path + ' ' +
                                          image1_path + '\n')
                    son_mother_file.write(image1_path + ' ' +
                                          image2_path + '\n')
                elif image1.role_id == 'WIFE' and image2.role_id == 'DAUG':
                    mother_daughter_file.write(image1_path + ' ' +
                                               image2_path + '\n')
                    daughter_mother_file.write(image2_path + ' ' +
                                               image1_path + '\n')
                elif image1.role_id == 'DAUG' and image2.role_id == 'WIFE':
                    mother_daughter_file.write(image2_path + ' ' +
                                               image1_path + '\n')
                    daughter_mother_file.write(image1_path + ' ' +
                                               image2_path + '\n')
                elif image1.role_id == 'DAUG' and image2.role_id == 'DAUG':
                    sisters_file.write(image1_path + ' ' + image2_path + '\n')
                    sisters_file.write(image2_path + ' ' + image1_path + '\n')
                elif image1.role_id == 'SONN' and image2.role_id == 'SONN':
                    brothers_file.write(image1_path + ' ' + image2_path + '\n')
                    brothers_file.write(image2_path + ' ' + image1_path + '\n')
                elif image1.role_id == 'DAUG' and image2.role_id == 'SONN':
                    sister_brother_file.write(image1_path + ' ' +
                                              image2_path + '\n')
                    brother_sister_file.write(image2_path + ' ' +
                                              image1_path + '\n')
                elif image1.role_id == 'SONN' and image2.role_id == 'DAUG':
                    sister_brother_file.write(image2_path + ' ' +
                                              image1_path + '\n')
                    brother_sister_file.write(image1_path + ' ' +
                                              image2_path + '\n')
                else:
                    try:
                        assert((image1.role_id == 'HUSB' and
                                image2.role_id == 'WIFE') or
                               (image2.role_id == 'HUSB' and
                                image1.role_id == 'WIFE') or
                               (image1.role_id == 'HUSB' and
                                image2.role_id == 'HUSB') or
                               (image1.role_id == 'WIFE' and
                                image2.role_id == 'WIFE'))
                    except AssertionError as e:
                        print(str(vars(image1)) + ' and ' + str(vars(image2)) +
                              ' are incompatible')
                        raise
        else:
            none_file.write(image1_path + ' ' + image2_path + '\n')
            none_file.write(image2_path + ' ' + image1_path + '\n')
    if (i + 1) % 1000 == 0:
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
sisters_file.close()
brothers_file.close()
sister_brother_file.close()
brother_sister_file.close()
none_file.close()
