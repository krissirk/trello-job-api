"""
Creates resources that represent various states and attributes of cards within
a job search Trello board. The code consumes a batch API of Trello data that
features cards across 3 lists; each list representing a job search status. The
cards data is organized and summarized into JSON responses for each relevant
resource's Get endpoint. The resources each represent a slice of the job search
data. The endpoints are designed to minimize the work of a client to display a
summary of the relevant job search data.

NB: I have kept the definition of all these resources within the same file in order
to limit the number of times that the Trello API is called. I'm sure there is
a better way to organize all this code. I'm also sure there are much more elegant
ways to parse the Trello JSON and build the custom response for this API.
"""
from flask_restful import Resource

import os, trello_request

# Initialize URL for Trello batch API comprised of IDs stored in config.py file
# (or server envrionment variables) - probably a better way to do this
try:
    from config import *
except:
    TRELLO_APPLIED_LIST_ID = os.environ.get('TRELLO_APPLIED_LIST_ID')
    TRELLO_INTERVIEWING_LIST_ID = os.environ.get('TRELLO_INTERVIEWING_LIST_ID')
    TRELLO_CLOSED_LIST_ID = os.environ.get('TRELLO_CLOSED_LIST_ID')
    TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY')
    TRELLO_API_TOKEN = os.environ.get('TRELLO_API_TOKEN')

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
# This tuple will be checked in the logic below to distinguish the two sets
# of the Trello Labels data and organize the information as intended
outcomes = ('Phone interview',
            'On-site interview',
            'No interview',
            'Offer',
            'Explore')

# Transform the JSON response from Trello into a dictionary of the relevant data
# for this API
for lists in trelloResponse.json():
    # The batch JSON response includes three 'list' groupings of Trello
    # cards; one for each workflow step of job search exploration
    for cards in lists['200']:

        # If the 'idList' element of the card matches the ID of workflow status
        # stored in the environment variable, increment the appropriate count
        # of cards in the JSON being assembled
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
                outcomesCount = cardsJSON['exploresByOutcome'].get(label['name'], 0) + 1
                cardsJSON['exploresByOutcome'].update({label['name']: outcomesCount})
            else:
                industryCount = cardsJSON['exploresByIndustry'].get(label['name'], 0) + 1
                cardsJSON['exploresByIndustry'].update({label['name']: industryCount})

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
        # Return a dictionary holding the summary of cards data in the "applied"
        # Trello board list; else, return an error if the Trello API request fails
        if trelloStatusCode == 200:

            # Initialize JSON
            applicationsJSON = {'openApplications':
                                {'totalApplied': cardsJSON['exploresByStatus']['Applied']},
                                 'appliedByIndustry': {},
                               }

            # Loop through Trello JSON response, grab and summarize relevant data
            # from the "Applied" list, and assign to the JSON for this endpoint
            for lists in trelloResponse.json():
                for cards in lists['200']:
                    if cards['idList'] == TRELLO_APPLIED_LIST_ID:
                        for label in cards['labels']:
                            if label['name'] not in outcomes:
                                appliedIndustryCount = applicationsJSON['appliedByIndustry'].get(label['name'], 0) + 1
                                applicationsJSON['appliedByIndustry'].update({label['name']: appliedIndustryCount})

            return applicationsJSON

        else:
            return {"message": "An error occurred retrieving the Job search data from Trello."}, 500

class Interviewing(Resource):
    def get(self):

        # Return the dictionary holding the  summary of cards data in the "interviewing"
        # Trello board list; else, return an error if the Trello API request fails
        if trelloStatusCode == 200:

            # Initialize JSON
            interviewsJSON = {'interviewingExplores':
                                {'totalInterviewing': cardsJSON['exploresByStatus']['Interviewing']},
                                 'interviewingByIndustry': {},
                                 'interviewingByOutcome': {}
                               }

            # Loop through Trello JSON response, grab and summarize relevant data
            # from the "Interviewing" list, and assign to the JSON for this endpoint
            for lists in trelloResponse.json():
                for cards in lists['200']:
                    if cards['idList'] == TRELLO_INTERVIEWING_LIST_ID:
                        for label in cards['labels']:
                            if label['name'] in outcomes:
                                interviewOutcomeCount = interviewsJSON['interviewingByOutcome'].get(label['name'], 0) + 1
                                interviewsJSON['interviewingByOutcome'].update({label['name']: interviewOutcomeCount})
                            else:
                                interviewIndustryCount = interviewsJSON['interviewingByIndustry'].get(label['name'], 0) + 1
                                interviewsJSON['interviewingByIndustry'].update({label['name']: interviewIndustryCount})

            return interviewsJSON
        else:
            return {"message": "An error occurred retrieving the Job search data from Trello."}, 500

class ClosedExplores(Resource):
    def get(self):
        # Return the dictionary holding the  summary of cards data in the "interviewing"
        # Trello board list; else, return an error if the Trello API request fails
        if trelloStatusCode == 200:

            # Initialize JSON
            closedJSON = {'closedExplores':
                                {'totalClosed': cardsJSON['exploresByStatus']['Closed']},
                                 'closedByIndustry': {},
                                 'closedByOutcome': {}
                               }

            # Loop through Trello JSON response, grab and summarize relevant data
            # from the "Closed" list, and assign to the JSON for this endpoint
            for lists in trelloResponse.json():
                for cards in lists['200']:
                    if cards['idList'] == TRELLO_CLOSED_LIST_ID:
                        for label in cards['labels']:
                            if label['name'] in outcomes:
                                closedOutcomeCount = closedJSON['closedByOutcome'].get(label['name'], 0) + 1
                                closedJSON['closedByOutcome'].update({label['name']: closedOutcomeCount})
                            else:
                                closedIndustryCount = closedJSON['closedByIndustry'].get(label['name'], 0) + 1
                                closedJSON['closedByIndustry'].update({label['name']: closedIndustryCount})

            return closedJSON
        else:
            return {"message": "An error occurred retrieving the Job search data from Trello."}, 500
