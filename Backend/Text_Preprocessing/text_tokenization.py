import re
import os
import sys
import django

from filter_regex import FilterRegex

# Configure the Settings to set up the correct models.py path for ORM
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..'))
# Pointing to Django Settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SentimentAnalysis.settings')

# Set up ORM to read / write in database
django.setup()

from filter_regex import FilterRegex  # Import the FilterRegex class
from import_csv import Data

# Fetch data from the Django ORM
all_records = Data.objects.all()

# Initialize the FilterRegex object with the fetched records
filter_regex = FilterRegex(all_records)

# Process the data and get the regex-free array
regex_free_data = filter_regex.iterate_data()

# Pass the regex_free_data to another script/module for further processing
another_class = AnotherClass()
another_class.use_data(regex_free_data)
