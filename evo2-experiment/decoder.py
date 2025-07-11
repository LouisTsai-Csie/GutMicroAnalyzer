import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split
import torch.nn.functional as F
import torch.optim as optim
from tqdm import tqdm

class EmbeddingDataset(Dataset):
    def __init__(self, data_path):
        data = torch.load(data_path)
        self.embeddings = data['embeddings']
        self.labels_raw = data['labels']
        self.label_map = {label: idx for idx, label in enumerate(sorted(set(self.labels_raw)))}
        self.labels = [self.label_map[label] for label in self.labels_raw]

    def __len__(self):
        return len(self.embeddings)

    def __getitem__(self, idx):
        return self.embeddings[idx], self.labels[idx]

class SimpleDecoder(nn.Module):
    def __init__(self, input_dim, num_classes):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        return self.net(x)

def train_epoch():
    model.train()
    total_loss, correct = 0, 0
    for x, y in tqdm(train_loader, desc="Training"):
        x, y = x.to(device), torch.tensor(y).to(device)
        logits = model(x)
        loss = F.cross_entropy(logits, y)
        total_loss += loss.item() * x.size(0)
        correct += (logits.argmax(1) == y).sum().item()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    return total_loss / len(train_loader.dataset), correct / len(train_loader.dataset)

def eval_epoch():
    model.eval()
    total_loss, correct = 0, 0
    with torch.no_grad():
        for x, y in tqdm(val_loader, desc="Validating"):
            x, y = x.to(device), torch.tensor(y).to(device)
            logits = model(x)
            loss = F.cross_entropy(logits, y)
            total_loss += loss.item() * x.size(0)
            correct += (logits.argmax(1) == y).sum().item()
    return total_loss / len(val_loader.dataset), correct / len(val_loader.dataset)


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# step. 1
dataset = EmbeddingDataset("embeddings_final.pt")
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_set, val_set = random_split(dataset, [train_size, val_size])

train_loader = DataLoader(train_set, batch_size=16, shuffle=True)
val_loader = DataLoader(val_set, batch_size=16)

# step. 2
input_dim = dataset[0][0].shape[0]
num_classes = len(set(dataset.labels))
model = SimpleDecoder(input_dim, num_classes).to(device)
optimizer = optim.Adam(model.parameters(), lr=1e-4)

for epoch in range(10):
    train_loss, train_acc = train_epoch()
    val_loss, val_acc = eval_epoch()
    print(f"[Epoch {epoch+1}] Train Loss: {train_loss:.4f}, Acc: {train_acc:.4f} | Val Loss: {val_loss:.4f}, Acc: {val_acc:.4f}")

torch.save(model.state_dict(), "decoder_model.pt")