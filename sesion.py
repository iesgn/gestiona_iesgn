from bottle import response,request
import uuid

class Sesion:
	info={}

	def start(self):
		id=uuid.uuid4()
		print id
		self.info[str(id)]={}
		response.set_cookie("id", str(id))

	def load(self):
		if self.has_sesion():
			return request.get_cookie("id")
		else:
			self.info[request.get_cookie("id")]={}
			return request.get_cookie("id")
			


	def set(self,key,value):
		id=request.get_cookie("id")
		self.info[id][key]=value
		print self.info
	
	def get(self,key):
		if self.has_sesion():
			return self.info[request.get_cookie("id")][key]
		else:
			return ""
	def islogin(self):
		if self.has_sesion():
			return self.info[request.get_cookie("id")].has_key("user")
		else:
			return False

	def delete(self):
		del self.info[request.get_cookie("id")]
		response.set_cookie("id", "", max_age=-1)

	def has_sesion(self):
		respuesta = False if request.get_cookie("id") is None else True
		return respuesta





