from feedparser import parse
from datetime import datetime

class YoutubeFeed:
    URL = "https://www.youtube.com/feeds/videos.xml?channel_id="

    def __init__(self, channel_id: str, last_run = None, keywords: list = None):
        self.channel_url = self.URL + channel_id
        self.last_run = last_run
        self.keywords = keywords
        self.rss_feed = parse(self.channel_url)

    def _transform_feed(self, video):
        dt_upload = datetime.fromisoformat(video['published'])
        if dt_upload > self.last_run:
            if self.keywords:
                if any(keyword in video["title"] for keyword in self.keywords):
                    return {"title" : video["title"],"url" : video["link"],"date_published" : video['published']}
            else:
                return {"title" : video["title"],"url" : video["link"],"date_published" : video['published']}
        
    def parse_feed(self):
        all_videos = list()
        for video in self.rss_feed['entries']:
            new_video = self._transform_feed(video)
            if new_video:
                all_videos.append(new_video)
        return all_videos