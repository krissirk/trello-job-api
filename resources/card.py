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
cardsJSON = {'jobSearchExplores':
                {'totalExplores': 0},
                'exploresByStatus': {
                        'Applied': 0,
                        'Interviewing': 0,
                        'Closed': 0
                },
                'exploresByIndustry': {},
                'exploresByOutcome': {}
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
            cardsJSON['exploresByStatus']['Applied'] += 1
        elif cards['idList'] == TRELLO_INTERVIEWING_LIST_ID:
            cardsJSON['exploresByStatus']['Interviewing'] += 1
        elif cards['idList'] == TRELLO_CLOSED_LIST_ID:
            cardsJSON['exploresByStatus']['Closed'] += 1

        # Check the label(s) of each card and put the data into the relevant
        # dicionary of the JSON - either 'outcome' or 'industry'
        for label in cards['labels']:
            if label['name'] in outcomes:
                x = cardsJSON['exploresByOutcome'].get(label['name'], 1) + 1
                cardsJSON['exploresByOutcome'].update({label['name']: x})
            else:
                y = cardsJSON['exploresByIndustry'].get(label['name'], 1) + 1
                cardsJSON['exploresByIndustry'].update({label['name']: y})

        # As each card is checked, increment the overall count in the JSON
        cardsJSON['jobSearchExplores']['totalExplores'] += 1

class AllExplores(Resource):
    def get(self):
        # Return the dictionary holding the overall summary of cards data across
        # all three Trello board lists; else, return an error if the Trello API request fails
        if trelloStatusCode == 200:
            return cardsJSON
        else:
            return {"message": "An error occurred retrieving the Job search data from Trello."}, 500

class Applications(Resource):
    def get(self):
        # Return the dictionary holding the  summary of cards data in the "applied"
        # Trello board list; else, return an error if the Trello API request fails
        if trelloStatusCode == 200:
            applicationsJSON = {'openApplications':
                                {'totalApplied': cardsJSON['exploresByStatus']['Applied']},
                                 'appliedByIndustry': {},
                               }

            for lists in trelloResponse.json():
                for cards in lists['200']:
                    if cards['idList'] == TRELLO_APPLIED_LIST_ID:
                        for label in cards['labels']:
                            if label['name'] not in outcomes:
                                yy = applicationsJSON['appliedByIndustry'].get(label['name'], 0) + 1
                                applicationsJSON['appliedByIndustry'].update({label['name']: yy})

            return applicationsJSON

        else:
            return {"message": "An error occurred retrieving the Job search data from Trello."}, 500

class Interviewing(Resource):
    def get(self):

        # Return the dictionary holding the  summary of cards data in the "interviewing"
        # Trello board list; else, return an error if the Trello API request fails
        if trelloStatusCode == 200:
            interviewsJSON = {'interviewingExplores':
                                {'totalInterviewing': cardsJSON['exploresByStatus']['Interviewing']},
                                 'interviewingByIndustry': {},
                                 'interviewingByOutcome': {}
                               }

            for lists in trelloResponse.json():
                for cards in lists['200']:
                    if cards['idList'] == TRELLO_INTERVIEWING_LIST_ID:
                        for label in cards['labels']:
                            if label['name'] in outcomes:
                                xx = interviewsJSON['interviewingByOutcome'].get(label['name'], 0) + 1
                                interviewsJSON['interviewingByOutcome'].update({label['name']: xx})
                            else:
                                yyy = interviewsJSON['interviewingByIndustry'].get(label['name'], 0) + 1
                                interviewsJSON['interviewingByIndustry'].update({label['name']: yyy})

            return interviewsJSON
        else:
            return {"message": "An error occurred retrieving the Job search data from Trello."}, 500

class ClosedExplores(Resource):
    def get(self):
        # Return the dictionary holding the  summary of cards data in the "interviewing"
        # Trello board list; else, return an error if the Trello API request fails
        if trelloStatusCode == 200:
            closedJSON = {'closedExplores':
                                {'totalClosed': cardsJSON['exploresByStatus']['Closed']},
                                 'closedByIndustry': {},
                                 'closedByOutcome': {}
                               }

            for lists in trelloResponse.json():
                for cards in lists['200']:
                    if cards['idList'] == TRELLO_CLOSED_LIST_ID:
                        for label in cards['labels']:
                            if label['name'] in outcomes:
                                abc = closedJSON['closedByOutcome'].get(label['name'], 0) + 1
                                closedJSON['closedByOutcome'].update({label['name']: abc})
                            else:
                                xyz = closedJSON['closedByIndustry'].get(label['name'], 0) + 1
                                closedJSON['closedByIndustry'].update({label['name']: xyz})

            return closedJSON
        else:
            return {"message": "An error occurred retrieving the Job search data from Trello."}, 500
