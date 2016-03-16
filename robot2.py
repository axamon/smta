from selenium import webdriver
import time
import sys
import redis

#rlocal = redis.StrictRedis(host='ghostbuster.ddns.net')
#rlocal =  redis.StrictRedis(host='pub-redis-12272.us-east-1-4.4.ec2.garantiadata.com', port=12272, password='smta')
rlocal = redis.StrictRedis(host='vocvideo.ddns.net')

while True:
	idvideoteca=str(rlocal.brpoplpush('filmdatestare','filmdatestare',0))
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
	accettacookie = browser.find_element_by_xpath('//*[@id="cookiebox"]/p[2]/a')
	type(accettacookie)
	try:
    		accettacookie.click()
	except:
       		self.browser.execute_script(
			 '$("{sel}").click()'.format(sel=el_selector)
        		)
	#accettacookie.click()
	browser.maximize_window()
	accedi = browser.find_element_by_link_text('Accedi')
	type(accedi)
	accedi.click()
	time.sleep(1)
	username = browser.find_element_by_id('loginUsernameId')
	username.send_keys(rlocal.get('username'))
	time.sleep(2)
	pwd =browser.find_element_by_id('loginPwdId')
	pwd.send_keys(rlocal.get('password'))
	time.sleep(2)
	accedi2 = browser.find_element_by_id('loginBtn')
	type(accedi2)
	accedi2.click()
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
    		self.browser.execute_script(
			 	'$("{sel}").click()'.format(sel=el_selector)
        			)
	#guarda.click()
	time.sleep(300)
	browser.quit()
