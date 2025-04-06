import praw
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# --- Get credentials from environment variables ---
CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USERNAME = os.getenv("REDDIT_USERNAME")
PASSWORD = os.getenv("REDDIT_PASSWORD")
USER_AGENT = "script:indian_toxicity:v1.0 (by u/Pure-Association-268)"

# --- Print loaded values for verification ---
print("--- Credentials loaded from environment ---")
print("CLIENT_ID:", CLIENT_ID)
print("CLIENT_SECRET:", CLIENT_SECRET)
print("USERNAME:", USERNAME)
print("PASSWORD:", "****" if PASSWORD else None)
print("-" * 20)

# --- Check if credentials were loaded ---
if not all([CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD]):
    print("❌ Error: One or more Reddit API credentials were not found in the environment variables.")
    print("Ensure you have a .env file in the same directory with:")
    print("REDDIT_CLIENT_ID=your_client_id")
    print("REDDIT_CLIENT_SECRET=your_client_secret")
    print("REDDIT_USERNAME=your_reddit_username")
    print("REDDIT_PASSWORD=your_reddit_password")
    exit()

# --- Initialize Reddit ---
try:
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
        username=USERNAME,
        password=PASSWORD
    )
    print(f"✅ Logged in successfully as: {reddit.user.me()}")

except Exception as auth_error:
    print(f"❌ Authentication failed: {auth_error}")
    exit()

# --- Scraping config ---
subreddits = ["india", "unitedstatesofindia", "IndianPoliticalHumor ", "indianews", "librandu", "IndiaSpeaks", "indiadiscussion","IndiaCricket"]
num_posts = 50
data = []

# --- Begin scraping ---
for subreddit in subreddits:
    print(f"🔍 Scraping from r/{subreddit}")
    try:
        subreddit_obj = reddit.subreddit(subreddit)
        for submission in tqdm(subreddit_obj.hot(limit=num_posts)):
            submission.comments.replace_more(limit=None)  # Fetch all comments
            for comment in submission.comments.list():
                author_name = str(comment.author) if comment.author else "[deleted]"
                data.append({
                    "subreddit": subreddit,
                    "submission_id": submission.id,
                    "submission_title": submission.title,
                    "comment_id": comment.id,
                    "parent_id": comment.parent_id,
                    "author": author_name,
                    "body": comment.body,
                    "score": comment.score,
                    "created_utc": comment.created_utc,
                    "is_submitter": comment.is_submitter
                })
    except praw.exceptions.PRAWException as praw_e:
        print(f"❌ PRAW Error scraping r/{subreddit}: {praw_e}")
    except Exception as e:
        print(f"❌ General Error scraping r/{subreddit}: {e}")

# --- Save to CSV ---
if data:
    df = pd.DataFrame(data)
    df.to_csv("indian_subreddit_comments.csv", index=False)
    print("✅ Data saved to indian_subreddit_comments.csv")
else:
    print("⚠️ No data collected.")

