import random
from tqdm import tqdm
random.seed(307)
length_to_generate = 10000000
gene_mapping = {0: 'A', 1: 'T', 2: 'C', 3: 'G'}
for i in tqdm(range(10)):
    gene_sequence = ''.join([gene_mapping[random.randint(0, 3)] for _ in range(length_to_generate)]) # gene "str" of length [length_to_generate] 
    # print(gene_sequence)
    # 10,000,000 is an acceptable length for a gene sequence (e.g.: figure width x height = 3677 × 2434)