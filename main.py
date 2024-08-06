from src.feeds.applemusic import AppleMusicFeed
from src.feeds.youtube import YoutubeFeed
from src.todoist import TodoistAuth, TodoistApi, TaskManager, Todoist
import json
import datetime
import pytz
from dotenv import load_dotenv
import os

load_dotenv('.env')

TODOIST_PERSONAL_TOKEN = os.getenv('TODOIST_PERSONAL_TOKEN')

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
    todoist = Todoist(TODOIST_PERSONAL_TOKEN)

    feed_handlers = {
        'Apple Music': {
            'feed_class': AppleMusicFeed,
            'entity_key': 'artists',
            'name_key': 'artist',
            'project_id': '2337470474',
            'published_date': 'date_published'
        },
        'YouTube': {
            'feed_class': YoutubeFeed,
            'entity_key': 'channels',
            'name_key': 'channel',
            'project_id': '2337470496',
            'published_date': 'date_published'
        }
    }

    for f in feeds['feeds_type']:
        support = f['support']
        if f['support'] in feed_handlers:
            # Loop through all the channels I have in 'feeds.json'
            handler = feed_handlers[support]
            feed_class = handler['feed_class']
            entity_key = handler['entity_key']
            name_key = handler['name_key']
            project_id = handler['project_id']
            published_date = handler['published_date']

            for entity in f[entity_key]:
                print(f'Analyzing {entity[name_key]}')
                # Initialize the feed parser
                if support == 'Apple Music':
                    feed = feed_class(artist_id=entity['id'], last_run=last_run)
                elif support == 'YouTube':
                    feed = feed_class(entity['id'], last_run, entity.get('keywords'))

                # Parse feed
                news = feed.parse_feed()

                for n in news:
                    date_str = transform_date(n.get(published_date))
                    # Prepare the task
                    task_content = {
                        'content': f'{date_str} - {entity[name_key]} - {n['title']}',
                        'project_id': project_id,
                        'labels': [entity[name_key]],
                        'description': f"{n['url']}"
                    }

                    # Add task
                    new_task = todoist.taskmanager.add_task(task_content)
                    print(f'Added : {task_content["content"]}')

    with open('last_run.json', 'w') as f:
        json.dump({'last_run': datetime.datetime.now().timestamp()}, f)