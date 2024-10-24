from flask import Flask, render_template, url_for,request,redirect
from flask_mysqldb import MySQL
from flask_login import LoginManager,login_user,logout_user
from config import config
from werkzeug.security import generate_password_hash
import datetime 
from models.ModelUser import ModelUser
from models.entities.User import User


gamezoneApp = Flask(__name__)
db = MySQL(gamezoneApp)
adminSession = LoginManager(gamezoneApp)

@adminSession.user_loader
def signingUser(id):
    return ModelUser.get_by_id(db,id) 

@gamezoneApp.route('/')
def home():
    return render_template('home.html')

@gamezoneApp.route('/signup', methods  = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        claveCIFRADA = generate_password_hash(request.form['clave'])
        fechareg     = datetime.datetime.now()
        regUsuario   = db.connection.cursor()
        regUsuario.execute("INSERT INTO usuario (nombre,correo,clave,fechareg) VALUES (%s, %s, %s, %s)",(nombre, correo, claveCIFRADA, fechareg))
        db.connection.commit()
        return redirect(url_for('home'))
    else:    
        return render_template('signup.html',methods = {'GET','POST'})

@gamezoneApp.route('/signin',methods = ['GET','POST'])
def signin():
    if request.method == 'POST':
        usuario = User(0, None, request.form['correo'], request.form['clave'], None, None)
        usuarioAutenticado =  ModelUser.signin(db, usuario)
        if usuarioAutenticado is not None :
            login_user(usuarioAutenticado)
            if usuarioAutenticado.clave:
                if usuarioAutenticado.perfil == 'A':
                    return render_template('admin.html')
                else:
                    return render_template('user.html')
            else:
                return 'Contraseña Incorrecta'
        else:
            return 'Usuario Inexistente'    
    else: 
        return render_template('signin.html')
@gamezoneApp.route('/sigout',methods=['GET','POST'])
def signout():
    logout_user()
    return render_template('home.html')

if __name__ == '__main__':  
    gamezoneApp.config.from_object(config['development'])
    gamezoneApp.run(port=3300)       