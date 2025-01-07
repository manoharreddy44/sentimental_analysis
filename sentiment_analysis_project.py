import tweepy
import pandas as pd
from textblob import TextBlob
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import re

# Twitter API credentials (Replace these with your actual credentials)
consumer_key = 'JTDdjtDO2u5FTFHcJGKx7oTRJ'  # Replace with your consumer key
consumer_secret = 'oIC6hdNMakbO7pHK3aZQYBe0Nfkw4RAzgxtU4m6lQ0dEH2cSkC'  # Replace with your consumer secret
access_token = '1659960641808109568-TS1Ek5xvJGxX26z7rVDvpPyW1kCyMC' # Replace with your access token
access_token_secret = '4fkil6IgaJwPGyZyKYCebpgNXRGa6kHeyqtkrNIwXlvdX'  # Replace with your access token secret

# Authenticate with Twitter
def authenticate_twitter():
    client = tweepy.Client(
        bearer_token='AAAAAAAAAAAAAAAAAAAAAKbwxwEAAAAAZnN%2BTWv1zLQhK2oxj2sDcSCebKM%3DjLp30P7V4e0VAHDMDVjjJ52FqUmsd9rpzT0Hxk2nuGlLmytT8H',
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    return client


# Collect tweets based on a keyword or hashtag
def collect_tweets(api, keyword, count=100):
    tweets_data = []
    try:
        tweets = api.search_recent_tweets(query=keyword, max_results=count, tweet_fields=["created_at", "text"])
        for tweet in tweets.data:
            tweets_data.append({
                "text": tweet.text,
                "created_at": tweet.created_at,
            })
    except tweepy.errors.TweepyException as e:
        print(f"Error: {e}")
    return pd.DataFrame(tweets_data)


# Clean tweet text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra whitespaces
    return text

# Analyze sentiment
def analyze_sentiment(text):
    sentiment = TextBlob(text).sentiment.polarity
    if sentiment > 0:
        return "Positive"
    elif sentiment < 0:
        return "Negative"
    else:
        return "Neutral"

# Store data into SQLite database
def store_data(df, db_name="tweets_data.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tweets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        created_at TEXT,
        cleaned_text TEXT,
        sentiment TEXT
    )
    ''')
    df.to_sql("tweets", conn, if_exists="append", index=False)
    conn.close()

# Analyze sentiment distribution
def get_sentiment_distribution(df):
    sentiment_counts = df["sentiment"].value_counts()
    return sentiment_counts

# Visualize sentiment distribution
def visualize_sentiment_distribution(sentiment_dist):
    sentiment_dist.plot(kind="bar", color=["green", "red", "blue"], alpha=0.7)
    plt.title("Sentiment Distribution")
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Tweets")
    for i, value in enumerate(sentiment_dist):
        plt.text(i, value, str(value), ha='center', va='bottom')  # Add value labels
    plt.show()

if __name__ == "__main__":
    # Step 1: Authenticate with Twitter
    api = authenticate_twitter()

    # Step 2: Collect Tweets
    keyword = "medicine"  # Replace "technology" with your desired keyword/hashtag
    print(f"Collecting tweets for keyword: {keyword}")
    tweets_df = collect_tweets(api, keyword, count=50)  # Replace 200 with your desired tweet count

    # Step 3: Clean Tweets
    print("Cleaning tweets...")
    tweets_df["cleaned_text"] = tweets_df["text"].apply(clean_text)

    # Step 4: Analyze Sentiment
    print("Analyzing sentiment...")
    tweets_df["sentiment"] = tweets_df["cleaned_text"].apply(analyze_sentiment)

    # Step 5: Store Data
    print("Storing data into database...")
    store_data(tweets_df)

    # Step 6: Analyze and Visualize Trends
    print("Analyzing sentiment distribution...")
    sentiment_dist = get_sentiment_distribution(tweets_df)
    print("Sentiment Distribution:\n", sentiment_dist)

    print("Visualizing sentiment distribution...")
    visualize_sentiment_distribution(sentiment_dist)
