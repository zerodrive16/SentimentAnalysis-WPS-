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
from django.db import transaction


class ImportCSVData:
    # Initialize both Dataset
    def __init__(self, csv_path_post_dataset, csv_path_comment_dataset):
        self.csv_path_post_dataset = csv_path_post_dataset
        self.csv_path_comment_dataset = csv_path_comment_dataset

    @transaction.atomic
    def readData(self):
        # Open the Post Dataset first
        with open(self.csv_path_post_dataset, 'r', errors='ignore') as csv_post_file:
            csv_post_reader = csv.reader(csv_post_file, delimiter=',')
            # Skip the Header
            next(csv_post_reader)

            # Iterate over the post_dataset
            for post_line in csv_post_reader:
                post_id = post_line[0] # Take the Post ID

                # Finding matched ids from post and comment
                match_post_comment = self.findMatchId(post_id)

                for comment_line in match_post_comment:
                    dataOutput = self.parseData(post_line, comment_line)
                    dataOutput.save()

    def findMatchId(self, post_id):
        # Find all the Comments that match with the Post Id
        match_comments = []

        with open(self.csv_path_comment_dataset, 'r', errors='ignore') as csv_comment_file:
            csv_comment_reader = csv.reader(csv_comment_file, delimiter=',')
            # Skip the Header
            next(csv_comment_reader)

            post_id = int(post_id)

            # Iterate over the Comments and check till the id sequence is higher than post_id
            for comment_line in csv_comment_reader:
                check_current_comment = int(comment_line[0])
                if check_current_comment == post_id:
                    match_comments.append(comment_line)
                elif check_current_comment > post_id:
                    break

        return match_comments

    def parseData(self, post_line, comment_line):
        return Data(
            post_id=post_line[1],
            post_author=post_line[2],
            post_title=post_line[3],
            post_created=int(post_line[4]),
            post_up_votes=int(post_line[5]),
            c_id=int(comment_line[0]),
            comment_id=comment_line[1],
            comment_author=comment_line[2],
            comment_body=comment_line[3],
            comment_body_adjusted=comment_line[4],
            comment_created=int(comment_line[5]),
            comment_up_votes=int(comment_line[6]),
            subreddit=comment_line[7],
            comment_personal_labels=int(comment_line[8]),
            comment_bert_labels=int(comment_line[9])
        )



if __name__ == '__main__':
    print("Starting script: \n")

    # Get Absolute Path till 2nd parent folder to retrieve the files
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path_post_dataset = os.path.join(base_path, 'Dataset', 'Post_Dataset.csv')
    csv_path_comment_dataset = os.path.join(base_path, 'Dataset', 'Comment_Dataset.csv')

    sendCSV = ImportCSVData(csv_path_post_dataset, csv_path_comment_dataset)
    sendCSV.readData()

    print("End of script")