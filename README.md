# Prerequisite
Install `evo2` on the same server by the following

```
conda create -n evo2-env python=3.11
conda activate evo2-env
conda install -c nvidia cuda-toolkit=12.4 cudnn=9

pip install torch==2.6.0 torchvision

git clone --recurse-submodules https://github.com/ArcInstitute/evo2.git

### Go to /vortex/Makefile
### Change line 61 from "pip install transformer_engine[pytorch] --no-build-isolation" 
### to "pip install transformer_engine[pytorch]==1.13.0 --no-build-isolation"

cd evo2
pip install .

# test if installed sucessfully (required ~16GB GPU VRAM)
python ./test/test_evo2.py --model_name evo2_7b
```

Please run the following python3 code in `anaconda evo2-env`

# File structure
1. fastq-experiment
   1. `api_test/`: to test if api works fine
   2. `fastq_folder/`: store downloaded `fastq` files
   3. `gene_txt_folder(_base)/`: store transformed `txt` gene seqs from `fastq` files
   4. `fastq_to_txt.py`: transform fastq files to txt files
   5. `fastq-dump.py`: dump fastq files from website
   6. `getPhenotype.py`: get the phenotype informations to download `fastq` files
   7. `gentxt_to_png.py`: (TO BE DEPRECATED)
   8. `gene_seq_len.json` & `gene_txt_seq_len.py`: analysis of gene seqs
2. evo2-experiment
   1. `retrieve_evo2.py`: get retrieved info (embedded info) from `evo2`
   2. `decoder.py`: train decoder to perform classification tasks on the embedded infos
   3. `visualization.py`: show visualization results of the retrieved embedded info
3. YOLO-experiment (TO BE DEPRECATED)

# Note
1. nvidia-smi 顯示 3426MiB /  24564MiB 時，還是跑不動