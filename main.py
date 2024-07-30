from src.feeds.applemusic import AppleMusicFeed
from src.feeds.youtube import YoutubeFeed
from src.todoist import TodoistAuth, TodoistApi, TaskManager
import json
import datetime
import pytz
import pprint
from dotenv import load_dotenv
import os

load_dotenv('.env')

TODOIST_PERSONAL_TOKEN = os.getenv('TODOIST_PERSONAL_TOKEN')

FEEDS_FILE_PATH = 'feeds.json'
# LAST_RUN = datetime.datetime.fromtimestamp(1700823521, pytz.UTC)

if __name__ == '__main__':
    f = open('feeds.json')
    feeds = json.load(f)

    lr = open('last_run.json')
    last_run = datetime.datetime.fromtimestamp(json.load(lr)['last_run'], pytz.UTC)

    # Todoist initialization
    todoist_auth = TodoistAuth(TODOIST_PERSONAL_TOKEN)
    todoist_api = TodoistApi(todoist_auth)
    todoist_task_manager = TaskManager(todoist_api)

    for f in feeds['feeds_type']:
        # Apple Music
        if f['support'] == 'Apple Music':
            # Loop through all the channels I have in 'feeds.json'

            for artist in f['artists']:
                # Load the Apple Music feed parser
                amf = AppleMusicFeed(artist_id=artist['id'], last_run=last_run)

                # Parse feed
                news = amf.parse_feed()

                # Create the section
                new_section = todoist_task_manager.add_section(project_id='2336934522', section_name=artist['artist'])

                for n in news:
                    # Prepare the task
                    task_content = {
                        'content': artist['artist'] + ' - ' + n['title'], 
                        'section_id': new_section['id'], 
                        'project_id': '2336934522',
                        'labels': artist['tags'], 
                        'description' : f"{n['url']}\n{n['date_published']}"
                    }

                    # Load the task
                    new_task = todoist_task_manager.add_task(task_content)

        if f['support'] == 'YouTube':
            # Loop through all the channels I have in 'feeds.json'

            for channel in f['channels']:
                # Load the YouTube feed parser
                yt = YoutubeFeed(channel['id'], last_run, channel.get('keywords'))

                # Parse feed
                news = yt.parse_feed()

                # Create the section
                new_section = todoist_task_manager.add_section('2336934512', channel['channel'])

                for n in news:
                    # Prepare the task
                    task_content = {
                        'content': channel['channel'] + ' - ' + n['title'], 
                        'section_id': new_section['id'], 
                        'project_id': '2336934512',
                        'labels': channel['tags'], 
                        'description' : f"{n['url']}\n{n['date_published']}"
                    }

                    # Load the task
                    new_task = todoist_task_manager.add_task(task_content)

        with open('last_run.json', 'w') as f:
            json.dump({'last_run': datetime.datetime.now().timestamp()}, f)


