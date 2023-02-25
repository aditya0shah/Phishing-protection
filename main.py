from flask import Flask, render_template, jsonify, request
import json 

app = Flask(__name__)

@app.route('/login')
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)

