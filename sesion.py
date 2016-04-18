from bottle import request

def set(key,value):
	s = request.environ.get('beaker.session')
	
	s[key]=value

def get(key):
	s = request.environ.get('beaker.session')
	
	if key in s:
		return s[key]
	else:
		return ""

def delete():
	s = request.environ.get('beaker.session')
	
	s.delete()

def islogin():
	s = request.environ.get('beaker.session')
	
	return 'user' in s






