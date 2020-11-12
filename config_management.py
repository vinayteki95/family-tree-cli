import os
import configparser

config = configparser.ConfigParser()

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

    with open('config.ini', "w") as configfile:
        config.write(configfile)


def read_config():
    base_config_path = 'config.ini'
    if not os.path.exists(base_config_path):
        initialize_config_defaults()
    config.read('config.ini')
    return config
        