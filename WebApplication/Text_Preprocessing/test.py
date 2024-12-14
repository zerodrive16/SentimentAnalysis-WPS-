import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os
import sys
import django
from tqdm import tqdm
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SentimentAnalysis.settings')
django.setup()
from WebApplication.models import Data

# Model and Tokenizer
preTrainedModel = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(preTrainedModel)
model = AutoModelForSequenceClassification.from_pretrained(preTrainedModel)

# Settings up the device
device = torch.device("cuda" if torch.cuda.is_available() else torch.device("cpu"))
model.to(device)
model.eval()


def retrieveDataset():
    # Retrieve the Dataset (finished Regex comment)
    dataset = Data.objects.values('comment_body_adjusted')
    comments = [entry['comment_body_adjusted'] for entry in dataset]
    return comments


def predictSentiment(commentsAdjusted):
    # Tokenize and predict the sentiment analysis
    inputs = tokenizer(commentsAdjusted, padding=True, truncation=True, return_tensors="pt", max_length=512).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    # Converting to probabilities
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    # predict the highest probability e.g. [0.25, 0.75] = 1
    predictions = torch.argmax(probabilities, dim=-1)
    return predictions.cpu().numpy()


def updateDataset(commentsAdjusted, sentimentPrediction):
    # Tqdm to see the terminal output
    # Update the change to models.py to corresponding comment
    for comment, prediction in tqdm(zip(commentsAdjusted, sentimentPrediction), total=len(commentsAdjusted), desc="Updating database"):
        Data.objects.filter(comment_body_adjusted=comment).update(comment_bert_labels=prediction)


def main():
    # Call the dataset
    commentsAdjusted = retrieveDataset()

    # Call the Sentiment prediction
    print("Predicting sentiment...")
    sentimentPrediction = predictSentiment(commentsAdjusted)

    # Update the dataset
    print("Update database...")
    updateDataset(commentsAdjusted, sentimentPrediction)

if __name__ == "__main__":
    main()


