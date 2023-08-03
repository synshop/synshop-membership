from bottle import *
import stripe

os.chdir(os.path.dirname(os.path.abspath(__file__)))

@route('/')
def index():
    return template('templates/index.html', headers=request.headers)

run(host='0.0.0.0', port=8080)

