from selenium import webdriver
import time
import sys

print '''
Sintassi: <username> <password> <id videoteca>	

Copyright Alberto Bregliano

'''

profile = webdriver.FirefoxProfile()
profile.set_preference('plugin.state.npctrl', 2)

browser = webdriver.Firefox(profile)
browser.get('http://www.timvision.it')
accettacookie = browser.find_element_by_id('cookieChoiceDismiss')
type(accettacookie)
accettacookie.click()
browser.maximize_window()
accedi = browser.find_element_by_link_text('Accedi')
type(accedi)
accedi.click()
time.sleep(1)
username = browser.find_element_by_id('loginUsernameId')
username.send_keys(sys.argv[1])
pwd =browser.find_element_by_id('loginPwdId')
pwd.send_keys(sys.argv[2])
accedi2 = browser.find_element_by_id('loginBtn')
type(accedi2)
accedi2.click()
time.sleep(2)
browser.get('http://www.timvision.it/detail/'+sys.argv[3])
time.sleep(2)
guarda = browser.find_element_by_link_text('Guarda')
type(guarda)
guarda.click()

