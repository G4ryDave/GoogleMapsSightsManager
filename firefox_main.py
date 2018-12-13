import sys
import time
import savePlace

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions




def main():
    counter = 0
    time_average = []
    exception_found = []

    print("Type the Id e psw the Google account to whome transfer the favorites")
    string_username = input("ID: ")
    string_password = input("Password: ")
    filepath = savePlace.select_google_bookmarks()
    sights_list = savePlace.parse_place_url(filepath)
    number_of_sights = len(sights_list)

    print("NUMBER OF ATTRACTIONS FOUND: {}".format(number_of_sights))
    print("ETA: {} seconds".format(number_of_sights * 4.5 + 17))  # 17 seconds is the average time to login the first time
    print(
        "Time estimated based on average time without considering exceptions, every exceptions require at least 20 seconds.")
    time.sleep(0.2)
    main_time = time.time()
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options)
    # options.add_argument("--headless")
    print("Firefox Headless Browser Invoked")

    for sight in sights_list:
        start_time = time.time()
        savePlace.visit_sight_url(driver, sight)
        if sight == sights_list[0]:
            try:
                savePlace.login(driver, string_username, string_password)
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
        time_average.append(time_passed)
        # print ("{} seconds ---".format(time_passed))
        # print ("{}/{}".format(counter,number_of_sights))
        savePlace.progbar(counter, number_of_sights, 30)
        sys.stdout.flush()

    total_time = time.time() - main_time
    print("\nTOTAL TIME: {} seconds".format(round(total_time, 2)))
    print("Total Exception found: {} ".format(len(exception_found)))
    for exception in exception_found:
        print(exception)

    driver.quit()

if __name__ == "__main__":
    main()