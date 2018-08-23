# Shifty [![CircleCI](https://circleci.com/gh/emaohi/Shifty.svg?style=svg)](https://circleci.com/gh/emaohi/Shifty)
### Tools used and main features

#### Shift-Generation-Algorithm
The app can choose in runtime between:
1. "Thoughtful" algorithm which takes into consideration
the employee request and his rank
2. Naive method which only consider manager requirements.

#### Wrong-details request
An Employee can request to change some of his details (time in business & role). Other attributes
can be change directly by the employee.

#### Swap-requests
An Employee can ask to swap shifts with another employee who has *the same role* 
that is assigned to a *different* shift in the same week. The manager can approve/reject this request. 

#### Caching
The following resources are being cached for accelerating requests:
1. ETL to business
2. old employee requests (manager user)
3. old manager messages (employee user)
4. old swap requests
5. previous shifts (manager & employee)
5. slot-names

#### Leader-Board
Uses Redis sorted-set capability to hold the 5 highest ranked employees of a business.
Updates when necessary along with the DB.

#### Search
Through ElasticSearch Previous shifts can be free-searched, with highlighting and ES scores.

#### Third-party-APIs
1. Google maps API -for calculating walking&driving ETAs 
from user's home address to the business.
2. Profanity API - for detecting bad language when employee submit request to his manager
3. Holidays API - for mentioning them in shifts

#### Logo-finder
When registering new business, scraping of restaurants website to find the business logo 
begins upon entering the business name, suggesting the result logo to the user.

#### Anonymous user support
Anonymous user can send request to be added to existing business. Will expire the browser session
to prevent multiple anonymous requests.

#### Celery & RabbitMQ jobs (Scheduled / Upon request)
1. Update Holidays
2. Re-send joining emails to users which haven't got theirs yet.
3. Indexing shifts to ElasticSearch.
4. Start shift generation process upon manager request.
5. Send mail in various scenarios (employee registration, employee request,
manager response, etc)

#### HealthCheck page
monitors the availability of:
1. MySQL Database
2. Redis cache
3. 3rd party APIs
4. ElasticSearch
5. Celery workers (through RabbitMQ)
6. Logo Fetcher
  
