import glob
import os
import xml.etree.ElementTree as ET
from os import getcwd
from tqdm import tqdm

dataset_dirs = ['fire/validation', 'fire/train'] # all dirs include images dir and labels dir
classes = ['fire'] # all classes in these datasets, index in array is class index of output

labels_dir = 'Annotations' # name of the dir contains labels
images_dir = 'JPEGImages' # name of the dir contains images

def get_images_in_dir(dir_path):
    image_list = []
    for filename in glob.glob(dir_path + '/*.jpg'): # you can rewrite here to support more types of images
        image_list.append(filename)

    return image_list

def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_annotation(label_path, output_path, image_path):
    basename = os.path.basename(image_path)
    basename_no_ext = os.path.splitext(basename)[0]

    in_file = open(label_path + '/' + basename_no_ext + '.xml')
    out_file = open(output_path + basename_no_ext + '.txt', 'w')

    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)

        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

if __name__ == "__main__":
    cwd = getcwd() # path to the dir where the script is located

    for dataset_dir in dataset_dirs:

        dataset_path = cwd + '/' + dataset_dir # path to each dataset
        output_path = dataset_path +'/yolo/' # path to output dir of each dataset

        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        classes_file = open(output_path + 'classes.txt', 'w')
        for cls in classes:
            classes_file.write(cls + '\n')

        image_paths = get_images_in_dir(dataset_path + '/' + images_dir) # paths to each images
        label_path = dataset_path + '/' + labels_dir # path to label dir

        process_bar = tqdm(range(len(image_paths)))
        process_bar.set_description("Processing " + dataset_dir + ": ")
        for idx in process_bar:
            convert_annotation(label_path, output_path, image_paths[idx])