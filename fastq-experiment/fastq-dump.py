import os
import sys
import json
import subprocess
from tqdm import tqdm
if not os.path.exists('fastq_folder'):
    os.makedirs('fastq_folder')
with open('disease_runID_amp_300MB.json', 'r') as f:
    disease_runID_dict = json.load(f)

target_phenotype_list = ["Parkinson Disease", "Health","Diabetes Mellitus, Type 2","Prediabetic State"] 

for disease, run_ids in disease_runID_dict.items():
    if disease not in target_phenotype_list:
        continue
    # eleminate space and comma in disease name
    disease = disease.replace(" ", "_").replace(",", "")
    if not os.path.exists(f'fastq_folder/{disease}'):
        os.makedirs(f'fastq_folder/{disease}')
    # run_ids = run_ids[1000:1500] # for health
    for run_id, sequence in tqdm(run_ids):
        if os.path.exists(f'fastq_folder/{disease}/{run_id}.fastq'):
            continue
        # working_directory = f"./prefetch_folder/{disease}"
        working_directory = f"."
        # result = subprocess.run(['prefetch', 'DRR048993', "-O", "prefetch_folder/Health"], stdout=None, stderr=None)
        # with subprocess.Popen(['fastq-dump', run_id, '--outdir', f'../../fastq_folder/{disease}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=working_directory) as process:
        with subprocess.Popen(['fastq-dump', run_id, '--outdir', f'./fastq_folder/{disease}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=working_directory) as process:
            # for line in process.stdout:
            #     sys.stdout.write(line)
            # for line in process.stderr:
            #     sys.stderr.write(line)
            process.wait()