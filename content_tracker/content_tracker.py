import requests
from bs4 import BeautifulSoup
import time

class DataSource:
    def __init__(self, url, title, publication_date, identifier):
        self.url = url
        self.title = title
        self.publication_date = publication_date
        self.identifier = identifier

class Content:
    def __init__(self, content_data, title, url, sources):
        self.content_data = content_data
        self.title = title
        self.url = url
        self.sources = sources
        self.usage_count = 0

    def increment_usage(self):
        self.usage_count += 1

class ContentManager:
    def __init__(self):
        self.contents = {}

    def add_content(self, content):
        self.contents[content.title] = content

    def get_content_info(self, title):
        if title in self.contents:
            content = self.contents[title]
            content.increment_usage()
            return content
        else:
            return None

    def scrape_website(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Scrape article titles (Real Python uses h2 tags for article titles)
        for i, heading in enumerate(soup.find_all('h2', class_='card-title')):
            title = heading.text.strip()
            content_data = title
            identifier = f"{url}-{i}"
            publication_date = time.strftime("%Y-%m-%d")
            source = DataSource(url, title, publication_date, identifier)
            
            content = Content(content_data, title, url, [source])
            self.add_content(content)
            print(f"Scraped and added content: {title}")

    def run(self, url, interval):
        while True:
            print(f"Scraping {url}...")
            self.scrape_website(url)
            time.sleep(interval)

# Example usage:
url_to_track = "https://realpython.com/"
manager = ContentManager()
manager.run(url_to_track, 3600)  # Scrapes every hour
