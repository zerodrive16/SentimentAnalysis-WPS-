import os
import sys
import django
import re
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, Dataset
from sklearn.model_selection import train_test_split
from torch.optim import Adam
from tqdm import tqdm



# Configure Django Settings for ORM
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SentimentAnalysis.settings')
django.setup()

from WebApplication.models import Data  # Ensure you have Django models configured for text storage



all_records = Data.objects.all()

######################################################################################################

# Step 1 Prepare Dataset

data = []

# Iterate over the records from the database
for record in all_records:
    # Clean the comment_body using regex
    cleaned_comment = re.sub(r'[^\x00-\x7F]+', '', record.comment_body)
    cleaned_comment = re.sub(r'[^a-zA-Z0-9\s]', '', cleaned_comment)
    cleaned_comment = re.sub(r'\s+', ' ', cleaned_comment).strip()

    # Access the label and append the cleaned comment with its label as a tuple
    data.append((cleaned_comment, record.labels))

print(data)

# Split the data into training and testing sets
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Define a custom Dataset class to handle the data
class SentimentDataset(Dataset):
    def __init__(self, data, tokenizer, max_len=128):
        self.data = data
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        sentence, label = self.data[index]

        tokens = self.tokenizer(
            sentence,
            max_length=self.max_len,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        return {
            "input_ids": tokens["input_ids"].squeeze(0),
            "attention_mask": tokens["attention_mask"].squeeze(0),
            "labels": torch.tensor(label, dtype=torch.long)
        }

# Initialize tokenizer for BERT
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Create Dataset objects for training and testing
train_dataset = SentimentDataset(train_data, tokenizer)
test_dataset = SentimentDataset(test_data, tokenizer)

# Step 2: Set up the DataLoader
# DataLoader helps in batching and shuffling data for training
train_loader = DataLoader(train_dataset, batch_size=2, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=2)

# Step 3: Load Pre-trained BERT Model
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

# Step 4: Define the Optimizer and Loss Function
optimizer = Adam(model.parameters(), lr=2e-5)
loss_fn = torch.nn.CrossEntropyLoss()

# Step 5: Train the Model
# Move the model to the GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
print(f"Using device: {device}")

epochs = 10
for epoch in range(epochs):
    print(f"Epoch {epoch + 1}/{epochs}")
    model.train()

    loop = tqdm(train_loader, leave=True)
    for batch in loop:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        optimizer.zero_grad()

        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        logits = outputs.logits

        loss.backward()

        optimizer.step()

        loop.set_description(f"Loss {loss.item():.4f}")

# Step 6: Evaluate the Model
model.eval()

correct = 0
total = 0

with torch.no_grad():
    for batch in test_loader:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        # Get predictions
        outputs = model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=1)

        correct += (predictions == labels).sum().item()
        total += labels.size(0)

accuracy = correct / total
print(f"Test Accuracy: {accuracy:.4f}")

# Step 7: Save the Model
model.save_pretrained("sentiment_model")
tokenizer.save_pretrained("sentiment_model")