from django.db import models

# Model made for caching urls
class UrlModel(models.Model):

    '''
    created - time of creation, used to recache if over 24 hours

    url - url of scraped page
    html_version - describes html version of scraped page
    title - describes title of scraped page
    h1-h6 - number of certain headings of scraped page
    internal - number of internal links of scraped page
    external - nubmer of external links of scraped page
    inaccessible - number of inaccessible links of scraped page
    has_login_form - determines if scraped page has loginform
    '''

    created = models.DateTimeField(auto_now_add=True)

    url = models.URLField()
    html_version = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    h1 = models.IntegerField()
    h2 = models.IntegerField()
    h3 = models.IntegerField()
    h4 = models.IntegerField()
    h5 = models.IntegerField()
    h6 = models.IntegerField()
    internal = models.IntegerField()
    external = models.IntegerField()
    inaccessible = models.IntegerField()
    has_login_form = models.BooleanField()
