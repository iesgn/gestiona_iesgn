from bottle import response,request

def set(key,value):
	s = request.environ.get('beaker.session')
	s[key]=value

#	def get(self,key):
#		if self.has_sesion():
#			return self.info[request.get_cookie("id")][key]
#		else:
#			return ""
#	def islogin(self):
#		if self.has_sesion():
#			return self.info[request.get_cookie("id")].has_key("user")
#		else:
#			return False#

def delete():
	s = request.environ.get('beaker.session')
	s.delete()

#	def has_sesion(self):
#		respuesta = False if request.get_cookie("id") is None else True
#		return respuesta





