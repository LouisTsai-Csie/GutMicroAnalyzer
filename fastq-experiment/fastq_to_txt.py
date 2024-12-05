import os
from tqdm import tqdm

fastq_subfolder = os.listdir("./fastq_folder")
if not os.path.exists("./gene_txt_folder"):
    os.makedirs("./gene_txt_folder")

# target_dirs = ["Arthritis_Rheumatoid","Bipolar_Disorder"]

for dir in fastq_subfolder:
    # if dir not in target_dirs:
    #     continue
    if not os.path.exists(f"./gene_txt_folder/{dir}"):
        os.makedirs(f"./gene_txt_folder/{dir}")
    files = os.listdir(f"./fastq_folder/{dir}")
    for file in tqdm(files):
        if file.endswith(".fastq"):
            with open(f"./fastq_folder/{dir}/{file}", "r") as f:
                lines = f.readlines()
                with open(f"./gene_txt_folder/{dir}/{file[:-6]}.txt", "w") as txt_file:
                    for i, line in enumerate(lines):
                        if i % 4 == 1:
                            # for c in line:
                            #     if c not in ['A', 'T', 'C', 'G', 'N', '\n']:
                            #         raise Exception (f"Invalid character {c} in file {file}, line {i}")
                            txt_file.write(line[:-1])
                    txt_file.close()
                f.close()
                # if len(file) < 1000000 then delete the file
                txt_file = open(f"./gene_txt_folder/{dir}/{file[:-6]}.txt", "r")
                txt_line = txt_file.readlines()[0]
                if len(txt_line) < 1000000:
                    os.remove(f"./gene_txt_folder/{dir}/{file[:-6]}.txt")

        else:
            print(f"File {file} is not a fastq file")
