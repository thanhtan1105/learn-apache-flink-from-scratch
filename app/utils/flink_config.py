import yaml

with open('app_config.yaml', 'r') as file:
    config = yaml.safe_load(file)

FLINK_CONFIGURE = config['flink']