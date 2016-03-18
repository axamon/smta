from selenium import webdriver
import time
import sys
import redis

#rlocal = redis.StrictRedis(host='ghostbuster.ddns.net')
#rlocal =  redis.StrictRedis(host='pub-redis-12272.us-east-1-4.4.ec2.garantiadata.com', port=12272, password='smta')
rlocal = redis.StrictRedis(host='vocvideo.ddns.net')

while True:
	try:
		idvideoteca=str(rlocal.brpoplpush('filmdatestare','filmdatestare',0))
		print idvideoteca
		print '''
		Copyright Alberto Bregliano
		
		tutti i diritti riservati
		'''
		time.sleep(3)
		profile = webdriver.FirefoxProfile()
		profile.set_preference('plugin.state.npctrl', 2)
		browser = webdriver.Firefox(profile)
		browser.maximize_window()
		browser.get('http://www.timvision.it')
		accettacookie = browser.find_element_by_link_text('OK')
		type(accettacookie)
		try:
				accettacookie.click()
		except:
				pass
		#accettacookie.click()
		browser.maximize_window()
		time.sleep(5)
		accedi = browser.find_element_by_link_text('Accedi')
		type(accedi)
		try:
			accedi.click()
		except:
			pass
		time.sleep(1)
		username = browser.find_element_by_id('loginUsernameId')
		try:
			username.send_keys(rlocal.get('username'))
		except:
			pass
		time.sleep(2)
		pwd =browser.find_element_by_id('loginPwdId')
		try:
			pwd.send_keys(rlocal.get('password'))
		except:
			pass
		time.sleep(2)
		accedi2 = browser.find_element_by_id('loginBtn')
		type(accedi2)
		try:
			accedi2.click()
		except:
			pass
		time.sleep(2)
		browser.get('http://www.timvision.it/detail/'+idvideoteca)
		time.sleep(2)
		#guarda = browser.find_element_by_xpath('//*[@id="spct"]/div[3]/div/div[5]/a[3]')
		#guarda = browser.find_elements_by_class_name('button asset')
		guarda = browser.find_element_by_link_text('Guarda')
		type(guarda)
		try:
				guarda.click()
		except:
			pass
		for handle in browser.window_handles:
    			browser.switch_to_window(handle)
    			browser.maximize_window()
    			#browser.set_window_size(1920,1080)
		#guarda.click()
		time.sleep(30)
		browser.quit()
		rlocal.set('chiusura','ok')
	except:
		pass
