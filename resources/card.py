"""
Creates resources that represent various states and attributes of cards within
a job search Trello board. The code consumes a batch API of Trello data that
features cards across 3 lists; each list representing a job search status. The
cards data is organized and summarized JSON responses for each relevant resource's
Get endpoint. The resources each represent a slice of the job search data. The
endpoints are designed to minimize the work of a client to display a summary
of the relevant job search data.
"""
from flask_restful import Resource

import trello_request
from configs import *

# URL for Trello batch API comprised of IDs stored in configs.py file
trelloApiUrl = "https://api.trello.com/1/batch?urls=/lists/{0}/cards,/lists/{1}/cards,/lists/{2}/cards&key={3}&token={4}".format(
                TRELLO_APPLIED_LIST_ID,
                TRELLO_INTERVIEWING_LIST_ID,
                TRELLO_CLOSED_LIST_ID,
                TRELLO_API_KEY,
                TRELLO_API_TOKEN)

# Trello API request
trelloResponse, trelloStatusCode = trello_request.getApiResponse(trelloApiUrl)

# Initialize JSON that contains superset of cards data as a skeleton dicionary
cardsJSON = {'jobSearchCards':
                {'totalExplores': 0},
             'cardsByStatus':
                {
                    'Applied': 0,
                    'Interviewing': 0,
                    'Closed': 0
                },
             'cardsByIndustry': {},
             'cardsByOutcome': {}
            }

# Initialize a tuple of the relevant job search activities/outcomes
outcomes = ('Phone interview',
            'On-site interview',
            'No interview',
            'Offer',
            'Explore')

for lists in trelloResponse.json():
    # The batch JSON response includes three 'list' groupings of Trello
    # cards; one for each workflow step of job search exploration
    for cards in lists['200']:

        # If the 'idList' element of the card matches the ID of workflow
        # status stored in the environment variable, increment the count
        # in the JSON
        if cards['idList'] == TRELLO_APPLIED_LIST_ID:
            cardsJSON['cardsByStatus']['Applied'] += 1
        elif cards['idList'] == TRELLO_INTERVIEWING_LIST_ID:
            cardsJSON['cardsByStatus']['Interviewing'] += 1
        elif cards['idList'] == TRELLO_CLOSED_LIST_ID:
            cardsJSON['cardsByStatus']['Closed'] += 1

        # Check the label(s) of each card and put the data into the relevant
        # dicionary of the JSON - either 'outcome' or 'industry'
        for label in cards['labels']:
            if label['name'] in outcomes:
                x = cardsJSON['cardsByOutcome'].get(label['name'], 1) + 1
                cardsJSON['cardsByOutcome'].update({label['name']: x})
            else:
                y = cardsJSON['cardsByIndustry'].get(label['name'], 1) + 1
                cardsJSON['cardsByIndustry'].update({label['name']: y})

        # As each card is checked, increment the overall count in the JSON
        cardsJSON['jobSearchCards']['totalExplores'] += 1

class AllCards(Resource):
    def get(self):
        # Return an error if the Trello API request fails; else return the
        # dictionary holding the overall summary of cards data
        if trelloStatusCode != 200:
            return {"message": "An error occurred retrieving the Companies data from Trello."}, 500
        else:
            return cardsJSON

class AppliedCards(Resource):
    def get(self):

        # Return an error if the Trello API request fails
        if trelloStatusCode != 200:
            return {"message": "An error occurred retrieving the Companies data from Trello."}, 500

class InterviewCards(Resource):
    def get(self):

        # Return an error if the Trello API request fails
        if trelloStatusCode != 200:
            return {"message": "An error occurred retrieving the Companies data from Trello."}, 500

class ClosedCards(Resource):
    def get(self):

        # Return an error if the Trello API request fails
        if trelloStatusCode != 200:
            return {"message": "An error occurred retrieving the Companies data from Trello."}, 500
