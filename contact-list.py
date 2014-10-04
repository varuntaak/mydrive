import requests
session = requests.session()
host = 'http://localhost:5000'
login_url = '/login'

def login(data):
	r = session.post(host+login_url, data)

def contacts():
	r = session.get(host+'/contacts/page/1')
	print r.text

login({'username':'varun@gs.com', 'password':'varun'})
contacts()





