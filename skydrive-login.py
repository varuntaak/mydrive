import requests, os, dircache
from pprint import pprint
from bottle import get, post, request,  route, run

session = requests.session()
host = 'https://login.live.com/oauth20_authorize.srf?client_id=000000004C128E28&scope=wl.signin%20wl.basic%20wl.skydrive_update&response_type=code&redirect_uri=http%3A%2F%2Fwww.gyansource.com%2Flogin'
url_profile = 'https://apis.live.net/v5.0/me?access_token='
url_access_token = 'https://login.live.com/oauth20_token.srf?'
url_post_files = 'https://apis.live.net/v5.0/me/skydrive/files'
#access_token_g = ''

base_location = '/home/varun/study/python'


@get('/login')
def getLogin():
	r = session.get(host)
	print r.text
	return r.text
 
@get('/login/<code>')
def loginToSynch(code):
	if (code is None):
	 return 'Not a valid code'
	else:
	 print code
	 r = session.get(url_access_token + code)
      	 return r.text
        
@get('/me/<access_token>')
def getMyData(access_token):
    r = session.get(url_profile +'"'+access_token+'"')
    return r.text

@post('/synch/<access_token:re:.+>')
def startSynching(access_token):
    global access_token_g
    access_token_g = access_token
    return synch(base_location)

def synch(root):
    for new_root, dirs, files in os.walk(root, topdown=True):
        print files
        uploadFiles(files, new_root)
    return 'success'
#        uploadDirs(dirs)

def uploadFiles(files, path):
    print(path)
    os.chdir(path)
    path = path.replace(base_location, '')
    print(path)
    for name in files:
        fileItem = open(name, 'r')
        headers = {'Content-Disposition': 'form-data; name="file"; filename="'+ fileItem.name +'"'}
        files = {'file': (fileItem.name, fileItem, 'application/octet-stream', headers)}
        url = url_post_files + path + '"?access_token=' + access_token_g + '"'
        print(url)
        r = session.post(url, files=dict(files))
        print(r.status_code)
        print(r.text)
    return

#def uploadDirs(dirs):
        

@get('/test/<url:re:.+>')
def test(url):
    print (url)
    fileList = dircache.listdir(base_location)       
    fileItem = open('browser.py', 'r')
    headers = {
    'Content-Disposition': 'form-data; name="file"; filename="test.txt"'}
    files = {'file': (fileItem.name, fileItem, 'application/octet-stream', headers)}
    pprint(fileItem)
    response = requests.post('http://httpbin.org/post', files=dict(files))
    pprint(response.json())

def testDir():
    for new_root, dirs, files in os.walk(base_location, topdown=True):
        print files
        print dirs
        print new_root

testDir()
run()
