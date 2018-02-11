# trello-job-api
This is an API that exposes a subset of data from a private Trello board tracking my 2017/2018 job search activity. This "experience" API features resources that summarize data from Trello's API in a highly condensed and streamlined fashion. The design of the API and presentation of the summarized Trello data is meant to minimize the work required by a client to render the information.

## Trello prerequisites and API assumptions
* Visit https://developers.trello.com to understand the Trello API and get set up to make requests.
* This API is built with the following assumptions and Trello board designs in mind:
- A Trello board exists with three lists that each represent a stage in a job search workflow exploring a given opportunity - Applied, Interviewing, Closed.
- Each job opportunity is represented as a Trello card that lives within one of the three lists. The naming convention for each card on the Trello board is "<Company Name> - <Job Title>"
- Card Labels are used to classify a job opportunity by 1.) job search explore step achievement; and 2.) industry of job opportunity. There is only one set of Label options within Trello, so values across these two classifications are stored within the same list. Each card is tagged with two label values to reflect the current (or most advanced) explore stage and the industry of the opportunity.
- See <future URL> for a sample Trello board that would support this API.

## API Resources:
* companies -
* cards -
* applications -
* interviews -
* closed-cards -
