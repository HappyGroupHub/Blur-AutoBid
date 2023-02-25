"""This python file will do the AutoClass job."""
import math
import time

from selenium import webdriver
from selenium.common import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

import utilities as utils

config = utils.read_config()

options = webdriver.ChromeOptions()
options.add_extension('metamask.crx')
driver = webdriver.Chrome(options=options)
driver.maximize_window()


def driver_send_keys(locator, key):
    """Send keys to element.

    :param locator: Locator of element.
    :param key: Keys to send.
    """
    WebDriverWait(driver, 100).until(ec.presence_of_element_located(locator)).send_keys(key)


def driver_click(locator):
    """Click element.

    :param locator: Locator of element.
    """
    WebDriverWait(driver, 100).until(ec.presence_of_element_located(locator)).click()


def driver_get_text(locator):
    """Get text of element.

    :param locator: Locator of element.
    :return: Text of element.
    """
    return WebDriverWait(driver, 100).until(ec.presence_of_element_located(locator)).text


def driver_clear_input(locator):
    """Clear input of element.

    :param locator: Locator of element.
    """
    WebDriverWait(driver, 100).until(ec.presence_of_element_located(locator)).clear()


def setup_metamask():
    driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
    driver.switch_to.window(driver.window_handles[0])
    driver_click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/ul/li[2]/button'))
    driver_click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div/button[1]'))
    for i in range(12):
        driver_send_keys((By.XPATH, f'//*[@id="import-srp__srp-word-{i}"]'),
                         config.get('security_phrases')[i])
    driver_click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/button'))
    time.sleep(2)
    driver_send_keys(
        (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[1]/label/input'),
        '12345678')
    driver_send_keys(
        (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[2]/label/input'),
        '12345678')
    driver_click(
        (By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[3]/label/input'))
    driver_click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/button'))
    time.sleep(2)
    driver_click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'))
    time.sleep(1)
    driver_click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'))
    driver_click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'))
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print('Metamask setup successfully.')
    login_blur()


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
    init_blur()


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
    place_init_bids()


def place_init_bids():
    print('Start placing initial bids. \n')
    print('-----------------------------------------------------')
    collections = config.get('followed_collections')
    for current_collection in range(len(collections)):
        driver.get(collections[current_collection].get('bid_url'))
        bid_amount_left_to_stop = collections[current_collection].get('bid_amount_left_to_stop')
        total_bid_left = driver_get_text((By.XPATH,
                                          '/html/body/div/div/main/div/div[3]/div/div[2]/div/div[2]/div/div/div[1]/div[3]/div[1]'))
        total_bid_left = float(total_bid_left)
        bid_sort_num = 1
        while True:
            if total_bid_left >= bid_amount_left_to_stop:
                place_bid(str(bid_sort_num))
                break
            else:
                sum_next_total = driver_get_text((By.XPATH,
                                                  f'/html/body/div/div/main/div/div[3]/div/div[2]/div/div[2]/div/div/div[{bid_sort_num}]/div[3]/div[1]'))
                total_bid_left += float(sum_next_total)
                bid_sort_num += 1
                continue
    print('Initial bids placed successfully.')
    time.sleep(1000)
    secure_bidding()


def place_bid(bid_sort_num):
    bid_price = f'/html/body/div/div/main/div/div[3]/div/div[2]/div/div[2]/div/div/div[{bid_sort_num}]/div[1]/div/div[2]/div[1]'
    bid_price = driver_get_text((By.XPATH, bid_price))
    driver_click((By.XPATH, '//*[@id="__next"]/div/header/div[3]/div[2]/button'))
    bid_pool_balance = driver_get_text(
        (By.XPATH, '/html/body/div[2]/div/div/div[2]/div[2]/div[2]/div[1]/div[1]'))
    collection_name = driver_get_text((By.XPATH, '//*[@id="OVERLINE"]/div/div[1]/div[2]/div'))
    if float(bid_pool_balance) < float(bid_price):
        print(f'Not enough balance to place bid! [{collection_name}]')
        print(f'Current balance: {bid_pool_balance}')
        print(f'Bid price needed: {bid_price}')
        print('-----------------------------------------------------')
    else:
        driver_click((By.XPATH, '//*[@id="__next"]/div/main/div/div[4]/button'))
        driver_send_keys(
            (By.XPATH, '//*[@id="__next"]/div/main/div/div[4]/div/div[2]/div[3]/div[2]/div/input'),
            bid_price)
        bid_amount = float(bid_pool_balance) / float(bid_price)
        bid_amount = math.floor(bid_amount)
        driver_clear_input(
            (By.XPATH, '//*[@id="__next"]/div/main/div/div[4]/div/div[2]/div[4]/div[2]/div/input'))
        driver_send_keys(
            (By.XPATH, '//*[@id="__next"]/div/main/div/div[4]/div/div[2]/div[4]/div[2]/div/input'),
            bid_amount)
        driver_click((By.XPATH, '//*[@id="__next"]/div/main/div/div[4]/div/div[3]/div/button[2]'))
        sign_transaction()
        collection_name = driver_get_text((By.XPATH, '//*[@id="OVERLINE"]/div/div[1]/div[2]/div'))
        print(f'Initial bid success! [{collection_name}]')
        print(
            f'Placed with bid price: {bid_price} x {bid_amount} = {float(bid_price) * bid_amount}ETH')
        print('-----------------------------------------------------')


def sign_transaction():
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[1])
    driver_click((By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[4]/button[2]'))
    driver.switch_to.window(driver.window_handles[0])


def secure_bidding():
    bid_urls = config.get('bid_urls')
    for bid_url in bid_urls:
        driver.get(bid_url)


if __name__ == '__main__':
    setup_metamask()
    time.sleep(10000)
