from selenium import webdriver
import time
import sys
import os

if len(sys.argv) is 1:
	print '''
Sintassi: <username> <password> <id videoteca>	
'''
	quit()

if len(sys.argv) < 3:
	user = 'vocedt01@alice.it'
	paswd = 'vocedt01'
	if 'http' in sys.argv[1]:
		idvideoteca = sys.argv[1].split("/")[8]
	else:
		idvideoteca = sys.argv[1]
		
else:
	user = str(sys.argv[1])
	paswd = sty(sys.argv[2])
	idvideoteca = sys.argv[3]


print '''

Copyright Alberto Bregliano
	per aggiornamenti e segnalazioni scrivere a:
	 alberto.bregliano@telecomitalia.it
'''

profile = webdriver.FirefoxProfile()
profile.set_preference('plugin.state.npctrl', 2)

browser = webdriver.Firefox(profile)
browser.get('http://www.timvision.it')
accettacookie = browser.find_element_by_id('cookieChoiceDismiss')
type(accettacookie)
accettacookie.click()
browser.maximize_window()
#Settare schermo a massima definizione
#browser.set_window_size(1920,1080)
accedi = browser.find_element_by_link_text('Accedi')
type(accedi)
accedi.click()
time.sleep(1)
username = browser.find_element_by_id('loginUsernameId')
username.send_keys(user)
pwd =browser.find_element_by_id('loginPwdId')
pwd.send_keys(paswd)
accedi2 = browser.find_element_by_id('loginBtn')
type(accedi2)
accedi2.click()
time.sleep(2)
browser.get('http://www.timvision.it/detail/'+idvideoteca)
time.sleep(2)
guarda = browser.find_element_by_link_text('Guarda')
type(guarda)
guarda.click()

import smta


'''
	sniffa il traffico fino a che non incontra una richista manifest
'''
manifest = smta.sniffa()
#print manifest

'''
	carica su redis le informazioni importanti del manifest
'''
smta.caricamanifest(manifest)

'''
	Cominicia a scaricare tutti i chunks al massimo bitrate e aggiorna redis
'''
smta.scarica(manifest)

#Settare schermo a massima definizione
time.sleep(5)
for handle in browser.window_handles:
    browser.switch_to_window(handle)
    browser.set_window_size(1920,1080)

#browser.set_window_size(1920,1080)

