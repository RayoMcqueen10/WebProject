from flask_login import UserMixin 
from werkzeug.security import check_password_hash

class User(UserMixin):
    def __init__(self,id,titulo,correo,clave,fechareg,perfil)-> None:
        self.id     = id 
        self.titulo = titulo
        self.correo = correo
        self.clave  = clave
        self.fecharef = fechareg
        self.perfil = perfil

    @classmethod 
    def validarClave(self,claveCifrada,clave):
        return check_password_hash(claveCifrada,clave)      
