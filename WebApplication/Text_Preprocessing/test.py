import os
import torch
from torch.utils.data import DataLoader
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Step 1: Define dummy data
texts = [
    "I love this product. It's amazing!",
    "This is the worst experience I've ever had.",
    "Absolutely fantastic! Highly recommend it.",
    "Terrible quality. I want my money back.",
    "Good value for money.",
    "I am extremely disappointed.",
    "This exceeded my expectations. Great job!",
    "Not worth the hype at all.",
]  # Example text data
labels = [1, 0, 1, 0, 1, 0, 1, 0]  # 1 for positive, 0 for negative

# Step 2: Split into train and validation sets
train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels, test_size=0.2, random_state=42)

# Step 3: Tokenize the data
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=128)

# Step 4: Create a PyTorch Dataset class
class SentimentDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

train_dataset = SentimentDataset(train_encodings, train_labels)
val_dataset = SentimentDataset(val_encodings, val_labels)

# Step 5: Load pre-trained BERT model
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

# Step 6: Set up optimizer and training parameters
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model.to(device)

train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=4)

optimizer = AdamW(model.parameters(), lr=5e-5)

# Step 7: Training loop
epochs = 3

for epoch in range(epochs):
    model.train()
    total_loss = 0
    for batch in train_loader:
        batch = {key: val.to(device) for key, val in batch.items()}
        optimizer.zero_grad()
        outputs = model(**batch)
        loss = outputs.loss
        total_loss += loss.item()
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch + 1}: Loss {total_loss / len(train_loader):.4f}")

    # Validation loop
    model.eval()
    val_preds, val_labels = [], []
    with torch.no_grad():
        for batch in val_loader:
            batch = {key: val.to(device) for key, val in batch.items()}
            outputs = model(**batch)
            logits = outputs.logits
            val_preds.extend(torch.argmax(logits, dim=1).cpu().numpy())
            val_labels.extend(batch['labels'].cpu().numpy())
    acc = accuracy_score(val_labels, val_preds)
    print(f"Validation Accuracy: {acc:.4f}")

# Step 8: Save the model
model.save_pretrained("sentiment_model")
tokenizer.save_pretrained("sentiment_model")
print("Model and tokenizer saved to 'sentiment_model'.")
