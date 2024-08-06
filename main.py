from src.feeds.applemusic import AppleMusicFeed
from src.feeds.youtube import YoutubeFeed
from src.todoist import Todoist
from src.functions import transform_date, load_json, load_config_yaml, store_last_run
import json
import datetime
import pytz
from dotenv import load_dotenv
import os

CONFIGURATION_FILEPATH = 'configuration.yaml'

if __name__ == '__main__':
    # Load the environment and get the TODOIST_PERSONAL_TOKEN
    load_dotenv('.env')
    TODOIST_PERSONAL_TOKEN = os.getenv('TODOIST_PERSONAL_TOKEN')

    # Load the YAML config
    config = load_config_yaml(CONFIGURATION_FILEPATH)

    # Create variables
    FEEDS_FILEPATH = config['feeds_filepath']
    LAST_RUN = config['last_run']
    APPLEMUSIC_PROJECT_ID = config['todoist']['music_project_id']
    YOUTUBE_PROJECT_ID = config['todoist']['youtube_project_id']

    # Load elements
    feeds = load_json(FEEDS_FILEPATH)
    last_run = datetime.datetime.fromtimestamp(LAST_RUN, pytz.UTC)

    # Todoist initialization
    todoist = Todoist(TODOIST_PERSONAL_TOKEN)

    feed_handlers = {
        'Apple Music': {
            'feed_class': AppleMusicFeed,
            'entity_key': 'artists',
            'name_key': 'artist',
            'project_id': APPLEMUSIC_PROJECT_ID,
            'published_date': 'date_published'
        },
        'YouTube': {
            'feed_class': YoutubeFeed,
            'entity_key': 'channels',
            'name_key': 'channel',
            'project_id': YOUTUBE_PROJECT_ID,
            'published_date': 'date_published'
        }
    }

    for f in feeds['feeds_type']:
        support = f['support']
        if support in feed_handlers:
            # Loop through all the entities I have in 'feeds.json'
            handler = feed_handlers[support]
            feed_class = handler['feed_class']
            entity_key = handler['entity_key']
            name_key = handler['name_key']
            project_id = handler['project_id']
            published_date = handler['published_date']

            for entity in f[entity_key]:
                print(f'Analyzing {entity[name_key]}')
                if support == 'Apple Music':
                    feed = feed_class(
                        artist_id=entity['id'], 
                        last_run=last_run
                    )
                elif support == 'YouTube':
                    feed = feed_class(
                        channel_id=entity['id'], 
                        last_run=last_run, 
                        keywords=entity.get('keywords')
                    )
                elif support == 'Podcast':
                    pass
                else:
                    pass

                # Parse feed
                news = feed.parse_feed()
                print(f'Found {len(news)} entries.')

                for n in news:
                    # Prepare the task into a todoist Format
                    task_content = {
                        'content': f'{n['title']}',
                        'project_id': project_id,
                        'labels': [entity[name_key]],
                        'description': f"{n['url']}"
                    }

                    # Add task in Todoist
                    new_task = todoist.taskmanager.add_task(task_content)
                    print(f'Added : {task_content["content"]}')

    store_last_run(CONFIGURATION_FILEPATH, config)