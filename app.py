"""This is the main python file of the project."""
import math
import time
from datetime import datetime

from selenium import webdriver
from selenium.common import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

import utilities as utils

config = utils.read_config()
bid_placed = dict()
is_bid_placed = dict()

options = webdriver.ChromeOptions()
options.add_extension('metamask.crx')
driver = webdriver.Chrome(options=options)
driver.maximize_window()


def driver_send_keys(locator, key):
    """Send keys to element.

    :param locator: Locator of element.
    :param key: Keys to send.
    """
    WebDriverWait(driver, 5).until(ec.presence_of_element_located(locator)).send_keys(key)


def driver_click(locator):
    """Click element.

    :param locator: Locator of element.
    """
    WebDriverWait(driver, 5).until(ec.presence_of_element_located(locator)).click()


def driver_get_text(locator):
    """Get text of element.

    :param locator: Locator of element.
    :return: Text of element.
    """
    return WebDriverWait(driver, 5).until(ec.presence_of_element_located(locator)).text


def driver_clear_input(locator):
    """Clear input of element.

    :param locator: Locator of element.
    """
    WebDriverWait(driver, 5).until(ec.presence_of_element_located(locator)).clear()


def setup_metamask():
    driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
    driver.switch_to.window(driver.window_handles[0])
    driver_click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/ul/li[2]/button'))
    driver_click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div/button[1]'))

    # check security phrase length
    if len(config.get('security_phrases')) == 15:
        driver_click((By.XPATH,
                      '//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/div/div[2]/select/option[2]'))
    if len(config.get('security_phrases')) == 18:
        driver_click((By.XPATH,
                      '//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/div/div[2]/select/option[3]'))
    if len(config.get('security_phrases')) == 21:
        driver_click((By.XPATH,
                      '//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/div/div[2]/select/option[4]'))
    if len(config.get('security_phrases')) == 24:
        driver_click((By.XPATH,
                      '//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/div/div[2]/select/option[5]'))

    # enter security phrases
    for i in range(len(config.get('security_phrases'))):
        driver_send_keys((By.XPATH, f'//*[@id="import-srp__srp-word-{i}"]'),
                         config.get('security_phrases')[i])
    driver_click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/button'))
    time.sleep(2)

    password = utils.key_generator()
    driver_send_keys(
        (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[1]/label/input'),
        password)
    driver_send_keys(
        (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[2]/label/input'),
        password)
    driver_click(
        (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[3]/label/input'))
    driver_click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/button'))
    time.sleep(2)
    driver_click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'))
    time.sleep(1)
    driver_click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'))
    driver_click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'))

    # check if user has entered private key
    if not config.get('private_key') == '':
        time.sleep(3)
        driver_click((By.XPATH, '//*[@id="app-content"]/div/div[1]/div/div[2]/button'))
        driver_click((By.XPATH, '//*[@id="app-content"]/div/div[3]/button[2]'))
        driver_send_keys((By.XPATH, '//*[@id="private-key-box"]'), config.get('private_key'))
        driver_click(
            (By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/div[2]/div[2]/div[2]/button[2]'))
        time.sleep(3)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print('Metamask setup successfully.')


def login_blur():
    driver.get('https://blur.io/')
    driver_click((By.XPATH, '//*[@id="__next"]/div/header/div/div[3]/button'))
    driver_click((By.ID, 'METAMASK'))
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[1])
    driver_click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[3]/div[2]/button[2]'))
    driver_click(
        (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]'))

    # try sign in with metamask
    try:
        WebDriverWait(driver, 1).until(ec.presence_of_element_located(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[3]/button[2]')))
        driver_click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[3]/button[2]'))
    except TimeoutException:
        pass

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print('Blur login successfully.')


def init_blur():
    driver.get('https://blur.io/portfolio')

    # try sign in with metamask
    try:
        WebDriverWait(driver, 1).until(ec.presence_of_element_located(
            (By.XPATH, '//*[@id="__next"]/div/main/div/button')))
        driver_click((By.XPATH, '//*[@id="__next"]/div/main/div/button'))
        driver_click((By.ID, 'METAMASK'))
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        driver_click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[3]/button[2]'))
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except (TimeoutException, ElementClickInterceptedException):
        pass

    time.sleep(3)

    # try init blur show mode
    try:
        WebDriverWait(driver, 1).until(ec.presence_of_element_located(
            (By.XPATH, '/html/body/div[3]/form/button')))
        driver_click((By.XPATH, '/html/body/div[3]/form/button'))
    except TimeoutException:
        pass

    # try pass through bid tutorial
    try:
        driver_click((By.XPATH, '//*[@id="__next"]/div/header/div[3]/div[2]/button'))
        WebDriverWait(driver, 1).until(ec.presence_of_element_located(
            (By.XPATH, '/html/body/div[2]/div/div/div[2]/div[2]/button')))
        driver_click((By.XPATH, '/html/body/div[2]/div/div/div[2]/div[2]/button'))
        driver_click((By.XPATH, '/html/body/div[2]/div/div/div[2]/div[2]/button'))
        driver_click((By.XPATH, '/html/body/div[2]/div/div/div[2]/div[2]/button'))
        driver_click((By.XPATH, '/html/body/div[2]/div/div/div[2]/div[2]/button'))
        driver_click((By.XPATH, '/html/body/div[2]/div/div/div[2]/div[2]/button'))
    except (TimeoutException, ElementClickInterceptedException):
        pass

    print('Blur initialize successfully.')


def place_init_bids():
    while True:
        try:
            print('Start placing initial bids.')
            print('-----------------------------------------------------\n')
            collections = config.get('followed_collections')
            for current_collection in range(len(collections)):
                time.sleep(config.get('check_interval'))
                current_collection = collections[current_collection]
                driver.get(current_collection.get('bid_url'))
                bid_amount_left_to_stop = current_collection.get('bid_amount_left_to_stop')
                total_bid_left = driver_get_text((By.XPATH,
                                                  '/html/body/div/div/main/div/div[3]/div/div[2]/div/div[2]/div/div/div[1]/div[3]/div[1]'))
                total_bid_left = float(total_bid_left)
                bid_sort_num = 1
                while True:
                    if total_bid_left >= bid_amount_left_to_stop:
                        place_bid(str(bid_sort_num), current_collection.get('collection'))
                        break
                    else:
                        bid_sort_num += 1

                        # try to get next bid price, may encounter error if bid price is too far
                        try:
                            next_total = driver_get_text((By.XPATH,
                                                          f'//*[@id="collection-main"]/div[2]/div/div[2]/div/div/div[{bid_sort_num}]/div[3]/div[1]'))
                            total_bid_left += float(next_total)
                        except TimeoutException:
                            print(
                                f'Bid price is too far to place [{current_collection.get("collection")}]')
                            print('Please try lower bid_amount_left_to_stop')
                            bid_placed[current_collection.get('collection')] = 0
                            is_bid_placed[current_collection.get('collection')] = False
                            break

                        continue

            print('Initial bids placed successfully. \n')
            print('Start secure your bidding!')
            print('-----------------------------------------------------')
            break
        except (Exception, IndexError) as error_init_bid:
            print('-----------------------------------------------------')
            print(error_init_bid)
            print('-----------------------------------------------------')
            print('Error occurred while placing initial bids.')
            print('Closing redundant windows now.')
            for init_bid_window in driver.window_handles[1:]:
                driver.switch_to.window(init_bid_window)
                driver.close()
            driver.switch_to.window(driver.window_handles[0])
            print('All redundant windows closed.')
            print('Canceling all bids now.')
            cancel_all_bids()
            bid_placed.clear()
            is_bid_placed.clear()
            print('All bids canceled.')
            print('Now placing initial bids again.')
            continue


def secure_bidding():
    collections = config.get('followed_collections')
    for current_collection in range(len(collections)):
        time.sleep(config.get('check_interval'))
        current_collection = collections[current_collection]
        driver.get(current_collection.get('bid_url'))
        bid_amount_left_to_stop = current_collection.get('bid_amount_left_to_stop')
        total_bid_left = driver_get_text((By.XPATH,
                                          '/html/body/div/div/main/div/div[3]/div/div[2]/div/div[2]/div/div/div[1]/div[3]/div[1]'))
        total_bid_left = float(total_bid_left)
        collection_name = driver_get_text((By.XPATH, '//*[@id="OVERLINE"]/div/div[1]/div[2]/div'))
        bid_sort_num = 1
        while True:
            if total_bid_left >= bid_amount_left_to_stop:
                bid_price = driver_get_text((By.XPATH,
                                             f'/html/body/div/div/main/div/div[3]/div/div[2]/div/div[2]/div/div/div[{bid_sort_num}]/div[1]/div/div[2]/div[1]'))
                bid_price = float(bid_price)
                previous_bid_price = bid_placed.get(
                    current_collection.get('collection'))
                current_time = datetime.now().strftime('[%m/%d %H:%M:%S]')
                if not bid_price == previous_bid_price:
                    if not previous_bid_price == 0:
                        print('-----------------------------------------------------')
                        print(f'{current_time} Bid price changed!')
                        print(f'Previous bid price on {collection_name} is {previous_bid_price}')
                        print(f'New bid price on {collection_name} is {bid_price}')
                        print('-----------------------------------------------------')
                        if is_bid_placed.get(current_collection.get('collection')):

                            # try to cancel bid, may encounter error if you bid that NFT successfully
                            try:
                                cancel_bid(current_collection.get('contract_address'))
                            except TimeoutException:
                                print('Cancel bid failed!')
                                print(f'Your bid on {collection_name} might get accepted')
                                print(f'Please check your wallet activity to confirm')
                                print('Now continue to secure your bidding...\n')
                                bid_placed[current_collection.get('collection')] = 0

                            is_bid_placed[current_collection.get('collection')] = False
                            driver.get(current_collection.get('bid_url'))
                            time.sleep(3)

                    # try to place bid, may encounter error if lagged
                    while True:
                        try:
                            place_bid(str(bid_sort_num),
                                      current_collection.get('collection'))
                            break
                        except (Exception, IndexError):
                            driver.refresh()
                            time.sleep(config.get('check_interval'))
                            continue

                    break
                else:
                    print(f'{current_time} Your bid on {collection_name} is secured!')
                    break
            else:
                bid_sort_num += 1

                # try to get next bid price, may encounter error if bid price is too far
                try:
                    next_total = driver_get_text((By.XPATH,
                                                  f'//*[@id="collection-main"]/div[2]/div/div[2]/div/div/div[{bid_sort_num}]/div[3]/div[1]'))
                    total_bid_left += float(next_total)
                except TimeoutException:
                    print(f'Bid price is too far to place [{current_collection.get("collection")}]')
                    print('Please try lower bid_amount_left_to_stop, canceling its bid now.')

                    # try to cancel bid, may encounter error if you bid that NFT successfully
                    try:
                        cancel_bid(current_collection.get('contract_address'))
                        print('Bid canceled successfully.')
                    except TimeoutException:
                        pass

                    bid_placed[current_collection.get('collection')] = 0
                    is_bid_placed[current_collection.get('collection')] = False
                    break

                continue
    time.sleep(1)
    secure_bidding()


def place_bid(bid_sort_num, collection):
    bid_price = f'/html/body/div/div/main/div/div[3]/div/div[2]/div/div[2]/div/div/div[{bid_sort_num}]/div[1]/div/div[2]/div[1]'
    bid_price = driver_get_text((By.XPATH, bid_price))
    bid_pool_balance = str
    driver_click((By.XPATH, '//*[@id="__next"]/div/header/div[3]/div[2]/button'))

    # Trying to get bid pool balance, xpath may change if bid is placed or canceled
    while True:
        try:
            bid_pool_balance = driver_get_text(
                (By.XPATH, '/html/body/div[2]/div/div/div[2]/div[2]/div[2]/div[1]/div[1]'))
            break
        except TimeoutException:
            driver.refresh()
            time.sleep(1)
            driver_click((By.XPATH, '//*[@id="__next"]/div/header/div[3]/div[2]/button'))
            continue

    collection_name = driver_get_text((By.XPATH, '//*[@id="OVERLINE"]/div/div[1]/div[2]/div'))
    current_time = datetime.now().strftime('[%m/%d %H:%M:%S]')
    if float(bid_pool_balance) < float(bid_price):
        if collection not in bid_placed:
            bid_placed[collection] = 0
        print('-----------------------------------------------------')
        print(current_time)
        print(f'Not enough balance to place bid! [{collection_name}]')
        print(f'Current balance: {bid_pool_balance}')
        print(f'Bid price needed: {bid_price}')
        print('-----------------------------------------------------')
    else:
        driver_click((By.XPATH, '//*[@id="__next"]/div/main/div/div[4]/button'))
        time.sleep(0.5)
        driver_send_keys(
            (By.XPATH, '//*[@id="__next"]/div/main/div/div[4]/div/div[2]/div[3]/div[2]/div/input'),
            bid_price)
        bid_pool_balance = float(bid_pool_balance)
        bid_pool_balance = math.floor(bid_pool_balance * 100) / 100.0
        bid_amount = bid_pool_balance / float(bid_price)
        bid_amount = math.floor(bid_amount)
        driver_clear_input(
            (By.XPATH, '//*[@id="__next"]/div/main/div/div[4]/div/div[2]/div[4]/div[2]/div/input'))
        time.sleep(0.1)
        driver_send_keys(
            (By.XPATH, '//*[@id="__next"]/div/main/div/div[4]/div/div[2]/div[4]/div[2]/div/input'),
            bid_amount)
        time.sleep(0.5)
        driver_click((By.XPATH, '//*[@id="__next"]/div/main/div/div[4]/div/div[3]/div/button[2]'))
        sign_transaction()
        collection_name = driver_get_text((By.XPATH, '//*[@id="OVERLINE"]/div/div[1]/div[2]/div'))
        bid_placed[collection] = float(bid_price)
        is_bid_placed[collection] = True
        print(f'Bid placed success! [{collection_name}]')
        print(
            f'Placed with: {bid_price} x {bid_amount} = {float(bid_price) * bid_amount}ETH')
        print('-----------------------------------------------------')


def cancel_bid(contract_address):
    driver.get(f'https://blur.io/portfolio/bids?contractAddress={contract_address}')
    time.sleep(1)
    driver_click((By.XPATH,
                  '/html/body/div/div/main/div/div[4]/div/div[2]/div/div[2]/div/div/a/div[7]/div/button'))
    time.sleep(3)


def cancel_all_bids():
    collections = config.get('followed_collections')
    for current_collection in range(len(collections)):
        time.sleep(config.get('check_interval'))
        current_collection = collections[current_collection]
        driver.get(
            f'https://blur.io/portfolio/bids?contractAddress={current_collection.get("contract_address")}')
        time.sleep(1)

        # Try to cancel bid, if no bid is placed, pass
        try:
            driver_click((By.XPATH,
                          '/html/body/div/div/main/div/div[4]/div/div[2]/div/div[2]/div/div/a/div[7]/div/button'))
        except TimeoutException:
            pass

        time.sleep(3)


def sign_transaction():
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[1])
    try:
        WebDriverWait(driver, 1).until(ec.presence_of_element_located(
            (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[3]/div[1]')))
        driver_click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[3]/div[1]'))
    except TimeoutException:
        pass
    driver_click((By.XPATH, '/html/body/div[1]/div/div[2]/div/div[4]/button[2]'))
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)


if __name__ == '__main__':
    setup_metamask()
    login_blur()
    init_blur()
    place_init_bids()

    # Secure bidding
    while True:
        try:
            secure_bidding()
        except (Exception, IndexError) as error:
            print('-----------------------------------------------------')
            print(error)
            print('-----------------------------------------------------')
            print('Error occurred. Restarting the whole process...')
            print('Closing redundant windows now.')
            for window in driver.window_handles[1:]:
                driver.switch_to.window(window)
                driver.close()
            driver.switch_to.window(driver.window_handles[0])
            print('All redundant windows closed.')
            print('Canceling all bids now.')
            cancel_all_bids()
            bid_placed.clear()
            is_bid_placed.clear()
            print('All bids canceled.')
            print('Now placing initial bids again.')
            place_init_bids()
            continue
