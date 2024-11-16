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

from Backend_ML.models import Data


# Get Absolute Path till 2nd parent folder
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(base_path, 'Dataset', 'Dataset.csv')

# Need to write in western code (encoding='cp850', errors='ignore')
# reason = special characters from other countries
with open(csv_path, 'r', errors='ignore') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')

    next(csv_reader)

    for line in csv_reader:
        data_id = line[0]
        link_author = line[1]
        author = line[2]
        title = line[3]
        time_posted = int(line[4])
        body_information = line[5]

        data = Data(
            id=data_id,
            link_author=link_author,
            author=author,
            title=title,
            time_posted=time_posted,
            body_information=body_information
        )

        data.save()

