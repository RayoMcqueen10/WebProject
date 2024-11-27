from flask import Flask,render_template,url_for,request,redirect,flash, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash
import random
import string
import datetime
from config import config
from models.ModelUser import  ModelUser
from models.entities.User import   User


gamezoneApp = Flask(__name__)
#python enewere dfdf
gamezoneApp.config.from_object(config['development'])
gamezoneApp.config.from_object(config['mail'])
db = MySQL(gamezoneApp)
mail = Mail(gamezoneApp)
adminSesion = LoginManager(gamezoneApp)

@adminSesion.user_loader
def cargarUsuario(id):
    return ModelUser.get_by_id(db, id)

@gamezoneApp.route('/')
def home():
    '''if session['tituloU']:
        if session['PerfilU'] == 'A':
            return render_template('admin.html')
        else:
            return render_template('user.html')'''
    return render_template('home.html')

@gamezoneApp.route('/signup',methods=['GET','POST'])
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
        msg=Message(subject='Bienvenido a gamezone, disfruta de tus tenis', recipients=[correo])
        msg.html = render_template('mail.html', nombre=nombre)
        mail.send(msg)
        return render_template('home.html')
    else:
        return render_template('signup.html')
        
    
@gamezoneApp.route('/signin', methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        usuario = User(0, None, request.form['correo'], request.form['clave'], None,  None)
        usuarioAutenticado =  ModelUser.signin(db,  usuario)
        if usuarioAutenticado is not None:
            login_user(usuarioAutenticado)
            session['tituloU'] = usuarioAutenticado.titulo
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

@gamezoneApp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        correo = request.form['correo']
       
        # Verificar si el correo existe en la base de datos
        cursor = db.connection.cursor()
        cursor.execute("SELECT id, correo FROM usuario WHERE correo = %s", (correo,))
        usuario = cursor.fetchone()
        cursor.close()

        if usuario:
            # Generar un enlace de restablecimiento único
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=20))

            # Guardar el token en la base de datos para validarlo más tarde
            cursor = db.connection.cursor()
            cursor.execute("UPDATE usuario SET reset_token = %s WHERE correo = %s", (token, correo))
            db.connection.commit()
            cursor.close()

            # Enviar un correo con el enlace de restablecimiento
            reset_url = url_for('reset_password', token=token, _external=True)  # URL con token para restablecer
            msg = Message(subject='Restablecer contraseña', recipients=[correo])
            msg.body = f'Haz clic en el siguiente enlace para restablecer tu contraseña: {reset_url}'
            mail.send(msg)

            flash('Te hemos enviado un correo con instrucciones para restablecer tu contraseña.', 'success')
            return redirect(url_for('signin'))
        else:
            flash('El correo no está registrado.', 'danger')

    return render_template('forgot_password.html')

@gamezoneApp.route('/reset-password/<token>', methods=['GET', 'POST'], strict_slashes=False)
def reset_password(token):
    # Verificar si el token es válido
    cursor = db.connection.cursor()
    cursor.execute("SELECT id FROM usuario WHERE reset_token = %s", (token,))
    usuario = cursor.fetchone()
    cursor.close()

    if not usuario:
        flash('El enlace de restablecimiento no es válido o ha expirado.', 'danger')
        return redirect(url_for('signin'))
    if request.method == 'POST':
        nueva_clave = request.form['clave']
        hashed_password = generate_password_hash(nueva_clave)
        cursor = db.connection.cursor()
        cursor.execute("UPDATE usuario SET clave = %s, reset_token = NULL WHERE reset_token = %s", (hashed_password, token))
        db.connection.commit()
        cursor.close()
        flash('Tu contraseña ha sido actualizada con éxito.', 'success')
        return redirect(url_for('signin'))
    return render_template('reset_password.html')

@gamezoneApp.route('/signout', methods=['GET', 'POST'])
def signout():
    session.pop('cart', None)
    logout_user()
    return render_template('home.html')

@gamezoneApp.route('/sUsuario', methods=['GET','POST'])
def sUsuario():
    selUsuario = db.connection.cursor()
    selUsuario.execute("SELECT * FROM usuario")
    u = selUsuario.fetchall()
    selUsuario.close()
    return render_template('usuarios.html', usuarios = u)

@gamezoneApp.route('/iUsuario', methods=['GET', 'POST'])
def iUsuario():
    titulo = request.form['titulo']
    correo = request.form['correo']
    clave = request.form['clave']
    claveCifrada = generate_password_hash(clave)
    fechareg = datetime.datetime.now()
    perfil = request.form['perfil']
    creaUsuario= db.connection.cursor()
    creaUsuario.execute("INSERT INTO usuario (titulo, correo, clave, fechareg, perfil) VALUES (%s,%s,%s,%s,%s)", (titulo, correo, claveCifrada, fechareg, perfil))
    db.connection.commit()
    flash('usuario creado')
    return redirect('/sUsuario')

@gamezoneApp.route('/uUsuario/<int:id>', methods=['GET', 'POST'])
def uUsuario(id):
    titulo = request.form['titulo']
    correo = request.form['correo']
    clave = request.form['clave']
    claveCifrada = generate_password_hash(clave)
    fechareg = datetime.datetime.now()
    perfil = request.form['perfil']
    editarUsuario= db.connection.cursor()
    editarUsuario.execute("UPDATE usuario SET titulo=%s, correo=%s, clave=%s, fechareg=%s, perfil=%s WHERE id=%s", (titulo, correo, claveCifrada, fechareg, perfil, id))
    db.connection.commit()
    flash('Usuario Actualizado')
    return redirect('/sUsuario')

@gamezoneApp.route("/dUsuario/<int:id>", methods=['GET', 'POST'])
def dUsuario(id):
    eliminarusuario = db.connection.cursor()
    eliminarusuario.execute("DELETE FROM usuario WHERE id = %s", (id,))
    db.connection.commit()
    flash('Usuario Eliminado')
    return redirect('/sUsuario')

@gamezoneApp.route('/sProducto',  methods=['GET', 'POST'])
def sProducto():
    selProducto=db.connection.cursor()
    selProducto.execute("SELECT * FROM juegos")
    p=selProducto.fetchall()
    selProducto.close()
    return render_template('juegos.html', juegos=p)

@gamezoneApp.route('/catalogo',  methods=['GET', 'POST'])
def catalogo():
    selcat=db.connection.cursor()
    selcat.execute("SELECT * FROM juegos")
    c=selcat.fetchall()
    selcat.close()
    return render_template('user.html', juegos=c)

@gamezoneApp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    idp=int(request.form['id'])
    selProducto=db.connection.cursor()
    selProducto.execute("SELECT id, titulo, precio, imagen FROM juegos WHERE id = %s", (idp,))
    pc=selProducto.fetchone()
    selProducto.close()
    if not pc:
        return redirect('/catalogo')
    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == idp:
            item['cantidad'] += 1
            break
    else:
        cart.append({
            'id': pc[0],
            'titulo': pc[1],
            'precio': pc[2],
            'imagen': pc[3],
            'cantidad': 1
        })
    session['cart']=cart
    return redirect('/catalogo')

@gamezoneApp.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    idp = int(request.form['id'])
    cart = session.get('cart', [])
    session['cart'] = [item for item in cart if item['id'] != idp]
    return redirect('/view_cart')

@gamezoneApp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        tarjeta = request.form['tarjeta']
        vencimiento = request.form['vencimiento']
        cvv = request.form['cvv']
        titulo_titular = request.form['titulo_titular']
        return redirect('/direccion')
    return render_template('checkout.html')

@gamezoneApp.route('/direccion', methods=['GET', 'POST'])
def direccion():
    if request.method == 'POST':
        titulo = request.form['titulo']
        direccion = request.form['direccion']
        ciudad = request.form['ciudad']
        codigopostal = request.form['codigopostal']
        correo = request.form['correo']
        cart=session.get('cart', [])
        total=sum(item['precio'] * item['cantidad'] for item in cart)
        msg=Message(subject='Gracias por tu compra', recipients=[correo])
        msg.html = render_template('mail2.html', titulo=titulo, juegos=cart, total=total)
        mail.send(msg)
        return redirect('/gracias')
    return render_template('direccion.html')

@gamezoneApp.route('/gracias')
def gracias():
    return render_template('gracias.html')

@gamezoneApp.route('/cart', methods=['GET', 'POST'])
def view_cart():
    cart = session.get('cart', [])
    '''
    print("Contenido del carrito:", cart)
    print(session)
    '''
    cart_valid = [item for item in cart if 'precio' in item and 'cantidad' in item]
    if len(cart) != len(cart_valid):
        print("Elementos inválidos encontrados y excluidos:", [item for item in cart if item not in cart_valid])
    total=sum(item['precio']*item['cantidad'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@gamezoneApp.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if query:
        selProducto = db.connection.cursor()
        selProducto.execute("SELECT * FROM juegos WHERE titulo LIKE %s", ('%' + query + '%',))
        juegos = selProducto.fetchall()
        selProducto.close()
    else:
        juegos = []
    
    return render_template('user.html', juegos=juegos)

@gamezoneApp.route('/iProducto', methods=['GET', 'POST'])
def iProducto():
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    categoria = request.form['categoria']
    plataforma = request.form['plataforma']
    existencias = request.form['existencias']
    imagen = request.form['imagen'] 
    creaProducto= db.connection.cursor()
    creaProducto.execute("INSERT INTO juegos (titulo, descripcion, precio, categoria, plataforma, existencias, imagen) VALUES (%s,%s,%s,%s,%s,%s,%s)", (titulo, descripcion, precio, categoria, plataforma, existencias, imagen))
    db.connection.commit()
    flash('Producto creado')
    return redirect('/sProducto')

@gamezoneApp.route('/uProducto/<int:id>', methods=['GET', 'POST'])
def uProducto(id):
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    categoria = request.form['categoria']
    plataforma = request.form['plataforma']
    existencias = request.form['existencias']
    imagen = request.form['imagen']
    editarProducto= db.connection.cursor()
    editarProducto.execute("UPDATE juegos SET titulo=%s, descripcion=%s, precio=%s, categoria=%s, plataforma=%s, existencias=%s, imagen=%s WHERE id=%s", (titulo, descripcion, precio, categoria, plataforma, existencias, imagen, id))
    db.connection.commit()
    flash('Producto Actualizado')
    return redirect('/sProducto')

@gamezoneApp.route("/dProducto/<int:id>", methods=['GET', 'POST'])
def dProducto(id):
    eliminarProducto = db.connection.cursor()
    eliminarProducto.execute("DELETE FROM juegos WHERE id = %s", (id,))
    db.connection.commit()
    flash('Producto Eliminado')
    return redirect('/sProducto')



'''
if __name__ == '__main__':
    gamezoneApp.config.from_object(config['development'])
    gamezoneApp.run(port=3300)
'''
if __name__ == "__main__":
    gamezoneApp.run(host="0.0.0.0", port=5000, debug=True)