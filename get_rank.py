from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException

import time
import sys
import os
import re

def get_rank(team_name="22222222222222222222222222222222"):
    print("Calling get_rank()...")
    # sets up selenium driver with correct Chrome headless version
    os.environ['WDM_LOG_LEVEL'] = '0'  # suppress logs from ChromeDriverManager install
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager(version="96.0.4664.45").install(), options=options)
    url = "https://berkeley-cs170.github.io/project-leaderboard-fa21/?team={}".format(team_name)

    driver.get(url)
    # time.sleep(8)

    i = 1
    rank_dict = {}
    while True:
        try:
            name_selector = "//*[@id=\"table\"]/table/tr[{}]/td[1]/span/a".format(i)
            name = driver.find_element_by_xpath(name_selector).text
            rank_selector = "//*[@id=\"table\"]/table/tr[{}]/td[2]".format(i)
            rank = driver.find_element_by_xpath(rank_selector).text
            rank_dict[name] = int(rank)
            i += 1
            if i % 100 == 0:
                print("progress: {} / 899".format(i))

        except NoSuchElementException:
            if i == 1:
                pass
            else:
                break

    not_first = [item[0] for item in rank_dict.items() if item[1] != 1]
    more_than_ten = [item[0] for item in rank_dict.items() if item[1] > 10]
    more_than_twenty = [item[0] for item in rank_dict.items() if item[1] > 20]

    try:
        driver.close()
    except InvalidSessionIdException:
        pass

    return rank_dict, not_first, more_than_ten, more_than_twenty

if __name__ == '__main__':
    rank_dict, not_first, more_than_ten, more_than_twenty = get_rank()
    print("\n=========================================================\n")
    print("rank dict:\n", rank_dict)
    print("\n=========================================================\n")
    print("not first:\n", not_first)
    print("\n=========================================================\n")
    print("more than 10:\n", more_than_ten)
    print("\n=========================================================\n")
    print("more than 20:\n", more_than_twenty)
