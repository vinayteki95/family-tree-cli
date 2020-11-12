import os
import configparser

config = configparser.ConfigParser()
base_config_path = os.path.join(os.path.dirname(__file__), 'config.ini')

def initialize_config_defaults():
    config_path = os.path.expanduser("~")
    config_path = os.path.join(config_path, ".familytree")

    if not os.path.exists(config_path):
        os.mkdir(config_path)

    config['DEFAULT'] = {
        "familytree_image_path": os.path.join(config_path, "cache.png"),
        "relationships_list_path": os.path.join(config_path, "cache.json"),
        "familytree_graph_path": os.path.join(config_path, "cache.graphml"),
    }

    with open(base_config_path, "w") as configfile:
        config.write(configfile)


def read_config():
    if not os.path.exists(base_config_path):
        initialize_config_defaults()
    config.read(base_config_path)
    return config
        