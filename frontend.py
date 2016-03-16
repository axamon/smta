from bottle import route, run, template
import redis

rlocal = redis.StrictRedis()

@route('/testa/<id>')
def index(id):
    rlocal.lpush('filmdatestare',id)
    return template('<b>film con id {{id}} aggiunto alla lista di quelli da testare</b>!', id=id)
	

run(host='0.0.0.0', port=8080)
