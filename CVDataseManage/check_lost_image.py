import glob
import os
from os import getcwd
from tqdm import tqdm

dataset_dirs = ['stagnant_water', 'smoking', 'call', 'fire/train', 'fire/val', 'helmet', 'reflective', 'engine'] # all dirs include images dir and labels dir

labels_dir = 'labels' # name of the dir contains labels
images_dir = 'images' # name of the dir contains images

def get_images_in_dir(dir_path):
    image_list = []
    for filename in glob.glob(dir_path + '/*.jpg'): 
        image_list.append(os.path.splitext(os.path.basename(filename))[0])

    return image_list

if __name__ == "__main__":
    cwd = getcwd() # path to the dir where the script is located

    for dataset_dir in dataset_dirs:
        dataset_path = cwd + '/' + dataset_dir # path to each dataset

        image_list = get_images_in_dir(dataset_path + '/' + images_dir) # paths to each labels

        file_list = glob.glob(dataset_path + '/' + labels_dir + '/*.txt')

        missing_list = []
        process_bar = tqdm(range(len(file_list)))
        process_bar.set_description("Checking " + dataset_dir)
        for idx in process_bar: 
            filename = file_list[idx]
            if not os.path.splitext(os.path.basename(filename))[0] in image_list:
                basename = os.path.basename(filename)
                if basename == 'classes.txt':
                    continue

                tmp_list = filename.split('.')
                tmp_list[-1] = 'jpg'
                image_name = '.'.join(tmp_list)
                missing_list.append(image_name)
        
        if len(missing_list) > 0:
            print('\nMissing images in', dataset_dir, ':')
            for m in missing_list:
                print(m)
            print('\n')