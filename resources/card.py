"""
Creates ...
"""
import requests, operator
from flask_restful import Resource
from collections import Counter

from configs import *

# URL for Trello batch API comprised of IDs stored in configs.py file
trelloApiUrl = "https://api.trello.com/1/batch?urls=/lists/{0}/cards,/lists/{1}/cards,/lists/{2}/cards&key={3}&token={4}".format(
                TRELLO_APPLIED_LIST_ID,
                TRELLO_INTERVIEWING_LIST_ID,
                TRELLO_CLOSED_LIST_ID,
                TRELLO_API_KEY,
                TRELLO_API_TOKEN)

"""
try:
	apiResponse = requests.get(trelloApiUrl, timeout=10)
	apiResponse.close()
	apiStatusCode = apiResponse.status_code
except:
	None
"""

class AllCards(Resource):
    def get(self):
        pass

class AppliedCards(Resource):
    def get(self):
        pass

class InterviewCards(Resource):
    def get(self):
        pass

class ClosedCards(Resource):
    def get(self):
        pass
