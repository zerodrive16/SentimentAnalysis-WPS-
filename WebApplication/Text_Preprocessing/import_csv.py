import csv
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


class ImportCSVData:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def readData(self):
        with open(self.csv_path, 'r', errors='ignore') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            next(csv_reader)

            for line in csv_reader:
                data = self.parseData(line)

                data.save()

    def parseData(self, line):
        return Data(
            id=line[0],
            post_id=line[1],
            post_author=line[2],
            post_title=line[3],
            post_created=int(line[4]),
            post_upvotes=int(line[5]),
            comment_id=line[6],
            comment_author=line[7],
            comment_body=line[8],
            comment_created=int(line[9]),
            comment_upvotes=int(line[10]),
            subreddit=line[11]
        )


# Get Absolute Path till 2nd parent folder
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(base_path, 'Dataset', 'Dataset.csv')

sendCSV = ImportCSVData(csv_path)
sendCSV.readData()