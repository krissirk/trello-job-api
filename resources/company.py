"""
Creates a resource that features a lone Get endpoint to display the
range of companies that have been explored during job search. The code
consumes a batch API of Trello data that features cards across 3 lists.
The cards data is combined into a sorted JSON response that includes the
name of each distinct company that has been explored and a count of total
number of times a position with that company has been pursued. The resource
and endpoint are design to minimize the work of a client to display a summary
of this company data.
"""
import requests, operator
from flask_restful import Resource
from collections import Counter

from configs import *

# Companies resource featuring a single Get endpoint
class Companies(Resource):

    def get(self):

        # URL for Trello batch API comprised of IDs stored in configs.py file
        trelloApiUrl = "https://api.trello.com/1/batch?urls=/lists/{0}/cards,/lists/{1}/cards,/lists/{2}/cards&key={3}&token={4}".format(
                        TRELLO_APPLIED_LIST_ID,
                        TRELLO_INTERVIEWING_LIST_ID,
                        TRELLO_CLOSED_LIST_ID,
                        TRELLO_API_KEY,
                        TRELLO_API_TOKEN)

        # Trello API request
        try:
        	apiResponse = requests.get(trelloApiUrl, timeout=10)
        	apiResponse.close()
        	apiStatusCode = apiResponse.status_code
        except:
        	return {"message": "An error occurred retrieving the Companies data from Trello."}, 500

        #Initialize a list that will store each company value in the Trello JSON
        companies = []

        for lists in apiResponse.json():

            # The batch JSON response includes three 'list' groupings of Trello
            # cards; one for each workflow step of job search exploration
            for cards in lists['200']:

                # Append the name of each Trello card to the list; the Trello
                # card naming convention is <Company> - <Position Name>, so the
                # card value after the ' -' is stripped away
                companies.append(cards['name'].split('-')[0].strip())

        # Leverage the Counter object to get the count of each instance of a given
        # company name in the list; cast it to be a proper dictionary object
        countedCompanies = dict(Counter(companies))

        # Sort the companies dictionary by name
        sortedCompanies = sorted(countedCompanies.items(), key=operator.itemgetter(0))

        # Initialize the JSON for the Get endpoint and include a total count of
        # the companies in the response
        companyJSON = {'companies': [], 'totalCompanies': len(sortedCompanies)}

        # Put each company and its count into the JSON
        for company in sortedCompanies:
            companyJSON['companies'].append({'name': company[0], 'count': company[1]})

        return companyJSON
