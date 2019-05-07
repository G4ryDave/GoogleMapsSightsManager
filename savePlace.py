import time
import tkinter
from tkinter import filedialog

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

language_save = ["Salva", "Save", "Guardar", "Speichern", "Enregistrer", "Opslaan"]
language_saved = ["Salvato", "Saved", "Guardado", "Gespeichert", "Enregistré", "Opgeslagen"]
sights_alrd_starred = 0


# gui for selection of Bookmarks file with Sights to import.
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
        exit("Select a correct file")


# parse the html inside the bookmarks Google. Aka lists of all sights to import
def parse_place_url(bookmarks_path):
    f = open(bookmarks_path)
    soup = BeautifulSoup(f, "html.parser")
    f.close()
    list_sights = []
    links = soup.findAll("a")
    for link in links:
        url_sight = link.get('href')
        name_sight = link.text  # the name of the attraction
        list_sights.append(url_sight)  # direct url to the attraction
    return list_sights


def progbar(current_value, total, len_progress_bar, eta):
    fraction = current_value / total
    filled_progbar = round(fraction * len_progress_bar)
    print('\r', '#' * filled_progbar + '-' * (len_progress_bar - filled_progbar),
          '[{}/{} {:.2%} - ETA: {}s]'.format(current_value, total, fraction, eta))
    print("")


def login(driver, string_username, string_password):
    elem = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.LINK_TEXT, "Sign in")))
    elem.click()
    signup = driver.find_element_by_id("identifierId")
    signup.send_keys(string_username)
    signup.send_keys(Keys.ENTER)

    time.sleep(3)  # implicit wait

    password = driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[1]/div/form/content/section/div/content/div[1]/div/div[1]/div/div[1]/input")
    password.send_keys(string_password)
    password.send_keys(Keys.ENTER)
    try:
        country_list_phonenumber = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "countryList")))
        print("TWO FACTOR AUTHENTICATION. Proceed with the autentication in the next 3 minutes")
        satellite_button = WebDriverWait(driver, 180).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "/html/body/jsl/div[3]/div[7]/div[24]/div[3]/div/div[2]/button")))  # trigger that enable the star button
    except:
        try:
            password_box_presence = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH,
                                                                                               "/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[1]/div/form/content/section/div/content/div[1]/div/div[1]/div/div[1]/input")))
            exit("Impossible to complete the Login: Check ID or Password")
        except:
            try:
                id_box_presence = WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.ID, "identifierId")))
                exit("Impossible to complete the Login: Check ID or Password")

            except:
                pass


'''Initial introduction of bookmarks actions:
1 = Favorites
2 = Want to go
3 = starred Place

'''


def favorite_sight(driver, bookmarks_action=3):
    trigger_satellite_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "/html/body/jsl/div[3]/div[7]/div[24]/div[3]/div/div[2]/button")))  # trigger:  page fully loaded

    # check if the sight is already starred
    save_sight_button = driver.find_elements_by_css_selector("[data-value]")
    if save_sight_button[2].text in language_save:
        save_sight_button[2].click()
        time.sleep(0.15)
        bookmarks_options = driver.find_elements_by_class_name("action-menu-entry-text")
        bookmarks_options[bookmarks_action].click()
    elif save_sight_button[2].text in language_saved:
        set_sights_alrd_starred()
    time.sleep(0.1)


def get_sights_alrd_starred():
    return str(sights_alrd_starred)


def set_sights_alrd_starred():
    global sights_alrd_starred
    sights_alrd_starred = sights_alrd_starred + 1
