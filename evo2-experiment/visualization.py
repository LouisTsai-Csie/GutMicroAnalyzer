import torch
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE
import umap

# 1. load embeddings
data = torch.load('embeddings_final.pt')
X = torch.stack(data['embeddings']).numpy()
labels = data['labels']

# transform labels to integers
unique_labels = sorted(set(labels))
label_map = {l: i for i, l in enumerate(unique_labels)}
y = np.array([label_map[l] for l in labels])

palette = sns.color_palette("tab10", n_colors=len(unique_labels))

# 2. t-SNE down to 2D
tsne = TSNE(n_components=2, perplexity=30, random_state=42)
X_tsne = tsne.fit_transform(X)

# 3. UMAP down to 2D
um = umap.UMAP(n_components=2, n_neighbors=15, min_dist=0.1, random_state=42)
X_umap = um.fit_transform(X)

# 4. plotting function
def plot_embeds(Z, title):
    plt.figure(figsize=(8,6))
    sns.scatterplot(x=Z[:,0], y=Z[:,1], hue=y, palette=palette, s=20, alpha=0.8)
    plt.title(title)
    plt.legend(unique_labels, loc='best', bbox_to_anchor=(1.05,1))
    plt.tight_layout()
    plt.show()

# 5. show plots
plot_embeds(X_tsne, "t-SNE visualization of Evo2 embeddings")
plot_embeds(X_umap, "UMAP visualization of Evo2 embeddings")
