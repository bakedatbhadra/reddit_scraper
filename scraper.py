import praw
import pandas as pd
from datetime import datetime
from flask import Flask

# Flask app setup
app = Flask(__name__)

# Replace these with your Reddit API credentials
reddit = praw.Reddit(
    client_id="bPdk-ejgnJGF6qkd4DQ-HA",
    client_secret="r_KosazReFacgBpMABy85fFNIua5ew",
    user_agent="my_web_scraper"
)

# Scrape data into a list of dictionaries, including current date
posts = []
scrape_date = datetime.now().strftime("%Y-%m-%d")  # e.g., "2025-02-25"
for post in reddit.subreddit("python").top("week", limit=5):
    posts.append({
        "Date Scraped": scrape_date,
        "Title": post.title,
        "URL": post.url
    })

# Save to Excel
df = pd.DataFrame(posts)
df.to_excel("reddit_posts.xlsx", index=False)

print("Data saved to reddit_posts.xlsx with scrape date!")

# Flask route to display data
@app.route('/')
def show_posts():
    return df.to_html(header=True, index=False)  # HTML table with headers

if __name__ == "__main__":
    app.run(debug=True)