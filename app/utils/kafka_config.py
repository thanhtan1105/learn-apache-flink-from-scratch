import yaml

with open('app_config.yaml', 'r') as file:
    config = yaml.safe_load(file)

KAFKA_CONFIG = config['kafka']

