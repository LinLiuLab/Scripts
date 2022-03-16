import glob
import os
import cv2
from os import getcwd
from tqdm import tqdm

dataset_dirs = ['engine'] # all dirs include images dir and labels dir
image_type = ['jpeg', 'png', 'JPG', 'JPEG', 'PNG']

images_dir = 'images' # name of the dir contains images

def convert_img(image_dir, dataset_dir):
    list_dirs = os.walk(image_dir)
    process_bar = tqdm(total=len(os.listdir(image_dir)), desc='Converting')
    
    for root, _, files in list_dirs:
        for file in files:
            process_bar.update(1)
            if not file.split('.')[1] in image_type:
                continue
            file_name = file.split('.')[0]

            img_path = os.path.join(root, file)
            try:
                src = cv2.imread(img_path, 1)
                os.remove(img_path)
                cv2.imwrite(os.path.join(root, file_name + '.jpg'), src)
            except:
                os.remove(img_path)
                continue

if __name__ == "__main__":
    cwd = getcwd() # path to the dir where the script is located

    for dataset_dir in dataset_dirs:
        convert_img(cwd + '/' + dataset_dir + '/' + images_dir, dataset_dir)