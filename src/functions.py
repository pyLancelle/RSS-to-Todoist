import datetime
import json
import yaml

def transform_date(date_str):
    # Convertir la chaîne de caractères en objet datetime
    date_obj = datetime.datetime.fromisoformat(date_str)
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return str(formatted_date)

def load_json(filepath):
    f = open(filepath)
    return json.load(f)

def load_config_yaml(yaml_path):
    with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def store_last_run(yaml_path, config):
    # Obtenez le timestamp actuel
    config['last_run'] = datetime.datetime.now().timestamp()
    last_run_datetime = datetime.datetime.fromtimestamp(config['last_run'])
    config['last_run_format'] = last_run_datetime.strftime('%Y-%m-%d %H:%M')
    with open(yaml_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)