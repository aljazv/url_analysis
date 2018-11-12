# URL Scraper

All needed dependencies are in the requirements.txt. To install them use the following command:
```
cd url_analysis
pip install -r requirements.txt
```
First start application locally:
```
python manage.py migrate
python manage.py runserver
```
If you use application locally then to scan a URL send a JSON POST to localhost:8000/url/. The sent JSON should look like this:
```
{
	"url": "https://hostname/path/"
}
```
Example of response:
```
{
    "url": "https://hostname/path/",
    "html_version": "HTML5",
    "title": "TITLE",
    "h1": 4,
    "h2": 4,
    "h3": 7,
    "h4": 2,
    "h5": 5,
    "h6": 2,
    "internal": 267,
    "external": 1,
    "inaccessible": 4,
    "has_login_form": false
}
```
The project took me about 9 hours.

### Sunday 9:00-12:00:


- Deciding between Scrapy and beautifulsoup, decided on beautifulsoup
- using request for fetching websites
- Figuring out the solutions of tasks and writing them on paper
- Thinking about project structure, decided to firstly build functionality for scraping then building REST, lastly caching

Problems:

- Had problems with beautiful soup not able to parse, the solution was to force a parser on initialization
- Was not sure what inaccessible links are meant to be. The first option was that links are hidden, second that if I were to request these links that I would get HTTP response something other than 200. I then decided on second option, so I send requests for all links in HTML document
- I am not sure how to validate if a page has a login form but I decided on the solution where if a document has more than 1 input password field then there is a login form. There is a probability that a page doesn't have login-form (it has signup-form)


### Sunday 15:00-18:00:

- Finishing basic functions for scraping.
- Built REST point.
- Noticed that this kind of scraper does not work on pages where for instance JavaScript builds the page, but I decided that this programming challenge was not meant for these kinds of pages

Problems:

- Deciding between POST or GET when a user is requesting data. Because code assignment specifies that the user must get a response with data. By following REST API principles, neither POST or GET are correct solutions. To follow principles I would need to make 2 calls to the server. 1st to POST URL and getting UUID, 2nd to GET data with data. I ignored principles to follow code assignments

### Monday 9:00-11:00:

- Making cachable requests. Used Django Model to save requested data for 24hr.
- Decided not to use ModelSerializer but rather ordinary Serializer because it was easier to implement and much cleaner

Problems:

- Slight problem with native datetime when comparing datetime from model object and datetime.now(). solution: Use Django timezone

### Monday 13:00-15:00:

- Fixing bugs in functionality
- Adding error handling
- Noticing possible integration of parallel processing when requesting data and implementing it
