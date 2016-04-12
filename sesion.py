from bottle import response,request
import ldap
def set(username):
	response.set_cookie("account", username, secret='some-secret-key')

def get():
	return request.get_cookie("account", secret='some-secret-key')

def islogin():
	return request.get_cookie("account", secret='some-secret-key')!=None

def delete():
	response.set_cookie("account", "", max_age=-1)

def comprobar(username,password):
	username="uid=%s,ou=People,dc=gonzalonazareno,dc=org" % username
	try:
		con=ldap.initialize("ldap://papion.gonzalonazareno.org")
		con.protocol_version = ldap.VERSION3
		if con.simple_bind_s(username,password)[0]==97:
			return True
		else:
			return False
	except ldap.LDAPError, e:
		return False
