from PIL import Image
import numpy as np
import os
from tqdm import tqdm

def seq_to_array(seq):
    value_list = []
    for i in range(0, len(seq), 3):
        sub_seq = seq[i:i+3]
        if len(sub_seq) < 3:
            continue
        gene_to_value = {'A': 0, 'T': 1, 'C': 2, 'G': 3, 'N': 4}
        # substitute A, T, C, G, N with 0, 1, 2, 3, 4
        gene_str = "".join([str(gene_to_value[c]) for c in sub_seq])
        decimal_value = int(gene_str, 5)
        value_list.append(decimal_value)
    # padding value_list to the multiple of 3
    if len(value_list) % 3 != 0:
        value_list += [0] * (3 - len(value_list) % 3)
    # reshape value_list to m x n x 3
    size2d = len(value_list) // 3
    width = round(size2d**0.5)
    height = int(np.ceil(size2d / width))
    value_list += [0] * (width * height * 3 - len(value_list))
    image_array = np.array(value_list, dtype=np.uint8).reshape((height, width, 3))
    image = Image.fromarray(image_array, mode='RGB')
    return image

def deal_seq(txt_file, png_file):
    with open(txt_file, 'r') as f:
        seq = f.read()
    img = seq_to_array(seq)
    img.save(png_file)  

if __name__ == "__main__":
    relative_dataset_path = "../YOLO-experiment/datasets"
    if not os.path.exists(relative_dataset_path):
        os.makedirs(relative_dataset_path)
    # make train, test, val folders
    for folder in ["train", "test", "val"]:
        folder_path = os.path.join(relative_dataset_path, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    for root, dirs, files in os.walk("gene_txt_folder"):
        count = 0
        for i, file in enumerate(tqdm(files)):
            if not file.endswith(".txt"):
                continue
            txt_file = os.path.join(root, file)
            upper_folder = os.path.basename(os.path.dirname(txt_file))
            if count % 10 < 2:
                relative_dir = os.path.join(relative_dataset_path, "test", upper_folder)
            elif count % 10 < 4:
                relative_dir = os.path.join(relative_dataset_path, "val", upper_folder)
            else:
                relative_dir = os.path.join(relative_dataset_path, "train", upper_folder)
            if not os.path.exists(relative_dir):
                os.makedirs(relative_dir)
            png_file = os.path.join(relative_dir, file.replace(".txt", ".png"))
            deal_seq(txt_file, png_file)
            count += 1       



