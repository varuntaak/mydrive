from bottle import route, run
@route('/')
def index():
    return 'Hola Mundo!'
@route('/hello')
def hello():
	return 'hello world'
run()