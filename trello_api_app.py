from flask import Flask
from flask_restful import Api
# from flask_jwt import JWT

# from configs import JWT_SECRET
from resources.card import AllExplores, Applications, Interviewing, ClosedExplores
from resources.company import Companies

app = Flask(__name__)
# app.secret_key = JWT_SECRET
api = Api(app)

# jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(AllExplores, '/all-explores')
api.add_resource(Applications, '/applications')
api.add_resource(Interviewing, '/interviews')
api.add_resource(ClosedExplores, '/closed-explores')
api.add_resource(Companies, '/companies')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
