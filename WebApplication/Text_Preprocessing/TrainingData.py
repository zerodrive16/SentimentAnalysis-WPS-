import torch
import torch.optim as optim
from tqdm import tqdm
from torch.utils.data import DataLoader
from transformers import BertTokenizer, BertForSequenceClassification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os
import sys
import django
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SentimentAnalysis.settings')
django.setup()
from WebApplication.models import Data

# Set up the Data
dataset = Data.objects.values('comment_body_corrected', 'comment_labels')

texts = [entry['comment_body_corrected'] for entry in dataset]
labels = [entry['comment_labels'] for entry in dataset]

# Splitting the data in training and testing
train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels, test_size=0.2, random_state=42)

# Tokenize
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=128)


# Dataset class
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

# Load model
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

# Training device
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model.to(device)

train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=4)
optimizer = optim.AdamW(model.parameters(), lr=5e-5)

# Training Loop
epochs = 100 # Set the epoch

for epoch in range(epochs):
    model.train() # Train the model
    total_loss = 0 # Keep track of the cumulative loss during epoch
    for batch in tqdm(train_loader, desc=f"Epoch {epoch + 1}/{epochs}", leave=False):
        batch = {key: val.to(device) for key, val in batch.items()} # move batch to specified device and contains the inputs_id and attention_mask
        optimizer.zero_grad() # Clearing previous gradients
        outputs = model(**batch) # Put the input_ids and attention_mask to the model
        loss = outputs.loss # Extracts output loss from the model
        total_loss += loss.item() # Accumulate the loss
        loss.backward() # Adjust the gradients (weights and magnitude) for next epoch
        optimizer.step() # Updating model para
    print(f"Epoch {epoch + 1}: Loss {total_loss / len(train_loader):.4f}") # Output avg. loss each epoch

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

# Save the mdoel
model.save_pretrained("sentiment_model")
tokenizer.save_pretrained("sentiment_model")
print("Model and tokenizer saved to 'sentiment_model'.")
