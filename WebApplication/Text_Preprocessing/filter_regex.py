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

from WebApplication.models import Data


class FilterRegex:
    def __init__(self, records):
        self.records = records


    def iterateData(self):
        comment_body_array = []
        for record in all_records:
            comment_body_array.append(record.comment_body)

        return self.performRegex(comment_body_array)

    def performRegex(self, comment_body_array):
        regex_free_array = []

        for comment in comment_body_array:
            # Remove emojis and non-printable characters
            cleaned_comment = re.sub(r'[^\x00-\x7F]+', '', comment)
            # Remove special characters, keeping only letters and numbers
            cleaned_comment = re.sub(r'[^a-zA-Z0-9\s]', '', cleaned_comment)
            # Remove extra spaces
            cleaned_comment = re.sub(r'\s+', ' ', cleaned_comment).strip()

            regex_free_array.append(cleaned_comment)

        return regex_free_array


all_records = Data.objects.all()
filterRegex = FilterRegex(all_records)
filterRegex.iterateData()


