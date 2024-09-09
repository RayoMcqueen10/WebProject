from flask import Flask, render_template, url_for

gamezone = Flask(__name__)

@gamezone.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':  
   gamezone.run(debug=True,port=3300)  