# utils/util_selenium.py
from selenium import webdriver
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from time import sleep
from .util import setup_logger, does_it_exist
import pandas as pd



def get_soup(url_):
    logger = setup_logger()
    options = Options()
    options.add_argument('--headless')
    ua = UserAgent()
    user_agent = ua.random
    # logger.info(f"{user_agent}")
    options.add_argument(f'user-agent:{user_agent}')
    with webdriver.Firefox(service=Service('/Users/geckodriver'), options=options) as driver:
        driver.get(url_)
        sleep(2)
        driver.maximize_window()
        driver.save_screenshot("data/homepage.png")
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        return soup
    
def save_soup(soup, filename):
    with open(f'{filename}', 'w') as f:
        f.write(str(soup))

def retreive_soup(filename):
    with open(filename, 'r') as f:
        text = f.read()
        return BeautifulSoup(text, 'html.parser')

def obtain_soup(url: str, filename: str):
    logger = setup_logger()
    
    if does_it_exist(filename):
        soup = retreive_soup(filename=filename)
        logger.info("Used the file")
    else:
        logger.info("Used selenium")
        soup = get_soup(url)
        save_soup(str(soup), filename)
    return soup


if __name__ == '__main__':
    print("You have run the wrong file")
