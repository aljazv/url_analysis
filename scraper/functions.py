
# Create your views here.
from bs4 import  Doctype
import requests
import re
from multiprocessing import Pool
from urllib.parse import urlparse
# returns doctype of html document which determines it's version

def doctype(soup):
    items = [item for item in soup.contents if isinstance(item, Doctype)]
    return items[0] if items else None

# get html version of document
def html_version(soup):


    version = doctype(soup)

    # if doctype is html, version is html5, other doctypes are self explanitory
    if version == "html" or "doctype html":
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

# returns true if page is accessable
def succesful_page_request(url):
    # link is inaccessible if the HTTP response status is not 200

    try:
        req = requests.get(url)
        return req.status_code == 200

    # ConnectionError, HTTPError, Timeout, TooManyRedirects
    except:

        return False

# returns number of internal, external, inaccesable links
def number_of_links(soup, domain_name, url):


    list_urls_internal = []
    list_urls_external = []
    # all external links
    for link in soup.find_all('a', attrs={'href': re.compile("^((http|https)://|/|#)")}):

        # internal link /foo/bar
        if len(link['href']) > 0 and link['href'][0] == '/':
            list_urls_internal.append(domain_name + link['href'][1:])
        # internal link #foo
        elif len(link['href']) > 0 and link['href'][0] == '#':
            list_urls_internal.append(url + link['href'])

        # external link http:// https://
        else:

            parsed_uri = urlparse(link['href'])
            domain_name_link = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

            # if happens that external link actually points on same page
            if domain_name == domain_name_link:
                list_urls_internal.append(link['href'])
            else:
                list_urls_external.append(link['href'])

    # parallel compute because requests take a lot of time
    with Pool() as pool:
        result_internal = pool.map(succesful_page_request, list_urls_internal)
        result_external = pool.map(succesful_page_request, list_urls_external)

    internal_len = sum(result_internal)
    external_len = sum(result_external)
    # inaccessible are all that are false in internal_len in external_len
    inaccessible_len = len(result_external) + len(result_internal) - internal_len - external_len

    return {"internal": internal_len, "external": external_len, "inaccessible": inaccessible_len}

# if page has login page
def has_login(soup):

    # if page has more that one password field on it
    pass_input_len = len(soup.findAll('input', {'type': 'password'}))
    return pass_input_len > 0



