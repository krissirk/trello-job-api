"""
This module contains a function that submits an API request to the passed URL
and returns the response and status code.
"""
import requests

def getApiResponse(url):

    apiStatusCode = 0

    try:
        apiResponse = requests.get(url, timeout=10)
        apiResponse.close()
        apiStatusCode = apiResponse.status_code
    except:
        None

    return apiResponse, apiStatusCode
