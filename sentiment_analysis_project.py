import tweepy
import pandas as pd
from textblob import TextBlob
import sqlite3
import matplotlib.pyplot as plt
import re
import yfinance as yf
from yahooquery import search
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ------------------------------
# Twitter API credentials
# Load from environment variables
# ------------------------------
consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

# ------------------------------
# Authenticate Twitter API
# ------------------------------
def authenticate_twitter():
    try:
        client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        print("✅ Twitter API authenticated successfully.")
        return client
    except Exception as e:
        print(f"❌ Error authenticating Twitter API: {e}")
        return None

# ------------------------------
# Collect tweets based on a keyword
# ------------------------------
def collect_tweets(api, keyword, count=100):
    tweets_data = []
    try:
        tweets = api.search_recent_tweets(query=keyword, max_results=min(count, 100), tweet_fields=["created_at", "text"])
        if not tweets.data:
            print(f"⚠️ No tweets found for keyword: {keyword}")
            return pd.DataFrame()

        for tweet in tweets.data:
            tweets_data.append({
                "text": tweet.text,
                "created_at": tweet.created_at
            })
    except tweepy.errors.TweepyException as e:
        print(f"❌ Error collecting tweets: {e}")
    return pd.DataFrame(tweets_data)

# ------------------------------
# Clean tweet text
# ------------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove non-alphabet characters
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

# ------------------------------
# Analyze sentiment
# ------------------------------
def analyze_sentiment(text):
    sentiment = TextBlob(text).sentiment.polarity
    if sentiment > 0:
        return "Positive"
    elif sentiment < 0:
        return "Negative"
    else:
        return "Neutral"

# ------------------------------
# Store tweets in SQLite database
# ------------------------------
def store_data(df, db_name="tweets_data.db"):
    try:
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
        print("💾 Data stored in SQLite database successfully.")
    except Exception as e:
        print(f"❌ Error storing data in database: {e}")

# ------------------------------
# Visualize sentiment distribution
# ------------------------------
def visualize_sentiment_distribution(df):
    if df.empty:
        print("⚠️ No data to visualize sentiment distribution.")
        return
    sentiment_counts = df["sentiment"].value_counts()
    sentiment_counts.plot(kind="bar", color=["green", "red", "blue"], alpha=0.7)
    plt.title("Sentiment Distribution")
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Tweets")
    for i, value in enumerate(sentiment_counts):
        plt.text(i, value, str(value), ha='center', va='bottom')
    plt.tight_layout()
    plt.show()

# ------------------------------
# Get stock ticker symbol
# ------------------------------
def get_stock_ticker(company_name):
    try:
        search_results = search(company_name)
        quotes = search_results.get("quotes", [])
        if quotes:
            return quotes[0]["symbol"]
        else:
            print(f"⚠️ No ticker symbol found for '{company_name}'.")
            return None
    except Exception as e:
        print(f"❌ Error retrieving stock ticker: {e}")
        return None

# ------------------------------
# Analyze stock market impact
# ------------------------------
def analyze_market_impact(company_name):
    ticker = get_stock_ticker(company_name)
    if not ticker:
        print(f"⚠️ Cannot analyze market impact without a valid ticker for '{company_name}'.")
        return

    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period="1d", interval="5m")
        if history.empty:
            print(f"⚠️ No market data available for {company_name} ({ticker}).")
            return

        history['Close'].plot(title=f"{company_name} ({ticker}) Stock Price Movement", figsize=(10, 5))
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"❌ Error analyzing market impact: {e}")

# ------------------------------
# Main Program
# ------------------------------
if __name__ == "__main__":
    api = authenticate_twitter()
    if api:
        keyword = "Apple"
        print(f"📥 Collecting tweets for keyword: {keyword}")
        tweets_df = collect_tweets(api, keyword, count=50)

        if not tweets_df.empty:
            print("🧹 Cleaning tweets...")
            tweets_df["cleaned_text"] = tweets_df["text"].apply(clean_text)

            print("🧠 Analyzing sentiment...")
            tweets_df["sentiment"] = tweets_df["cleaned_text"].apply(analyze_sentiment)

            print("📦 Storing data...")
            store_data(tweets_df)

            print("📊 Visualizing sentiment distribution...")
            visualize_sentiment_distribution(tweets_df)

        print("💹 Analyzing market impact...")
        analyze_market_impact(keyword)
