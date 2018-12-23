import time
import tkinter
from tkinter import filedialog

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def select_google_bookmarks():
    root = tkinter.Tk()
    root.withdraw()
    root.update()
    root.filename = tkinter.filedialog.askopenfilename(initialdir="/Downloads", title="Select BookmarksGoogle.html",
                                                       filetypes=(("html files", "*.html"), ("all files", "*.*")))
    root.update()
    root.destroy()
    if root.filename.endswith('.html'):
        return root.filename
    else:
        print("Select a correct file")


def parse_place_url(bookmarks_path):
    f = open(bookmarks_path)  # simplified for the example (no urllib)
    soup = BeautifulSoup(f, "lxml")
    f.close()
    list_sights = []
    links = soup.findAll("a")
    for link in links:
        url_sight = link.get('href')
        name_sight = link.text  # the name of the attraction
        list_sights.append(url_sight)  # direct url to the attraction
        # print (name_sight)
    return list_sights


def progbar(current_value, total, len_progress_bar, eta):
    fraction = current_value / total
    filled_progbar = round(fraction * len_progress_bar)
    print('\r', '#' * filled_progbar + '-' * (len_progress_bar - filled_progbar),
          '[{:.2%} ETA: {}s]'.format(fraction, eta))
    print("")


def login(driver, string_username, string_password):
    satellite_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "/html/body/jsl/div[3]/div[7]/div[26]/div[3]/div/div[2]/button")))
    button = driver.find_element_by_class_name('section-action-popup-container')
    button.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "widget-signin-promo")))
    button_sign_in = driver.find_element_by_xpath(
        '/html/body/jsl/div[3]/div[7]/div[9]/div/div[1]/div/div/div[2]/div[1]/div[1]/div/div/button')
    button_sign_in.click()
    driver.implicitly_wait(2)
    # open Google login page
    print("LOGIN..")
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/content/span")))
    username = driver.find_element_by_id('identifierId')
    username.send_keys(string_username)
    next_button = driver.find_element_by_id('identifierNext')
    next_button.click()
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH,
                                                                    "/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[1]/div/form/content/section/div/content/div[1]/div/div[1]/div/div[1]/input")))
    time.sleep(1.5)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/content/span")))
    password = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.NAME, "password")))
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/content/span")))  # trigger that enable the star button
    password.send_keys(string_password)
    time.sleep(2.5)
    signin_button = driver.find_element_by_xpath(
        '/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/content/span')
    signin_button.click()


def visit_sight_url(driver, url):
    driver.get(url)


def favorite_sight(driver):
    satellite_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "/html/body/jsl/div[3]/div[7]/div[26]/div[3]/div/div[2]/button")))  # trigger that enable the star button
    save_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "/html/body/jsl/div[3]/div[7]/div[9]/div/div[1]/div/div/div[2]/div[1]/div[1]/button/jsl/div")))
    save_button.click()
    star_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "/html/body/jsl/div[3]/div[4]/div[1]/div[4]/div[2]")))
    star_button.click()

    time.sleep(0.5)
