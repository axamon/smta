import requests
import time
import redis
from datetime import datetime
import uuid
rlocal = redis.StrictRedis()

def update_stats(context, value, type='test', timeout=5):
	destination = 'stats:%s:%s'%(context, type)
	#Set up the destination statistics key.
   	start_key = destination + ':start'
	#Handle the current hour/last hour like in common_log().
   	#rlocal = rlocal.rlocalline(True)
   	end = time.time() + timeout
   	#while time.time() < end:
      	try:
	#Handle the current hour/last hour like in common_log().
       	#	tkey1 = str(uuid.uuid4())
       	#	tkey2 = str(uuid.uuid4())
       	#	rlocal.zadd(tkey1, value, 'min')
       	#	rlocal.zadd(tkey2, value, 'max')
	#Add the value to the temporary keys.
    #   		rlocal.zunionstore(destination,[destination, tkey1],aggregate='min')
    #   		rlocal.zunionstore(destination,[destination, tkey2],aggregate='max')
	#Union the temporary keys with the destination stats key, using the appropriate min/max 
    #  		rlocal.delete(tkey1, tkey2)
       		rlocal.hincrby(destination, 'count',1)
       		rlocal.hincrbyfloat(destination, 'sum', value)
       		rlocal.hincrbyfloat(destination, 'sumq', value*value)
	except redis.exceptions.WatchError:
		pass
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

