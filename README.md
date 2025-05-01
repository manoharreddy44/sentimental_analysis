# Twitter Sentiment Analysis Project

This project collects tweets based on a keyword, analyzes sentiment, and explores potential correlations with stock market movements.

## Features

- Twitter API integration to collect tweets
- Sentiment analysis using TextBlob
- Data storage in SQLite database
- Visualization of sentiment distribution
- Stock market impact analysis using Yahoo Finance

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/twitter-sentiment-analysis.git
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

## License

MIT 