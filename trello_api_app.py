from flask import Flask
from flask_restful import Api
# from flask_jwt import JWT # if/when i want to add authentication

# from configs import JWT_SECRET # if/when i want to add authentication
from resources.card import AllExplores, Applications, Interviewing, ClosedExplores
from resources.company import Companies

application = Flask(__name__)
# app.secret_key = JWT_SECRET
api = Api(application)

# jwt = JWT(app, authenticate, identity)  # if/when i want to add authentication

api.add_resource(AllExplores, '/all-explores')
api.add_resource(Applications, '/applications')
api.add_resource(Interviewing, '/interviews')
api.add_resource(ClosedExplores, '/closed-explores')
api.add_resource(Companies, '/companies')

if __name__ == '__main__':
    application.run(port=5001, debug=False)
