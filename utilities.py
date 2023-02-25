"""This python will handle some extra functions."""
import sys
from os.path import exists

import yaml
from yaml import SafeLoader


def config_file_generator():
    """Generate the template of config file"""
    with open('config.yml', 'w', encoding="utf8") as f:
        f.write("""# ++--------------------------------++
# | Blur-AutoBid                     |
# | Made by LD (MIT License)         |
# ++--------------------------------++


"""
                )
    sys.exit()


def read_config():
    """Read config file.

    Check if config file exists, if not, create one.
    if exists, read config file and return config with dict type.

    :rtype: dict
    """
    if not exists('./config.yml'):
        print("Config file not found, create one by default.\nPlease finish filling config.yml")
        with open('config.yml', 'w', encoding="utf8"):
            config_file_generator()

    try:
        with open('config.yml', 'r', encoding="utf8") as f:
            data = yaml.load(f, Loader=SafeLoader)
            security_phrases = separate_spaces(data['security_phrase'])
            followed_collections = data['Followed']
            for i in range(len(followed_collections)):
                current = followed_collections[i]
                current['bid_url'] = get_bid_url(current['collection_name'])
            config = {
                'security_phrases': security_phrases,
                'followed_collections': followed_collections,
            }
            return config
    except (KeyError, TypeError):
        print(
            "An error occurred while reading config.yml, please check if the file is corrected filled.\n"
            "If the problem can't be solved, consider delete config.yml and restart the program.\n")
        sys.exit()


def separate_spaces(input_string):
    """Separate spaces inside a string.

    :rtype: list
    """
    result = input_string.split(" ")
    return result


def get_bid_url(collection_name):
    """Get bid url from config file.

    :rtype: list
    """
    bid_url = f'https://blur.io/collection/{collection_name}/bids'
    return bid_url
