from selenium import webdriver
import time
import sys
import redis

rlocal = redis.StrictRedis(host='ghostbuster.ddns.net') 


while True:
	idvideoteca=str(rlocal.brpop('filmdatestare',0)[1])
	print idvideoteca
	print '''
	Sintassi: <username> <password> <id videoteca>	
	
	Copyright Alberto Bregliano

	'''
	time.sleep(3)
	profile = webdriver.FirefoxProfile()
	profile.set_preference('plugin.state.npctrl', 2)
	browser = webdriver.Firefox(profile)
	browser.maximize_window()
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
	username.send_keys(rlocal.get('username'))
	pwd =browser.find_element_by_id('loginPwdId')
	pwd.send_keys(rlocal.get('password'))
	accedi2 = browser.find_element_by_id('loginBtn')
	type(accedi2)
	accedi2.click()
	time.sleep(2)
	browser.get('http://www.timvision.it/detail/'+idvideoteca)
	time.sleep(2)
	guarda = browser.find_element_by_link_text('Guarda')
	type(guarda)
	guarda.click()
	time.sleep(30)
	browser.quit()
