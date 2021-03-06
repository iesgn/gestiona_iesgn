import ldap
import ldap.modlist
import ldif
from io import StringIO
from ldap.cidict import cidict
from unicodedata import lookup, name


class LibLDAP(object):
    base_dn="ou=People,dc=gonzalonazareno,dc=org"
    con=""
    isbind=False


    def __init__(self,username="",password=""):
        self.conectar(username,password)

    def conectar(self,username,password):
        try:
            self.con=ldap.initialize("ldap://ldap.gonzalonazareno.org")
            self.con.protocol_version = ldap.VERSION3
            self.con.opt_sizelimit=3000
            if username!="":
                username="uid=%s,ou=People,dc=gonzalonazareno,dc=org" % username
                respuesta=self.con.simple_bind_s(username,password)[0]
            else:
                respuesta=self.con.simple_bind_s()[0]
            if respuesta==97:
                self.isbind=True
            else:
                self.isbind=False
        except ldap.LDAPError as e:
            self.isbind=False

    def buscar(self,filter):
        result=self.con.search_ext_s(self.base_dn, ldap.SCOPE_SUBTREE, filter,sizelimit=1000)
        return get_search_results(result)
    def add(self,uid,attrs):
        attrs=convertir_dict_str_to_byte(attrs)
        self.con.add_s("uid="+uid+","+self.base_dn,self.addldif(attrs))
        self.con.unbind_s()
    def addldif(self,attrs):
        return ldap.modlist.addModlist(attrs)
    def delete(self,uid):
        self.con.delete_s("uid="+uid+","+self.base_dn)
        self.con.unbind_s()
    def modify(self,uid,new,old):
        new=convertir_dict_str_to_byte(new)
        old=convertir_dict_str_to_byte(old)
        self.con.modify_s("uid="+uid+","+self.base_dn,self.modldif(old,new))
        self.con.unbind_s()
    def modldif(self,old,new):
        return ldap.modlist.modifyModlist(old,new)



class gnLDAP(LibLDAP):
    grupo={'asir1':'1º ASIR',
        'asir2':'2º ASIR',
        'smr1':'1º SMR',
        'smr2':'2º SMR',
        'antiguosalumnos':'Otros',
        'profesores':'Profesor',
        'antiguosprofesores':'A.P.',
        'openstackusers':'OpenStack',
        'tituladosasir':'Titulados ASIR',
        'tituladossmr':'Titulados SMR',}

    def __init__(self,username="",password="",base_dn=""):
        LibLDAP.__init__(self,username,password)
        self.getGrupos()
        if base_dn!="":
            LibLDAP.base_dn = base_dn 
        else:
            LibLDAP.base_dn = "ou=People,dc=gonzalonazareno,dc=org"


    def getGrupos(self):
       
        LibLDAP.base_dn="ou=Group,dc=gonzalonazareno,dc=org"
        self.grupos={}
        for clave,valor in self.grupo.items():
            lista2=self.gnBuscar(cadena="(cn=%s)" % clave)
            self.grupos[clave]=lista2[0]["member"]
            

    def memberOfGroup(self,uid,key=False):
        lista=[]
        for clave,valor in self.grupos.items():
            usuario="uid=%s,ou=People,dc=gonzalonazareno,dc=org" % uid
            if usuario in valor:
                if not key:
                    lista.append(self.grupo[clave])
                else:
                    lista.append(clave)
        return lista

    def isMemberOfGroup(self,uid,grupo):
        return grupo in self.memberOfGroup(uid,key=True)

    def isMemberOfGroups(self,uid,grupos=[]):
        for grupo in grupos:
            if grupo in self.memberOfGroup(uid,key=True):
                return True
        return False


    def modUserGroup(self,uid,grupo,adddel):
        modlist = []
        usuario="uid=%s,ou=People,dc=gonzalonazareno,dc=org" % uid
        if adddel=="add":
            modlist.append((ldap.MOD_ADD, "member", usuario.encode("utf-8") ))
        elif adddel=="del":
            modlist.append((ldap.MOD_DELETE, "member", usuario.encode("utf-8") ))
        else:
            return self.con.modify_s("cn=%s,ou=Group,dc=gonzalonazareno,dc=org"%grupo,modlist)
       

    def gnBuscar(self,filtro={},cadena="",ordenarpor="sn"):
        if len(filtro)>0:
            cadena="(&(objectClass=inetOrgPerson)"
            for campo,valor in filtro.items():
                if campo=="grupo" and valor=='all': 
                    cadena+="(uid=*)"
                elif campo=="grupo": 
                    grupos=[valor]
                    if valor=="alumnos":
                        grupos=["asir1","asir2","smr1","smr2","antiguosalumnos"]
                    elif valor=="soloalumnos":
                        grupos=["asir1","asir2","smr1","smr2"]
                    elif valor=="allprofesores":
                        grupos=["profesores","antiguosprofesores"]
                    elif valor=="alltitulados":
                        grupos=["tituladosasir","tituladossmr"]
                    cadena2="(|"
                    for grupos in grupos:
                        cadena2+="(memberOf=cn=%s,ou=Group,dc=gonzalonazareno,dc=org)" % grupos
                    cadena2+=")"
                    cadena+=cadena2
                else:
                    cadena+="(%s=%s*)" % (campo,valor)
            cadena+=")"
      
        lista = LibLDAP.buscar(self,cadena)
        resultado=[]
        for elem in lista:
            usuario=elem.get_attributes()
            resultado.append(convertir_dict_byte_to_str(usuario))
        if len(resultado)>0 and resultado[0].get(ordenarpor,False):
        	#resultado=sorted(resultado,key=lambda d: normalize(d[ordenarpor][0]))
            resultado=sorted(resultado,key=lambda d: d[ordenarpor][0])
            
        
        return resultado

def get_search_results(results):
    """Given a set of results, return a list of LDAPSearchResult
    objects.
    """
    res = []

    if type(results) == tuple and len(results) == 2 :
        (code, arr) = results
    elif type(results) == list:
        arr = results

    if len(results) == 0:
        return res

    for item in arr:
        res.append( LDAPSearchResult(item) )

    return res

class LDAPSearchResult:
    """A class to model LDAP results.
    """

    dn = 'dc=gonzalonazareno,dc=org'

    def __init__(self, entry_tuple):
        """Create a new LDAPSearchResult object."""
        (dn, attrs) = entry_tuple
        if dn:
            self.dn = dn
        else:
            return

        self.attrs = cidict(attrs)

    def get_attributes(self):
        """Get a dictionary of all attributes.
        get_attributes()->{'name1':['value1','value2',...],
				'name2: [value1...]}
        """
        return self.attrs

    def set_attributes(self, attr_dict):
        """Set the list of attributes for this record.

        The format of the dictionary should be string key, list of
        string alues. e.g. {'cn': ['M Butcher','Matt Butcher']}

        set_attributes(attr_dictionary)
        """

        self.attrs = cidict(attr_dict)

    def has_attribute(self, attr_name):
        """Returns true if there is an attribute by this name in the
        record.

        has_attribute(string attr_name)->boolean
        """
        return self.attrs.has_key( attr_name )

    def get_attr_values(self, key):
        """Get a list of attribute values.
        get_attr_values(string key)->['value1','value2']
        """
        return self.attrs[key]

    def get_attr_names(self):
        """Get a list of attribute names.
        get_attr_names()->['name1','name2',...]
        """
        return self.attrs.keys()

    def get_dn(self):
        """Get the DN string for the record.
        get_dn()->string dn
        """
        return self.dn


    def pretty_print(self):
        """Create a nice string representation of this object.

        pretty_print()->string
        """
        str = "DN: " + self.dn + "n"
        for a, v_list in self.attrs.iteritems():
            str = str + "Name: " + a + "n"
            for v in v_list:
                str = str + "  Value: " + v + "n"
        str = str + "========"
        return str

    def to_ldif(self):
        """Get an LDIF representation of this record.

        to_ldif()->string
        """
        out = StringIO()
        ldif_out = ldif.LDIFWriter(out)
        ldif_out.unparse(self.dn, self.attrs)
        return out.getvalue()



#def normalize(s, encoding = "UTF-8"):
#    if not isinstance(s,unicode):
#        s = s.decode(encoding)
#
#    ret = u""
#    for c in s:
#        n = name(c)
#        pos = n.find("WITH")
#        if pos >= 0:
#            n = n[:pos]
#        n = lookup(n.strip())
#        ret += n
#    return ret
#

def convertir_dict_byte_to_str(usuario):
    valores={}
    for a,b in usuario.items():
        if type(b) == list and "jpeg" not in a:
            valores[a]=[x.decode("utf-8") for x in b]
        else:
            valores[a]=b
    return valores

def convertir_dict_str_to_byte(usuario):
    valores={}
    for a,b in usuario.items():
        if type(b) == str and "jpeg" not in a:
            valores[a]=b.encode("utf-8")
        elif type(b) == list and "jpeg" not in a:
            valores[a]=[x.encode("utf-8") for x in b]
        else:
            valores[a]=b
    return valores