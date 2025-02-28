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
        for record in all_records:
            comment_regex = self.performRegex(record.comment_body)
            record.comment_body_adjusted = comment_regex
            record.save()


    def performRegex(self, comment_body):

        # Remove emojis and non-printable characters
        cleaned_comment = re.sub(r'[^\x00-\x7F]+', '', comment_body)
        # Remove special characters, keeping only letters and numbers (', !, ., ?, +, -, and ,)
        cleaned_comment = re.sub(r'[^a-zA-Z0-9\s\'!,\.\?\+\-]', '', cleaned_comment)
        # Remove extra spaces
        cleaned_comment = re.sub(r'\s+', ' ', cleaned_comment).strip()

        return cleaned_comment


if __name__ == '__main__':
    all_records = Data.objects.all()
    filterRegex = FilterRegex(all_records)
    filterRegex.iterateData()


