import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import random

# Define the URL and the date range
url = "https://support.mozilla.org/en-US/questions/firefox?show=all"
end_date = datetime(2024, 11, 12)
start_date = datetime(2024, 10, 1)


# Function to parse the date from the post
def parse_date(date_str):
    return datetime.strptime(date_str, "%B %d, %Y")


# Function to check if the post date is within the desired range
def is_within_date_range(post_date):
    return start_date <= post_date <= end_date


# Function to extract posts from a page
def extract_posts(soup):
    posts = []
    for post in soup.find_all("div", id=lambda x: x and x.startswith("question-")):
        date_str = post.find("time")["datetime"]
        post_date = datetime.fromisoformat(date_str)
        if is_within_date_range(post_date):
            title = post.find("h2", class_="summary").text.strip()
            link = (
                "https://support.mozilla.org"
                + post.find("a", class_="question-hyperlink")["href"]
            )
            question_text = post.find("div", itemprop="text").text.strip()
            responses = [
                response.text.strip()
                for response in post.find_all("div", class_="reply")
            ]
            posts.append(
                {
                    "date": post_date,
                    "title": title,
                    "link": link,
                    "question_text": question_text,
                    "responses": responses,
                }
            )
    return posts


# Function to get the next page URL
def get_next_page(soup):
    next_button = soup.find("a", class_="next")
    if next_button:
        return "https://support.mozilla.org" + next_button["href"]
    return None


# Main function to crawl the website
def crawl_website(url):
    all_posts = []
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        posts = extract_posts(soup)
        all_posts.extend(posts)
        url = get_next_page(soup)

        # Add a delay to avoid getting rate-limited
        time.sleep(random.uniform(1, 3))  # Wait for 1 to 3 seconds randomly

    return all_posts


# Crawl the website and save the data
posts = crawl_website(url)
df = pd.DataFrame(posts)
df.to_csv("mozilla_support_posts.csv", index=False)

print(f"Saved {len(posts)} posts to 'mozilla_support_posts.csv'")
