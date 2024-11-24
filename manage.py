#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# Import snscrape and pandas after Django setup to avoid conflicts
try:
    import snscrape.modules.twitter as twitter
    import pandas as pd
except ImportError:
    raise ImportError(
        "Required modules not found. Install them by running:\n"
        "pip install snscrape pandas"
    )

def scrape_tweets(query, limit=3):
    """
    Scrape tweets using snscrape based on a search query and limit.

    Parameters:
    - query (str): The search query for tweets.
    - limit (int): The maximum number of tweets to retrieve (default is 100).

    Returns:
    - pd.DataFrame: A DataFrame containing tweet date, content, and username.
    """
    # Initialize an empty list to store tweets
    tweets = []

    # Loop through tweets from snscrape based on query
    for i, tweet in enumerate(twitter.TwitterSearchScraper(query).get_items()):
        if i >= limit:  # Stop if the limit is reached
            break
        # Append tweet details to the list
        tweets.append([tweet.date, tweet.content, tweet.user.username])

    # Convert the list to a DataFrame
    tweets_df = pd.DataFrame(tweets, columns=['Date', 'Content', 'Username'])
    return tweets_df


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SentimentAnalysis.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Run Django's command-line utility
    execute_from_command_line(sys.argv)

    # Example usage after Django setup
    if len(sys.argv) == 1 or sys.argv[1] == 'scrape_tweets':
        df = scrape_tweets("openai", limit=3)
        print(df)

if __name__ == '__main__':
    main()