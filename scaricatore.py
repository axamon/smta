import requests
import time
import redis
from datetime import datetime
import uuid
rlocal = redis.StrictRedis()

def update_stats(context, value, type='test'):
	destination = 'stats:%s:%s'%(context, type)
	rlocal.hsetnx(destination, 'min', value) 
	rlocal.hsetnx(destination, 'max', value) 
	if value < float(rlocal.hget(destination, 'min')):
		rlocal.hset(destination, 'min', value)
	if value > float(rlocal.hget(destination, 'max')):
		rlocal.hset(destination, 'max', value)		
       	rlocal.hincrby(destination, 'count',1)
       	rlocal.hincrbyfloat(destination, 'sum', value)
       	rlocal.hincrbyfloat(destination, 'sumq', value*value)

t=0
while True:
	chunk = "http://vodabr.cb.ticdn.it/videoteca2/V3/Film/2014/04/50403788/SS/10422185/10422185.ism/QualityLevels(5500000)/Fragments(video="+str(t)+")"
	idvideoteca = chunk.split("/")[8]
	response = requests.get(chunk)
	print response.status_code, response.elapsed.total_seconds(), float(response.headers['Content-Length'])/1024/response.elapsed.total_seconds()/1024, response.headers['VT3'], response.url.split("/")[2]
	print response.headers
	tts = float(response.elapsed.total_seconds())
	print tts
	update_stats(idvideoteca, tts)
	t=t+20000000
	#time.sleep(1)

