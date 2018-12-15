# GoogleMapsSightsManager
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/) [![built with Selenium](https://img.shields.io/badge/built%20with-Selenium-yellow.svg)](https://github.com/SeleniumHQ/selenium) [![built with Python3](https://img.shields.io/badge/built%20with-Python3-red.svg)](https://www.python.org/)  
![macOS](https://img.shields.io/badge/macOS-pass-brightgreen.svg) ![macOS](https://img.shields.io/badge/Ubuntu-pass-brightgreen.svg)


GoogleMapsSightsManager is a tool that automize the transfer of starred places from a Google Account to another. In the same way it is possible to delete all your starred places from your Google account.
Currently tested on MacOS and Ubuntu 16.04.


### Installation

```bash
1. git clone https://github.com/G4ryDave/GoogleMapsSightsManager.git
2. cd GoogleMapsSightsManager/
3. pip install -r requirements.txt
4a. python firefox_main.py
or
4b. python chrome.py
```

### Procedure
Choose one of the browser below:
##### - Firefox (Recommended)  [Background supported]
  Download ```geckodriver``` for your system [from here](https://github.com/mozilla/geckodriver/releases). Extract the .tar.gz file and put it in ```/assets``` folder
##### - Chrome (Doesn't work in background)
 Download ```chromedriver``` for your system [from here](https://sites.google.com/a/chromium.org/chromedriver/downloads). Extract the .zip file and put it in ```/assets``` folder
 
1. Go to ```https://www.google.com/bookmarks``` and login with the Google account that contains the starred places to transfer.
2. On the left side of the page press ```Export Bookmarks```. (Should download "GoogleBookmarks.html" in your download folder).
3. Start the programm and type ID & Password of your Google account, that should import the starred places, on request.
4. Select ```GoogleBookmarks.html``` in the next window.

 
 
## Why I have to put ID & Psw??
No one should have to share this sensible informations but they are required to login the browser.Infact, while in test mode, every account is logged out by default. Due to this constraint we need the Google Account ID & Password.**As you can see from the source code this credentials are not stored!** .

### To Do

  - Dynamic ETA
  - Handle Two-factor authentication
  - Change requirements.txt
  - Create GUI

License
----

MIT
