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
        if f['support'] == 'Apple Music':
            for artist in f['artists']:
                amf = AppleMusicFeed(artist['id'], last_run = last_run)
                news = amf.parse_feed()
                # Create the section
                new_section = todoist_task_manager.add_section('2336934522', artist['artist'])
                if not new_section:
                    for s in todoist_task_manager.get_all_sections('2336934522'):
                        if s['name'] == artist['artist']:
                            new_section = {'id' : s['id']}
                            break
                for n in news:
                    liste_tasks = todoist_task_manager.get_all_tasks(new_section['id'])
                    for t in liste_tasks:
                        if t['content'] == n['title']:
                            flag_stop = True
                    if not flag_stop:
                        n['tags'] = artist['tags']
                        n['artist'] = artist['artist']
                        task_content = {
                            'content': n['title'], 
                            'section_id': new_section['id'], 
                            'project_id': '2336934522',
                            'labels': n['tags'], 
                            'description' : f"{n['url']}\n{n['date_published']}"
                        }
                        new_task = todoist_task_manager.add_task(task_content)
        if f['support'] == 'YouTube':
            pass

        with open('last_run.json', 'w') as f:
            json.dump({'last_run': datetime.datetime.now().timestamp()}, f)


