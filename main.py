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
print(TODOIST_PERSONAL_TOKEN)
FEEDS_FILE_PATH = 'feeds.json'
# LAST_RUN = datetime.datetime.fromtimestamp(1700823521, pytz.UTC)

def transform_date(date_str):
    # Convertir la chaîne de caractères en objet datetime
    date_obj = datetime.datetime.fromisoformat(date_str)
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return str(formatted_date)


if __name__ == '__main__':
    f = open('feeds.json')
    feeds = json.load(f)

    lr = open('last_run.json')
    last_run = datetime.datetime.fromtimestamp(json.load(lr)['last_run'], pytz.UTC)

    # Todoist initialization
    # TODO : simplifier ce truc en faisant un TodoistOrchestrator, truc du style, c'est dégueu d'avoir 3 initialisations.
    todoist_auth = TodoistAuth(TODOIST_PERSONAL_TOKEN)
    todoist_api = TodoistApi(todoist_auth)
    todoist_task_manager = TaskManager(todoist_api)

    # feed_handlers = {
    #     'Apple Music': {
    #         'feed_class': AppleMusicFeed,
    #         'entity_key': 'artists',
    #         'name_key': 'artist',
    #         'project_id': '2336934522'
    #     },
    #     'YouTube': {
    #         'feed_class': YoutubeFeed,
    #         'entity_key': 'channels',
    #         'name_key': 'channel',
    #         'project_id': '2336934512'
    #     }
    # }

    for f in feeds['feeds_type']:
        # Apple Music
        if f['support'] == 'Apple Music':
            # Loop through all the channels I have in 'feeds.json'

            for artist in f['artists']:
                print(f'Analyse de {artist['artist']}')
                # Load the Apple Music feed parser
                amf = AppleMusicFeed(artist_id=artist['id'], last_run=last_run)

                # Parse feed
                news = amf.parse_feed()

                for n in news:
                    date_str = transform_date(n['date_published'])
                    # Prepare the task
                    task_content = {
                        'content': f'{date_str} - {artist['artist']} - {n['title']}',
                        'project_id': '2337470474',
                        'labels': artist['tags'], 
                        'description' : n['url']
                    }

                    # Load the task
                    new_task = todoist_task_manager.add_task(task_content)

        if f['support'] == 'YouTube':
            # Loop through all the channels I have in 'feeds.json'

            for channel in f['channels']:
                print(f'Analyse de {channel['channel']}')
                # Load the YouTube feed parser
                yt = YoutubeFeed(channel['id'], last_run, channel.get('keywords'))

                # Parse feed
                news = yt.parse_feed()

                for n in news:
                    # Format date
                    date_str = transform_date(n['date_published'])
                    # Prepare the task
                    task_content = {
                        'content': f'{date_str} - {channel['channel']} - {n['title']}',
                        'project_id': '2337470496',
                        'labels': channel['tags'], 
                        'description' : f"{n['url']}"
                    }

                    # Load the task
                    new_task = todoist_task_manager.add_task(task_content)

        with open('last_run.json', 'w') as f:
            json.dump({'last_run': datetime.datetime.now().timestamp()}, f)


