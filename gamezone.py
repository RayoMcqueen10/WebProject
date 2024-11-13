from flask import Flask, render_template, url_for,request,redirect, session
from flask_mysqldb import MySQL
from flask_login import LoginManager,login_user,logout_user
from config import config
from werkzeug.security import generate_password_hash
import datetime 
from models.ModelUser import ModelUser
from models.entities.User import User


gamezone = Flask(__name__)
db=MySQL(gamezone)
adminSesion = LoginManager(gamezone)

@adminSesion.user_loader
def cargarUsuario(id):
    return ModelUser.get_by_id(db, id)

@gamezone.route('/')
def home():
    '''if session['NombreU']:
        if session['PerfilU'] == 'A':
            return render_template('admin.html')
        else:
            return render_template('user.html')'''
    return render_template('home.html')

@gamezone.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        nombre=request.form['nombre']
        correo=request.form['correo']
        clave=request.form['clave']
        claveCifrada=generate_password_hash(clave)
        fechareg=datetime.datetime.now()
        regUsuario=db.connection.cursor()
        regUsuario.execute("INSERT INTO usuario (nombre, correo, clave, fechareg) VALUES (%s,%s,%s,%s)",(nombre, correo, claveCifrada, fechareg))
        db.connection.commit()
        return render_template('home.html')
    else:
        return render_template('signup.html')
        
    
@gamezone.route('/signin', methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        usuario = User(0, None, request.form['correo'], request.form['clave'], None,  None)
        usuarioAutenticado =  ModelUser.signin(db,  usuario)
        if usuarioAutenticado is not None:
            login_user(usuarioAutenticado)
            session['NombreU'] = usuarioAutenticado.nombre
            session['Perfil.U']  = usuarioAutenticado.perfil
            if  usuarioAutenticado.clave:
                if usuarioAutenticado.perfil == 'A':
                    return render_template('admin.html')
                else:
                    return render_template('user.html')
            else:
                flash('CONTRASEÑA INCORRECTA')
                return redirect(request.url)
        else:
            flash('CORREO INCORRECTO')
            return redirect(request.url)
    else:
        return render_template('signin.html')

@gamezone.route('/signout', methods=['GET', 'POST'])
def signout():
    logout_user()
    return render_template('home.html')

@gamezone.route('/sUsuario', methods=['GET','POST'])
def sUsuario():
    selUsuario = db.connection.cursor()
    selUsuario.execute("SELECT * FROM usuario")
    u = selUsuario.fetchall()
    selUsuario.close()
    return render_template('usuarios.html', usuarios = u)

@gamezone.route('/iUsuario', methods=['GET', 'POST'])
def iUsuario():
    nombre = request.form['nombre']
    correo = request.form['correo']
    clave = request.form['clave']
    claveCifrada = generate_password_hash(clave)
    fechareg = datetime.datetime.now()
    perfil = request.form['perfil']
    creaUsuario= db.connection.cursor()
    creaUsuario.execute("INSERT INTO usuario (nombre, correo, clave, fechareg, perfil) VALUES (%s,%s,%s,%s,%s)", (nombre, correo, claveCifrada, fechareg, perfil))
    db.connection.commit()
    flash('usuario creado')
    return redirect('/sUsuario')

@gamezone.route('/uUsuario/<int:id>', methods=['GET', 'POST'])
def uUsuario(id):
    nombre = request.form['nombre']
    correo = request.form['correo']
    clave = request.form['clave']
    claveCifrada = generate_password_hash(clave)
    fechareg = datetime.datetime.now()
    perfil = request.form['perfil']
    editarUsuario= db.connection.cursor()
    editarUsuario.execute("UPDATE usuario SET nombre=%s, correo=%s, clave=%s, fechareg=%s, perfil=%s WHERE id=%s", (nombre, correo, claveCifrada, fechareg, perfil, id))
    db.connection.commit()
    flash('Usuario Actualizado')
    return redirect('/sUsuario')

@gamezone.route("/dUsuario/<int:id>", methods=['GET', 'POST'])
def dUsuario(id):
    eliminarusuario = db.connection.cursor()
    eliminarusuario.execute("DELETE FROM usuario WHERE id = %s", (id,))
    db.connection.commit()
    flash('Usuario Eliminado')
    return redirect('/sUsuario')

@gamezone.route('/sProducto',  methods=['GET', 'POST'])
def sProducto():
    selProducto=db.connection.cursor()
    selProducto.execute("SELECT * FROM productos")
    p=selProducto.fetchall()
    selProducto.close()
    return render_template('productos.html', productos=p)

if __name__ == '__main__':
    gamezone.config.from_object(config['development'])
    gamezone.run(port=3300)