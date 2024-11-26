import os
import json
from tqdm import tqdm
import numpy as np

gene_subfolder = os.listdir("./gene_txt_folder")
gene_seq_len = {}
for dir in gene_subfolder:
    gene_seq_len[dir] = {}
    files = os.listdir(f"./gene_txt_folder/{dir}")
    max_len, min_len = 0, np.inf
    gene_seq_len[dir]["total_files"] = len(files)
    gene_seq_len[dir]["max_len"] = max_len
    gene_seq_len[dir]["min_len"] = min_len
    gene_seq_len[dir]["less_than_100000"] = 0
    gene_seq_len[dir]["less_than_1000000"] = 0
    gene_seq_len[dir]["more_than_10000000"] = 0
    less_than_100000 = 0
    less_than_1000000 = 0
    more_than_10000000 = 0
    for file in tqdm(files):
        with open(f"./gene_txt_folder/{dir}/{file}", "r") as f:
            line = f.readlines()[0]
            gene_seq_len[dir][file] = len(line)
            if len(line) < 100000:
                less_than_100000 += 1
            if len(line) < 1000000:
                less_than_1000000 += 1
            if len(line) > 10000000:
                more_than_10000000 += 1
            if len(line) > max_len:
                max_len = len(line)
            if len(line) < min_len:
                min_len = len(line)
            f.close()
    gene_seq_len[dir]["less_than_100000"] = less_than_100000
    gene_seq_len[dir]["less_than_1000000"] = less_than_1000000
    gene_seq_len[dir]["more_than_10000000"] = more_than_10000000
    gene_seq_len[dir]["max_len"] = max_len
    gene_seq_len[dir]["min_len"] = min_len
    # print(f"Less than 100000: {less_than_100000}")
with open("gene_seq_len.json", "w") as json_file:
    json.dump(gene_seq_len, json_file, indent=4)
        # if file.endswith(".fastq"):
        #     with open(f"./fastq_folder/{dir}/{file}", "r") as f:
        #         lines = f.readlines()
        #         with open(f"./gene_txt_folder/{dir}/{file[:-6]}.txt", "w") as txt_file:
        #             for i, line in enumerate(lines):
        #                 if i % 4 == 1:
        #                     txt_file.write(line[:-1])
        #             txt_file.close()
        #         f.close()
        # else:
        #     print(f"File {file} is not a fastq file")