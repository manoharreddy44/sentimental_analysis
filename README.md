# Twitter Sentiment Analysis Project

This project collects tweets based on a keyword, analyzes sentiment, and explores potential correlations with stock market movements.

## Features

- Twitter API integration to collect tweets
- Sentiment analysis using TextBlob
- Data storage in SQLite database
- Visualization of sentiment distribution
- Stock market impact analysis using Yahoo Finance

## Visualizations

The project provides two main types of data visualizations:

### 1. Sentiment Distribution
This visualization shows the distribution of tweet sentiments (Positive, Negative, Neutral) in a bar chart format.

![Sentiment Distribution Chart](https://drive.google.com/uc?export=view&id=1BfC4bRV-jKAUH59IW9TANOWnsbI_aEQZ)

Features:
- Color-coded bars (Green: Positive, Red: Negative, Blue: Neutral)
- Tweet count labels on each bar
- Clear axis labels and title
- Transparent bars for better visibility

### 2. Stock Price Movement
This visualization displays the intraday stock price movement for the analyzed company.

![Stock Price Movement](https://drive.google.com/uc?export=view&id=1SFktMPfHeYuvoUZ-pp7fsNY8TAopaTGq)

Features:
- 5-minute interval data points
- Interactive time-series plot
- Grid lines for better readability
- Company name and ticker symbol in title
- Price trends throughout trading hours

## Setup

1. Clone the repository:
```bash
git clone https://github.com/manoharreddy44/sentimental_analysis
cd twitter-sentiment-analysis
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Create a `.env` file in the root directory
   - Copy the contents from `example.env`
   - Replace placeholder values with your Twitter API credentials

4. Run the project:
```bash
python sentiment_analysis_project.py
```

## Environment Variables

To use this project, you'll need Twitter API credentials. Create a `.env` file with the following variables:

```
TWITTER_CONSUMER_KEY=your_consumer_key_here
TWITTER_CONSUMER_SECRET=your_consumer_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here
```

## How to Generate Visualizations

1. **Sentiment Distribution Chart**:
   - Automatically generated after analyzing tweets
   - Shows proportion of positive, negative, and neutral sentiments
   - Updates with each new analysis run

2. **Stock Price Movement**:
   - Generated after fetching stock market data
   - Shows real-time price movements
   - Updates with current market data on each run

To save visualizations:
```python
# In sentiment_analysis_project.py
plt.savefig('images/sentiment_distribution.png')  # For sentiment chart
plt.savefig('images/stock_price.png')            # For stock price chart
```

