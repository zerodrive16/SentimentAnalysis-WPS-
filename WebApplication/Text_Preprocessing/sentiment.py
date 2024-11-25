import os
import sys
import django
import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Configure Django Settings for ORM
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SentimentAnalysis.settings')
django.setup()

# Load the trained model and tokenizer from the saved directory
model_path = "sentiment_model"  # Path to the saved model directory
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)

# Ensure the model is set to evaluation mode
model.eval()

# Define the device to use (CPU or GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# New texts to analyze
texts = [
    "I love the beautiful flowers",
]


# Function to preprocess and predict sentiment
def predict_sentiment(texts):
    results = []
    for text in texts:
        # Tokenize the text
        inputs = tokenizer(
            text,
            max_length=128,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        input_ids = inputs["input_ids"].to(device)
        attention_mask = inputs["attention_mask"].to(device)

        # Predict with the model
        with torch.no_grad():
            outputs = model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            predictions = torch.argmax(logits, dim=1).cpu().numpy()

        # Convert predictions to sentiment labels
        sentiment = "Positive" if predictions[0] == 1 else "Negative"
        results.append({"text": text, "sentiment": sentiment})

    return results


# Analyze the texts
results = predict_sentiment(texts)

# Print the results
for result in results:
    print(f"Text: {result['text']}\nPredicted Sentiment: {result['sentiment']}\n")
