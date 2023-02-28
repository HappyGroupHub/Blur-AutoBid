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
# | Made by LD                       |
# ++--------------------------------++

security_phrase: ''

# Bid Collection
# Copy collection_name from url, e.g. https://blur.io/collection/>>beanzofficial<<
# Follow as many collections as you want, below are examples.
Followed:
  - collection: 'beanzofficial'
    bid_amount_left_to_stop: 500
    contract_address: '0x306b1ea3ecdf94ab739f1910bbda052ed4a9f949'

  - collection: 'murakami-flowers-2022-official'
    bid_amount_left_to_stop: 100
    contract_address: '0x7d8820fa92eb1584636f4f5b8515b5476b75171a'
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
                current_collection = followed_collections[i]
                current_collection['bid_url'] = get_bid_url(current_collection['collection'])
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


def get_bid_url(collection):
    """Get bid url from config file.

    :rtype: list
    """
    bid_url = f'https://blur.io/collection/{collection}/bids'
    return bid_url
