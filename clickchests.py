from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import credentials, time

streamers = ['jonahveil', 'exiales', 'y0ttabyte','arengeeeternal']

print("Which streamer do you want to watch? ")
print("0. Jonah Veil")
print("1. Exiales")
print("2. Y0ttabyte")
print("3. arengeeeternal")
s_num = int(input(""))

browser = webdriver.Chrome()

# Log into twitch in the browser
browser.get('http://www.twitch.tv/' + streamers[s_num])
login = browser.find_element_by_xpath("//button[@data-a-target='login-button']")
login.click()
time.sleep(2)
username = browser.find_element_by_xpath("//input[@autocomplete='username']")
username.send_keys(credentials.login['username'])
password = browser.find_element_by_xpath("//input[@autocomplete='current-password']")
password.send_keys(credentials.login['password'])
login = browser.find_element_by_xpath("//button[@data-a-target='passport-login-button']")
time.sleep(10)
login.click()

time.sleep(10)
# If mature check, click it
try:
    mature = browser.find_element_by_id("mature-link")
    mature.click()
except NoSuchElementException:
    pass

time.sleep(15)
# Find the correct iframe

def findIFrame():
    for x in browser.find_elements_by_tag_name("iframe"):
        try:
            browser.switch_to.frame(x)
            time.sleep(10)
            drop = browser.find_element_by_class_name("newDrop")
            # Iframe located
            return x
        except NoSuchElementException:
            iframe = findIFrame()
            if (iframe):
                return iframe
            browser.switch_to.parent_frame()
            time.sleep(10)
    return

iframe = findIFrame()

while(True):
    try:
        if (iframe is None):
            raise StaleElementReferenceException
        drops = browser.find_elements_by_class_name("newDrop")
        for drop in drops:
            if ('dropHide' not in drop.get_attribute('class')):
                print("Found a chest!")
                drop.click()
    except StaleElementReferenceException:
        browser.switch_to.default_content()
        iframe = findIFrame()
        browser.switch_to.frame(iframe)
    except NoSuchElementException:
        pass

    time.sleep(15)
