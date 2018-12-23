import os
import sys
import time

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

import savePlace


def main():
    print("Google Account where you want to import the starred places:")
    string_username = input("ID: ")
    string_password = input("Password: ")
    counter = 0
    time_total = 0
    time_login = 0
    exception_found = []

    filepath = savePlace.select_google_bookmarks()
    print(filepath)
    sights_list = savePlace.parse_place_url(filepath)
    number_of_sights = len(sights_list)
    print("NUMBER OF SIGHTS FOUND: {}".format(number_of_sights))
    print(
        "Time estimated based on average time without considering exceptions, every exceptions require at least 20 seconds.")
    time.sleep(0.2)
    main_time = time.time()
    chrome_options = webdriver.ChromeOptions()
    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['acceptSslCerts'] = True
    capabilities['acceptInsecureCerts'] = True
    chrome_options.add_argument("--window-size=1024, 768")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    # chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--headless");
    webdriver_path = os.path.dirname(os.path.abspath(__file__))
    try:
        driver = webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=capabilities,
                                  executable_path=webdriver_path + r"/assets/chromedriver")
        print("Chrome cannot be minimize but doesn't require to be the active window. Use Firefox for background.")
    except:
        print(
            "Download WebDriver, follow the instructions on github: https://github.com/G4ryDave/GoogleMapsSightsManager")
        exit('File Not Found: Webdriver not found in "assets" folder')

    for sight in sights_list:
        start_time = time.time()
        savePlace.visit_sight_url(driver, sight)
        if sight == sights_list[0]:
            try:
                savePlace.login(driver, string_username, string_password)
                start_time = time.time()
                time.sleep(5)
                savePlace.favorite_sight(driver)
            except:
                print("WARNING: Something wrong in the Login procedure, check ID and Password ")
                exit("Unable to Login")
        else:
            try:
                savePlace.favorite_sight(driver)
            except:
                print("WARNING: Time Exception catch!")
                print("Unable to process: {}".format(sight))
                exception_found.append(sight)
        counter = counter + 1
        time_passed = time.time() - start_time
        time_total = time_total + time_passed
        time_eta = round(time_total / counter * (number_of_sights - counter), 2)
        # print("ETA {}: {} seconds pass , average {}".format(counter,round(time_passed,3),round(time_total/counter),3))
        savePlace.progbar(counter, number_of_sights, 30, time_eta)
        sys.stdout.flush()

    time_since_start = time.time() - main_time
    print("\nTOTAL TIME: {} seconds".format(round(time_since_start, 2)))
    print("Total Exception found: {} ".format(len(exception_found)))
    for exception in exception_found:
        print(exception)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nCATCH INTERRUPTION from the user. Program Ended')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
