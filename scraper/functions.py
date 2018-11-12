
# Create your views here.
from bs4 import  Doctype
import requests
import re

# returns doctype of html document which determines it's version

def doctype(soup):
    items = [item for item in soup.contents if isinstance(item, Doctype)]
    return items[0] if items else None

# get html version of document
def html_version(soup):


    version = doctype(soup)

    # if doctype is html, version is html5, other doctypes are self explanitory
    if version == "html":
        version = "HTML5"
    elif not version:
        version = "Cannot specify HTML version"

    return version

# returns html document page title
def page_title(soup):
    return soup.title.text

# returns dict of number of headings in document
def headings(soup):

    return {
    "h1": len(soup.find_all('h1')),
    "h2": len(soup.find_all('h2')),
    "h3": len(soup.find_all('h3')),
    "h4": len(soup.find_all('h4')),
    "h5": len(soup.find_all('h5')),
    "h6": len(soup.find_all('h6'))
    }

# returns number of internal, external, inaccesable links
def number_of_links(soup, domain_name):

    internal_len = 0
    external_len = 0
    inaccessible_len = 0

    for link in soup.find_all('a', attrs={'href': re.compile("^http://")}):

        print(link)
        if len(link['href']) > 0 and link['href'][0] == '/':

            # link is inaccessible if the HTTP response status is not 200
            req = requests.get(domain_name + link['href'][1:])
            if req.status_code != 200:
                print(domain_name + link['href'][1:])
                inaccessible_len += 1

            internal_len += 1

        elif len(link['href']) > 0 and link['href'][0] == '#':
            req = requests.get(url + link['href'])
            if req.status_code != 200:
                print("")
                inaccessible_len += 1

            internal_len += 1

        else:

            req = requests.get(link['href'])
            if req.status_code != 200:
                print("as")
                inaccessible_len += 1

            external_len += 1

    return {"internal": internal_len, "external": external_len, "inaccessible": inaccessible_len}

# if page has login page
def has_login(soup):

    # if page has more that one password field on it
    pass_input_len = len(soup.findAll('input', {'type': 'password'}))
    return pass_input_len > 0



