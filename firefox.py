import getpass
import os
import sys
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.firefox.options import Options as FirefoxOptions

import savePlace


def main():
    print("Requested information about the Google Account where you want to import the starred places:")
    string_username = input("Input ID: ")
    string_password = getpass.getpass("Input Password: ")
    counter = 0
    time_total = 0
    exception_found = []

    filepath = savePlace.select_google_bookmarks()
    sights_list = savePlace.parse_place_url(filepath)
    number_of_sights = len(sights_list)
    print("NUMBER OF SIGHTS FOUND: {}".format(number_of_sights))
    print("If you are using 2 factor authentication, you CAN'T use the background feature!")
    time.sleep(0.2)
    main_time = time.time()

    options = FirefoxOptions()
    options.add_argument("--headless")

    webdriver_path = os.path.dirname(os.path.abspath(__file__))
    try:
        driver = webdriver.Firefox(options=options, executable_path=webdriver_path + r"/assets/geckodriver")
        print("Firefox Headless Browser Invoked")
    except:
        print(
            "Download geckodriver, follow the instructions on github: https://github.com/G4ryDave/GoogleMapsSightsManager")
        exit('File Not Found: geckodriver not found in "assets" folder')

    driver.get("https://www.google.com/maps/?hl=en")
    try:
        savePlace.login(driver, string_username, string_password)
        print("STATE: Successfully Logged")

    except:
        print("WARNING: Something wrong in the Login procedure, check ID and Password ")
        exit("Unable to Login")

    for sight in sights_list:
        start_time = time.time()  # TIME FOR THE SINGLE SIGHT
        driver.get(sight)  # Open google page of the sight in english

        savePlace.favorite_sight(driver)

        counter = counter + 1
        time_passed = time.time() - start_time
        time_total = time_total + time_passed
        time_eta = round(time_total / counter * (number_of_sights - counter), 2)
        # print("ETA {}: {} seconds pass , average {}".format(counter,round(time_passed,3),round(time_total/counter),3))
        savePlace.progbar(counter, number_of_sights, 30, time_eta)
        sys.stdout.flush()

    time_since_start = time.time() - main_time
    print("\nTOTAL TIME: {} seconds".format(round(time_since_start, 2)))
    print("Sights already starred: {}".format(savePlace.get_sights_alrd_starred()))
    print("Total Exception found: {} ".format(len(exception_found)))
    for exception in exception_found:
        print(exception)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nCATCH INTERRUPTION from the User. Program Ended')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    except NoSuchWindowException:
        print("Browser Closed")
