from flask import Flask

pw = Flask(__name__)

@pw.route('/')
def home():
    return '<h1>Hola mundo</h1>'

if __name__ == '__main__':  
   pw.run(debug=True,port=3300)  