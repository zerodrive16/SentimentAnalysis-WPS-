import torch
from django.http import JsonResponse
from django.shortcuts import render
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Data
from .serializers import DataSerializer

# Model and Tokenizer
preTrainedModel = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(preTrainedModel)
model = AutoModelForSequenceClassification.from_pretrained(preTrainedModel)

# Settings up the device
device = torch.device("cuda" if torch.cuda.is_available() else torch.device("cpu"))
model.to(device)
model.eval()


# Calling the Web Application
def home(request):
    return render(request, "index.html")


def dataset(request):
    data = list(Data.objects.values())
    return JsonResponse(data, safe=False)


def dataset_retrieval(request):
    data = list(Data.objects.values())
    return JsonResponse(data, safe=False)


class PostAcceptance(APIView):
    def post(self, request):
        try:
            input_data = request.data
            # Tokenizing
            inputs = tokenizer([input_data.get('comment_body_adjusted')], padding=True, truncation=True,
                               return_tensors="pt", max_length=512).to(device)
            with torch.no_grad():
                outputs = model(**inputs)
                probabilities = torch.nn.functional.softmax(outputs[0], dim=1)
                predictions = torch.argmax(probabilities, dim=1).item()

            input_data['comment_bert_labels'] = predictions

            newComment = Data.objects.create(
                post_id=input_data.get('post_id'),
                post_author=input_data.get('post_author'),
                post_title=input_data.get('post_title'),
                post_created=input_data.get('post_created'),
                post_up_votes=input_data.get('post_up_votes'),
                c_id=input_data.get('c_id'),
                comment_id=input_data.get('comment_id'),
                comment_author=input_data.get('comment_author'),
                comment_body=input_data.get('comment_body'),
                comment_body_adjusted=input_data.get('comment_body_adjusted'),
                comment_created=input_data.get('comment_created'),
                comment_up_votes=input_data.get('comment_up_votes'),
                subreddit=input_data.get('subreddit'),
                comment_personal_labels=input_data.get('comment_personal_labels'),
                comment_bert_labels=input_data.get('comment_bert_labels')
            )

            serializedData = DataSerializer(newComment).data
            return Response(serializedData, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            allData = Data.objects.all()
            serializedData = DataSerializer(allData, many=True).data
            return Response(serializedData, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

