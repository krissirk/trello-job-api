"""
Creates a resource that features a lone Get endpoint to expose the total
list of companies that have been explored during job search. The code
consumes a batch API of Trello data that features cards across 3 lists.
The cards data is combined into a JSON response that includes the
name of each distinct company that has been explored and a count of each explore
outcome, as well as the total number of times a position with that company has
been pursued.
"""
import operator
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

# Companies resource featuring a single Get endpoint
class Companies(Resource):

    def get(self):

        # Trello API request
        trelloResponse, trelloStatusCode = trello_request.getApiResponse(trelloApiUrl)

        # Build JSON of company data and return it; else, return an error
        # if the Trello API request fails
        if trelloStatusCode == 200:

            # Initialize a list that will store each company value and explore
            # outcome
            companies = []

            # Initialize a tuple of the relevant job search activities/outcomes
            # This tuple will be checked in the logic below to distinguish the two sets
            # of the Trello Labels data and focus on just the exploring outcomes
            outcomes = ('Phone interview',
                        'On-site interview',
                        'No interview',
                        'Offer',
                        'Exploring')

            # Loop through the Trello API response, get each company+explore
            # instance, build an initial list of dictionaries
            for lists in trelloResponse.json():

                # The batch JSON response includes three 'list' groupings of Trello
                # cards; one for each workflow step of job search exploration
                for card in lists['200']:

                    # Set the company name to be the Trello card name stripped
                    # of all characters after an initial "-" is encountered.
                    # The card naming convention is <Company Name> - <Job Desc>
                    cardName = card['name'].split('-')[0].strip()

                    # Loop through each label assigned to the card; build a dict
                    # with the company name as the key and the explore outcome
                    # as the value. If no "outcome" is found, set the dict up
                    # with an "applied" value, indicating that a decision to
                    # interview hasn't been determined yet
                    for label in card['labels']:
                        if label['name'] in outcomes:
                            companies.append({cardName: label['name']})
                        elif len(card['labels']) < 2:
                            companies.append({cardName: "Applied"})

            # Initialize a dictionary that will store the final JSON to be
            # returned by the endpoint
            companyDict = {}

            # Loop through the list of companies and establish a count of each
            # company + explore outcome instance; assemble the dictionary along
            # with a total number of explores observed for each company
            for company in companies:
                for k, v in company.items():
                    if k in companyDict.keys():
                        if v in companyDict[k]["exploreOutcomes"]:
                            companyDict[k]["exploreOutcomes"][v] += 1
                        else:
                            companyDict[k]["exploreOutcomes"][v] = 1
                        companyDict[k]["totalExplores"] += 1
                    else:
                        companyDict.update({k: {"exploreOutcomes": {v: 1}}})
                        companyDict[k]["totalExplores"] = 1

            # Finailze the JSON by putting the dictionary into a list of all the
            # company details and supplement it with a total count of the
            # distinct companies explored during the job search
            companyJSON = {"companies": [companyDict], "distinctCompanies": len(companyDict)}

            return companyJSON
        else:
            return {"message": "An error occurred retrieving the Companies data from Trello."}, 500
