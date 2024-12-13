import torch
from transformers import BertTokenizer, BertForSequenceClassification
import os

# Load the fine-tuned model and tokenizer
model_dir = "sentiment_model"
if not os.path.exists(model_dir):
    raise FileNotFoundError(f"Model directory '{model_dir}' not found. Please ensure the model is saved in this location.")

model = BertForSequenceClassification.from_pretrained(model_dir)
tokenizer = BertTokenizer.from_pretrained(model_dir)

# Set the device
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model.to(device)
model.eval()

def predict_sentiment(text):
    """Predicts the sentiment of the given text using the fine-tuned BERT model."""
    # Tokenize and prepare input
    encoding = tokenizer(text, truncation=True, padding=True, max_length=128, return_tensors="pt")
    encoding = {key: val.to(device) for key, val in encoding.items()}

    with torch.no_grad():
        outputs = model(**encoding)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()

    return "Positive" if predicted_class == 1 else "Negative"

def calculate_percentages(comments):
    """Calculates the percentage of positive and negative comments."""
    positive_count = 0
    negative_count = 0

    for comment in comments:
        sentiment = predict_sentiment(comment)
        if sentiment == "Positive":
            positive_count += 1
        else:
            negative_count += 1

    total = positive_count + negative_count
    positive_percentage = (positive_count / total) * 100 if total > 0 else 0
    negative_percentage = (negative_count / total) * 100 if total > 0 else 0

    return positive_percentage, negative_percentage

# Example usage
if __name__ == "__main__":
    comments = []
    while True:
        text = input("Enter a comment to analyze sentiment (or 'done' to finish input and calculate percentages): ")
        if text.lower() == 'done':
            break
        comments.append(text)

    if comments:
        positive_percentage, negative_percentage = calculate_percentages(comments)
        print(f"Positive Sentiment: {positive_percentage:.2f}%")
        print(f"Negative Sentiment: {negative_percentage:.2f}%")
    else:
        print("No comments were provided.")
