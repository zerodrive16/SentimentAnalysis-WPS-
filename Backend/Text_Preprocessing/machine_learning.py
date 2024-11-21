import re
import os
import sys
import django

# Configure the Settings to set up the correct models.py path for ORM
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..'))
# Pointing to Django Settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SentimentAnalysis.settings')

# Set up ORM to read / write in database
django.setup()

from Backend.models import Data
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import torch.nn.functional as F

# Step 1: Load pre-trained BERT tokenizer and model for sequence classification
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')  # Use 'bert-base-uncased' or 'bert-base-cased'
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)  # Assume binary classification (positive/negative)

# Step 2: Preprocess input text (tokenization and conversion to tensor)
def preprocess_text(text):
    # Tokenize the input text using the BERT tokenizer
    inputs = tokenizer(text, padding=True, truncation=True, return_tensors='pt', max_length=512)
    return inputs

# Example input text (sentence)
text = "I absolutely love this product! It's amazing and totally worth it!"

# Step 3: Preprocess the text
inputs = preprocess_text(text)

# Step 4: Make the prediction
with torch.no_grad():  # No need to compute gradients for inference
    outputs = model(**inputs)
    logits = outputs.logits  # Get the logits (raw predictions)

# Step 5: Convert logits to probabilities using the softmax function
probabilities = F.softmax(logits, dim=1)  # Softmax across the second dimension (classes)

# Step 6: Get the predicted class and the probabilities
positive_prob = probabilities[0][1].item()  # Probability of class 1 (positive sentiment)
negative_prob = probabilities[0][0].item()  # Probability of class 0 (negative sentiment)

# Step 7: Print the results as percentages
print(f"Predicted sentiment: Positive: {positive_prob * 100:.2f}% | Negative: {negative_prob * 100:.2f}%")
