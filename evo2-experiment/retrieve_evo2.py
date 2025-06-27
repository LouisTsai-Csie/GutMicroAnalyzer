import os
import torch
from evo2 import Evo2
from tqdm import tqdm

CHECKPOINT_PATH = "checkpoint.pt"
CHECKPOINT_EVERY = 10

device = 'cuda:0'
evo2_model = Evo2('evo2_7b').to(device)
layer_name = 'blocks.28.mlp.l3'

def retrieve_gene(base_dir: str):
    # check every subdirectory in the base directory
    samples = []
    '''
    sample = {
        "disease": "disease_name" (Prediabetic_State),
        "gene": "gene_sequence" (ATCGATCG...),
        "ID": "sample_id" (SRR8534048)}
    '''
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".txt"):
                gene_file_path = os.path.join(root, file)
                with open(gene_file_path, 'r') as f:
                    gene_data = f.read()
                    sample = {
                        "disease": os.path.basename(root),
                        "gene": gene_data.strip(),
                        "ID": os.path.splitext(file)[0]
                    }
                samples.append(sample)
    return samples
                    
def slice_sequence(seq: str, window_size=100_000, overlap=50_000):
    step = window_size - overlap
    slices = [seq[i:i+window_size] for i in range(0, len(seq) - window_size + 1, step)]
    return slices

@torch.no_grad()
def get_embedding(sequence: str):
    input_ids = torch.tensor(
        evo2_model.tokenizer.tokenize(sequence),
        dtype=torch.int,
    ).unsqueeze(0).to(device)
    
    _, embeddings = evo2_model(input_ids, return_embeddings=True, layer_names=[layer_name])
    return embeddings[layer_name].squeeze(0)  # shape: [seq_len, hidden_dim]

def encode_sample(sample):
    gene_seq = sample["gene"]
    slices = slice_sequence(gene_seq)
    embeddings = [get_embedding(s) for s in slices]
    
    # e.g., simple mean pooling over tokens and slices
    pooled_embeddings = [e.mean(dim=0) for e in embeddings]  # mean over seq_len
    final_embedding = torch.stack(pooled_embeddings).mean(dim=0)  # mean over slices
    return final_embedding  # shape: [hidden_dim]

if __name__ == "__main__":
    samples = retrieve_gene("../fastq-experiment/gene_txt_folder")

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

    for sample in tqdm(samples):
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