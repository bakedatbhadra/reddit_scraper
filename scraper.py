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
for post in reddit.subreddit("youtube").top("week", limit=20):
    posts.append({
        "Date Posted": datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d'),
        "Title": post.title,
        "URL": post.url,
        "Score": post.score,
        "Date Scraped": scrape_date 
    })
# Add the body of posts into a mail merge type email format
with open("reddit_posts_email.txt", 'w', encoding="utf-8") as f:
    for post in posts:
        f.write(f"Subject: {post['Title']}\nURL: {post['URL']}\nScore: {post['Score']}\nDate: {post['Date Scraped']}\n\n")


# Save to Excel and .csv
df = pd.DataFrame(posts)
df.to_excel("reddit_posts.xlsx", index=False)
df.to_csv("posts_for_analysis")
print("Data saved to reddit_posts.xlsx with scrape date!")
print("Data saved to posts_for_analysis.csv with scrape date!")


# basic analysis using pandas
count_posts = len(df.Score)
max_score = max(df.Score)
row_with_max_score = df[df.Score==max_score]
post_title_with_max_score = row_with_max_score.loc[row_with_max_score.index[0],'Title']
print(f"Count of posts scraped ={count_posts}")
print(f"MaxScore ={max_score}")
print(row_with_max_score)
print(post_title_with_max_score)

# Flask route to display data
# @app.route('/')
# def show_posts():
#     return df.to_html(header=True, index=False)  # HTML table with headers

# if __name__ == "__main__":
#     app.run(debug=False, host='0.0.0.0', port=5001)  # Changed to port 5001