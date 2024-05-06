import yaml

with open('app_config.yaml', 'r') as file:
    config = yaml.sefe_load(file, Loader=yaml.FullLoader)

FLINK_CONFIGURE = config['flink']

print(FLINK_CONFIGURE)