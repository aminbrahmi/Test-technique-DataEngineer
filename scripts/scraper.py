import praw
import tweepy
import time
from tweepy.errors import TweepyException
from telethon.sync import TelegramClient
from pymongo import MongoClient
from datetime import datetime
import configparser

# ================= Configuration =================
config = configparser.ConfigParser()
config.read('config/config.ini')

with MongoClient("mongodb://localhost:27017/") as client:
    db = client['harcelement']
    collection = db['posts']
# =================================================

# =============== Reddit Scraper ==================
def scrape_reddit():
    reddit = praw.Reddit(
        client_id=config['REDDIT']['client_id'],
        client_secret=config['REDDIT']['client_secret'],
        user_agent=config['REDDIT']['user_agent']
    )
    subreddits = ['bullying', 'TrueOffMyChest']
    for sub in subreddits:
        for submission in reddit.subreddit(sub).new(limit=100):
            post = {
                'title': submission.title,
                'content': submission.selftext,
                'author': str(submission.author),
                'date': datetime.fromtimestamp(submission.created_utc),
                'url': submission.url,
                'source': 'reddit',
                'processed': False
            }
            collection.update_one({'url': post['url']}, {'$setOnInsert': post}, upsert=True)
            print(f"[Reddit] Added: {post['title'][:50]}...")

# =============== Twitter Scraper (Tweepy) ==================
def scrape_twitter():
    bearer_token = config.get('TWITTER', 'bearer_token', raw=True)
    client = tweepy.Client(bearer_token=bearer_token)
    
    keywords = ['harcèlement', 'bullying', 'cyberbullying']
    max_attempts = 3  # Max retry attempts
    wait_time = 15  # Seconds to wait after hitting rate limit
    
    for keyword in keywords:
        attempts = 0
        success = False
        
        while attempts < max_attempts and not success:
            try:
                tweets = client.search_recent_tweets(
                    query=f'{keyword} lang:fr',
                    max_results=100,
                    tweet_fields=['created_at', 'author_id', 'public_metrics']
                )
                
                if tweets.data:
                    for tweet in tweets.data:
                        post = {
                            'title': f"Tweet by {tweet.author_id}",
                            'content': tweet.text,
                            'author': str(tweet.author_id),
                            'date': tweet.created_at,
                            'url': f"https://twitter.com/user/status/{tweet.id}",
                            'source': 'twitter',
                            'retweets': tweet.public_metrics['retweet_count'],
                            'processed': False
                        }
                        collection.update_one({'url': post['url']}, {'$setOnInsert': post}, upsert=True)
                        print(f"[Twitter] Added: {tweet.text[:50]}...")
                
                success = True
                
            except tweepy.errors.TooManyRequests:
                attempts += 1
                print(f"⚠️ Rate limit exceeded for '{keyword}'. Waiting {wait_time} seconds (attempt {attempts}/{max_attempts})...")
                time.sleep(wait_time)
                wait_time *= 2  # Exponential backoff
                
            except TweepyException as e:
                print(f"❌ Error scraping '{keyword}': {str(e)}")
                break

# =============== Telegram Scraper =================
def scrape_telegram():
    api_id = config.getint("TELEGRAM", "api_id")
    api_hash = config["TELEGRAM"]["api_hash"]
    session_name = config["TELEGRAM"]["session_name"]
    group_name = config["TELEGRAM"]["group_name"]

    with TelegramClient(session_name, api_id, api_hash) as client:
        for message in client.iter_messages(group_name, limit=100):
            if message.text:
                post = {
                    'title': None,
                    'content': message.text,
                    'author': str(message.sender_id),
                    'date': message.date,
                    'url': None,
                    'source': 'telegram',
                    'processed': False
                }
                collection.insert_one(post)
                print(f"[Telegram] Added: {post['content'][:50]}...")

# =============== Main =================
if __name__ == '__main__':
    print("▶️ Starting Scrapers...")
    scrape_reddit()
    scrape_telegram()
    scrape_twitter()
    print("✅ All scraping finished.")
