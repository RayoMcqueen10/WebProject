from flask import Flask, render_template, url_for,request,redirect
from flask_mysqldb import MySQL
from flask_login import LoginManager,login_user,logout_user
from config import config
from werkzeug.security import generate_password_hash
import datetime


gamezone = Flask(__name__)
db = MySQL(gamezone)
#adminSession = LoginManager(gamezone)

@gamezone.route('/')
def home():
    return render_template('home.html')

@gamezone.route('/signup')
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

if __name__ == '__main__':  
   gamezone.config.from_object(config['development'])
   gamezone.run(port=3300)  
