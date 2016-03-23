from bottle import route, run, template
import redis

import os
import sys
rlocal = redis.StrictRedis()

pid = str(os.getpid())
pidfile = "/tmp/testweb.pid"
os.unlink(pidfile)

file(pidfile, 'w').write(pid)


@route('/')
@route('/ciao/<name>')
def greet(name='gringo'):
    return template('Ciao {{name}}, che vuoi?', name=name)
	
@route('/testa/<id>')
def index(id):
    rlocal.lpush('filmdatestare',id)
    return template('<b>film con id {{id}} aggiunto alla lista di quelli da testare</b>!', id=id)
	

@route('/cancella/<id>')
def index(id):
    rlocal.lrem('filmdatestare',0,id)
    return template('<b>film con id {{id}} eliminato dalla lista di quelli da testare</b>!', id=id)
	
@route('/elenca')
def index():
    allfilms = []
    allfilms = rlocal.lrange( "filmdatestare", 0, -1 )
    return {'idvideoteca':allfilms}
	
run(host='0.0.0.0', port=80)
