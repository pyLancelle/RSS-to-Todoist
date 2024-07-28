from feedparser import parse
from datetime import datetime

class YoutubeFeed:
    URL = "https://www.youtube.com/feeds/videos.xml?channel_id="

    def __init__(self, channel_id: str, last_run = None, keywords: list = None):
        self.channel_url = self.URL + channel_id
        self.last_run = last_run
        self.keywords = keywords

    def parse_feed(self):
        feed = parse(self.channel_url)

        video_feed = list()
        for video in feed['entries']:
            dt_upload = datetime.fromisoformat(video['published'])
            print(f'Date video : {dt_upload}\nDate seuil : {self.last_run}\n\n')
            if (dt_upload > self.last_run):
                if any(keyword in video["title"] for keyword in self.keywords):
                    video_feed.append({"title" : video["title"],"url" : video["link"],"date_published" : video['published']})
            
        return video_feed



