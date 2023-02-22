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
            security_phrases = get_security_phrases(data['security_phrase'])
            bid_urls = get_bid_url(data['bid_collections'])
            config = {
                'security_phrases': security_phrases,
                'bid_urls': bid_urls
            }
            return config
    except (KeyError, TypeError):
        print(
            "An error occurred while reading config.yml, please check if the file is corrected filled.\n"
            "If the problem can't be solved, consider delete config.yml and restart the program.\n")
        sys.exit()


def get_security_phrases(security_phrase):
    """Read class_id from config file.

    :rtype: list
    """
    security_phrases = security_phrase.split(" ")
    return security_phrases


def get_bid_url(bid_collections):
    """Get bid url from config file.

    :rtype: list
    """
    bid_urls = bid_collections.split(" ")
    for i in range(len(bid_urls)):
        bid_urls[i] = f'https://blur.io/collection/{bid_urls[i]}/bids'
    return bid_urls
