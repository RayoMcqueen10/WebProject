from models.entities.User import User 
from flask_login import login_user

class ModelUser:
    @classmethod
    def signin(self,db,usuario):
        try:
            SelUsuario = db.connection.cursor()
            SelUsuario.execute("SELECT * FROM usuario WHERE correo = %s",(usuario.correo,))
            u = SelUsuario.fetchone()
            if u is not None:
                return User(u[0],u[1],u[2],User.validarClave(u[3],usuario.clave),u[4],u[5])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self,db,id):
        try:
            SelUsuario = db.connection.cursor()
            SelUsuario.execute("SELECT * FROM usuario WHERE id = %s",(id,))
            u = SelUsuario.fetchone()
            if u is not None:
                return User(u[0],u[1],u[2],u[3],u[4],u[5]) 
            else:
                return None
        except Exception as ex:
            raise Exception(ex)