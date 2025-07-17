import os
import gc
import torch
from evo2 import Evo2
from tqdm import tqdm

CHECKPOINT_PATH = "checkpoint.pt"
CHECKPOINT_EVERY = 10

device = 'cuda:0'
evo2_model = Evo2('evo2_1b_base') # evo2_7b
layer_name = 'blocks.24.mlp.l3' # blocks.28.mlp.l3 (24: 1b_base)

def retrieve_total_file_list(base_dir: str):
    # check every subdirectory in the base directory
    file_list = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                file_list.append(file_path)
    return file_list

def retrieve_gene(filepath: str):
    with open(filepath, 'r') as f:
        gene_data = f.read().strip()
    sample_id = os.path.splitext(os.path.basename(filepath))[0]
    disease = os.path.basename(os.path.dirname(filepath))  # e.g., 'Prediabetic_State'
    sample = {
        "disease": disease,
        "gene": gene_data,
        "ID": sample_id
    }
    return sample
    

# 100000 & 50000 too large, GPU cannot handle                    
def slice_sequence(seq: str, window_size=10000, overlap=5000):
    step = window_size - overlap
    slices = [seq[i:i+window_size] for i in range(0, len(seq) - window_size + 1, step)]
    return slices

# TODO: make sure the shape is correct
@torch.no_grad()
def get_embedding(sequence: str):
    input_ids = torch.tensor(
        evo2_model.tokenizer.tokenize(sequence),
        dtype=torch.int,
    ).unsqueeze(0).to(device)
    
    _, embeddings = evo2_model(input_ids, return_embeddings=True, layer_names=[layer_name])
    return embeddings[layer_name].squeeze(0).cpu()  # shape: [seq_len, hidden_dim]

# TODO: make sure the shape is correct
def encode_sample(sample):
    gene_seq = sample["gene"]
    slices = slice_sequence(gene_seq)
    sum_embeddings = []

    # for s in slices:
    for s in tqdm(slices, desc=f"Processing {sample['ID']}"):
        mean_embedding = get_embedding(s).mean(dim=0).cpu()
        sum_embeddings.append(mean_embedding)
        torch.cuda.empty_cache()
        gc.collect()

    final_embedding = torch.stack(sum_embeddings).mean(dim=0)  # mean over slices
    return final_embedding  # shape: [hidden_dim]

if __name__ == "__main__":
    genefiles = retrieve_total_file_list("../fastq-experiment/gene_txt_folder")

    if os.path.exists(CHECKPOINT_PATH):
        data = torch.load(CHECKPOINT_PATH)
        embeddings = data['embeddings']
        labels = data['labels']
        ids = data['ids']  
        print(f"Resuming from checkpoint: {len(ids)} samples")
    else:
        embeddings, labels, ids = [], [], []
        print("Starting from scratch")

    buffer_emb, buffer_label, buffer_id = [], [], []

    for genefile in tqdm(genefiles):
        sample = retrieve_gene(genefile)

        if sample["ID"] in ids:
            continue  

        emb = encode_sample(sample)
        buffer_emb.append(emb.cpu())
        buffer_label.append(sample["disease"])
        buffer_id.append(sample["ID"])

        if len(buffer_emb) == CHECKPOINT_EVERY:
            embeddings.extend(buffer_emb)
            labels.extend(buffer_label)
            ids.extend(buffer_id)
            torch.save({
                'embeddings': embeddings,
                'labels': labels,
                'ids': ids
            }, CHECKPOINT_PATH)
            print(f"Checkpoint saved: {len(ids)} samples")
            buffer_emb, buffer_label, buffer_id = [], [], []

    # store the last batch
    if buffer_emb:
        embeddings.extend(buffer_emb)
        labels.extend(buffer_label)
        ids.extend(buffer_id)
        torch.save({
            'embeddings': embeddings,
            'labels': labels,
            'ids': ids
        }, CHECKPOINT_PATH)
        print(f"Final checkpoint saved: {len(ids)} samples")

    # save to final ver.
    torch.save({
        'embeddings': embeddings,
        'labels': labels,
        'ids': ids
    }, "embeddings_final.pt")
    print("Done! Saved all to embeddings_final.pt")

# data = torch.load("embeddings.pt")
# print(data['embeddings'][0].shape)  # e.g., torch.Size([4096])
# print(data['labels'][0])            # e.g., 'Prediabetic_State'
# print(data['ids'][0])               # e.g., 'SRR8534048'