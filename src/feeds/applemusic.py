from feedparser import parse
from datetime import datetime

class AppleMusicFeed:
    URL = "https://rss-bridge.org/bridge01/?action=display&bridge=AppleMusicBridge&artist=artist_id&limit=10&format=Atom"

    def __init__(self, artist_id: str, last_run = None):
        self.channel_url = f"https://rss-bridge.org/bridge01/?action=display&bridge=AppleMusicBridge&artist={artist_id}&limit=10&format=Atom"
        self.last_run = last_run
        self.rss_feed = parse(self.channel_url)

    def _transform_feed(self, video):
        dt_upload = datetime.fromisoformat(video['published'])
        if dt_upload > self.last_run:
            return {"title" : video["title"],"url" : video["link"],"date_published" : video['published']}
        
    def parse_feed(self):
        all_videos = list()
        for video in self.rss_feed['entries']:
            transformed_video = self._transform_feed(video)
            if transformed_video:
                all_videos.append(transformed_video)
        return all_videos