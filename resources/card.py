"""
Creates ...
"""
import requests, operator
from flask_restful import Resource
from collections import Counter

from configs import *

trelloApiUrl = TRELLO_API_URL

try:
	apiResponse = requests.get(trelloApiUrl, timeout=10)
	apiResponse.close()
	apiStatusCode = apiResponse.status_code
except:
	None

class AllCards(Resource):
    def get(self):
        pass
        #return {'cards': list(map(lambda x: x.json(), StoreModel.query.all()))}

class AppliedCards(Resource):
    def get(self):
        pass
        #return {'applications': list(map(lambda x: x.json(), StoreModel.query.all()))}

class InterviewCards(Resource):
    def get(self):
        pass
        #return {'interviews': list(map(lambda x: x.json(), StoreModel.query.all()))}

class ClosedCards(Resource):
    def get(self):
        pass
        #return {'closedCards': list(map(lambda x: x.json(), StoreModel.query.all()))}
