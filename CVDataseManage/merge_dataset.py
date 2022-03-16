import glob
import os
import shutil
from os import getcwd
from tqdm import tqdm

MAX_SIZE = 300 # max num of data from each datasets
TRAIN_VAL_SCALE = 5 # train : val = TRAIN_VAL_SCALE : 1
TRAIN_VAL_BIAS = 0

dataset_dirs = ['call', 'engine', 'fire/val', 'fire/train', 'helmet', 'reflective', 'smoking', 'stagnant_water'] # all dirs include images dir and labels dir

labels_dir = 'labels' # name of the dir contains labels
images_dir = 'images' # name of the dir contains images
output_dir = 'yolo_merge' # name of the dir contains outputs

global_class_list = []

def generate_yaml(cwd):
    yaml = open(cwd + '/' + output_dir + '/' + output_dir + '.yaml', 'w')
    yaml.write('path: ../' + output_dir + '\n')
    yaml.write('train: ' + images_dir + '/train\n')
    yaml.write('val: ' + images_dir + '/val\n')
    yaml.write('nc: ' + str(len(global_class_list)) + '\n')
    yaml.write('names: [\'' + '\', \''.join(global_class_list) + '\']\n')

def merge_classes(cwd):
    for dataset_dir in dataset_dirs:
        clses = open(cwd + '/' + dataset_dir + '/' + labels_dir + '/classes.txt')
        for cls in clses:
            cls = cls.strip('\n')
            if not cls in global_class_list and cls != '':
                global_class_list.append(cls)

    generate_yaml(cwd)

    classes_file_val = open(cwd + '/' + output_dir + '/' + labels_dir + '/val/classes.txt', 'w')
    classes_file_train = open(cwd + '/' + output_dir + '/' + labels_dir + '/train/classes.txt', 'w')
    for cls in global_class_list:
        classes_file_val.write(cls + '\n')
        classes_file_train.write(cls + '\n')

def get_labels_in_dir(dir_path):
    label_list = []
    for filename in glob.glob(dir_path + '/*.txt'): 
        basename = os.path.basename(filename)
        if basename == 'classes.txt':
            continue
        label_list.append(filename)

    return label_list

def get_local_classes(dataset_path):
    clses = open(dataset_path + '/' + labels_dir + '/classes.txt')
    return [cls.strip('\n') for cls in iter(clses)]

def renum_label(label_path, output_path, dataset_path, dataset, cnt):
    basename = os.path.basename(label_path)
    basename_no_ext = os.path.splitext(basename)[0]
    output_name = dataset + '_' + str(cnt)

    local_classes_list = get_local_classes(dataset_path)
    in_file = open(label_path)
    
    if (cnt + TRAIN_VAL_BIAS) % (TRAIN_VAL_SCALE + 1) != 0:
        out_file = open(output_path + '/' + labels_dir + '/train/' + output_name + '.txt', 'w')
        shutil.copyfile(dataset_path + '/' + images_dir + '/' + basename_no_ext + '.jpg', output_path + '/' + images_dir + '/train/' + output_name + '.jpg')
    else:
        out_file = open(output_path + '/' + labels_dir + '/val/' + output_name + '.txt', 'w')
        shutil.copyfile(dataset_path + '/' + images_dir + '/' + basename_no_ext + '.jpg', output_path + '/' + images_dir + '/val/' + output_name + '.jpg')

    for line in iter(in_file):
        line_list = line.split(' ')
        local_cls_id = int(line_list[0])
        global_cls_id = global_class_list.index(local_classes_list[local_cls_id])

        line_list[0] = str(global_cls_id)
        output_line = ' '.join(line_list)

        out_file.write(output_line)

if __name__ == "__main__":
    cwd = getcwd() # path to the dir where the script is located

    output_path = cwd + '/' + output_dir # path to output dir of each dataset
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    if not os.path.exists(output_path + '/' + labels_dir):
        os.makedirs(output_path + '/' + labels_dir)
    if not os.path.exists(output_path + '/' + images_dir):
        os.makedirs(output_path + '/' + images_dir)
    if not os.path.exists(output_path + '/' + labels_dir + '/train'):
        os.makedirs(output_path + '/' + labels_dir + '/train')
    if not os.path.exists(output_path + '/' + images_dir + '/train'):
        os.makedirs(output_path + '/' + images_dir + '/train')
    if not os.path.exists(output_path + '/' + labels_dir + '/val'):
        os.makedirs(output_path + '/' + labels_dir + '/val')
    if not os.path.exists(output_path + '/' + images_dir + '/val'):
        os.makedirs(output_path + '/' + images_dir + '/val')

    merge_classes(cwd)

    for dataset_dir in dataset_dirs:

        dataset_path = cwd + '/' + dataset_dir # path to each dataset
        
        label_paths = get_labels_in_dir(dataset_path + '/' + labels_dir) # paths to each labels
        
        if len(label_paths) > MAX_SIZE:
            label_paths = label_paths[0: MAX_SIZE]

        process_bar = tqdm(range(len(label_paths)))
        process_bar.set_description("Processing " + dataset_dir + ": ")
        for idx in process_bar:
            renum_label(label_paths[idx], output_path, dataset_path, '_'.join(dataset_dir.split('/')), idx)