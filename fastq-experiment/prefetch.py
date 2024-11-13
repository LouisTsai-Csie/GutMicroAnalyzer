import os
import json
import subprocess
from tqdm import tqdm
if not os.path.exists('prefetch_folder'):
    os.makedirs('prefetch_folder')
with open('disease_runID.json', 'r') as f:
    disease_runID_dict = json.load(f)
for disease, run_ids in disease_runID_dict.items():
    # eleminate space and comma in disease name
    disease = disease.replace(" ", "_").replace(",", "")
    if not os.path.exists(f'prefetch_folder/{disease}'):
        os.makedirs(f'prefetch_folder/{disease}')
    for run_id in tqdm(run_ids):
        subprocess.run(['prefetch', run_id, "-O", f"prefetch_folder/{disease}"], stdout=None, stderr=None)
        # result = subprocess.run(['prefetch', 'DRR048993', "-O", "prefetch_folder/Health"], stdout=None, stderr=None)
        # with subprocess.Popen(['prefetch', 'DRR048993', '-O', 'prefetch_folder/Health'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
            # for line in process.stdout:
            #     sys.stdout.write(line)
            # for line in process.stderr:
            #     sys.stderr.write(line)
            # process.wait()