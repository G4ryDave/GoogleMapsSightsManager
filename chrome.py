import sys
import time
import savePlace

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


string_username = 'caneferoce2'
string_password = 'alcibiad3'
counter = 0
time_average = []
exception_found = []

filepath = savePlace.select_google_bookmarks()
sights_list = savePlace.parse_place_url(filepath)
number_of_sights = len(sights_list)

print("NUMBER OF ATTRACTIONS FOUND: {}".format(number_of_sights))
print("ETA: {} seconds".format(number_of_sights * 4.5 + 17))  # 17 seconds is the average time to login the first time
print(
    "Time estimated based on average time without considering exceptions, every exceptions require at least 20 seconds.")
time.sleep(0.2)

main_time = time.time()
chrome_options = webdriver.ChromeOptions()
capabilities = DesiredCapabilities.CHROME.copy()
capabilities['acceptSslCerts'] = True
capabilities['acceptInsecureCerts'] = True
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
# chrome_options.experimental_options("useAutomationExtension")
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--headless");
driver = webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=capabilities)

for sight in sights_list:
    print("going wild")
    start_time = time.time()
    savePlace.visit_sight_url(driver, sight)
    if sight == sights_list[0]:
        try:
            savePlace.login(driver, string_username, string_password)
            time.sleep(5)
            savePlace.favorite_sight(driver)
            print("Succesfully Logged")
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
