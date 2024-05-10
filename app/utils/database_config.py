import yaml

with open('app_config.yaml', 'r') as file:
    config = yaml.safe_load(file)

DATABASE_CONFIG = config['database']