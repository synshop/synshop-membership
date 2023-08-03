from bottle import *
import stripe

@route('/')
def index():
    return template('templates/index.html')

run(host='0.0.0.0', port=8080)

