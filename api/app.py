from flask import Flask, session, jsonify, request
from flask_cors import CORS, cross_origin, logging
from route.users import users_api
from route.songs import songs_api
from route.leaderboards import leaderboards_api
from route.auth import auth_api
from route.profile import profile_api
from service.cache import init_cache
from flasgger import Swagger

import faulthandler
faulthandler.enable()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.secret_key = 'super secret key'
app.config['SWAGGER'] = {
    'title': 'Flask API Starter Kit',
}

swagger = Swagger(app)
app.register_blueprint(users_api, url_prefix='/users')
app.register_blueprint(songs_api, url_prefix='/songs')
app.register_blueprint(leaderboards_api, url_prefix='/leaderboards')
app.register_blueprint(auth_api, url_prefix='/auth')
app.register_blueprint(profile_api, url_prefix='/profile')
init_cache(app)

def create_app():
    appd = Flask(__name__)
    CORS(appd) 
    app.config['CORS_HEADERS'] = 'Content-Type'


    appd.secret_key = 'super secret key'
    appd.config['SWAGGER'] = {
        'title': 'Flask API Starter Kit',
    }
    swagger = Swagger(appd)
    appd.register_blueprint(users_api, url_prefix='/users')
    appd.register_blueprint(songs_api, url_prefix='/songs')
    init_cache(appd)
    return appd

@app.route('/hello')
@cross_origin()
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    #app = create_app()
    #app.run(debug=True, host='0.0.0.0', port=5000)
    #app.run(host='0.0.0.0', port=5001)
    app.run()

