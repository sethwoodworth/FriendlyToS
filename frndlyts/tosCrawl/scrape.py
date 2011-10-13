# Testing lxml and urllib here.
#
# Requires lxml - install via http://lxml.de/installation.html#installation or
# your distro's package manager
#
# .xpath(query) will return a list of lxml.html.HtmlElement
#
# TODO: Proper error handling
#       Check out parser.error_log
#       Put scraped data into the db

# Eventually pull these from the DB
urls = {
    'AOL PP' : 'http://privacy.aol.com/privacy-policy/',
    'AOL ToS' : 'http://legal.aol.com/terms-of-service/full-terms/',
    'Digg PP' : 'http://about.digg.com/privacy',
    'Digg ToS' : 'http://about.digg.com/terms-use',
    'Facebook ToS' : 'http://www.facebook.com/terms.php',
    'Facebook PP' : 'http://www.facebook.com/full_data_use_policy',
    'Google PP' : 'http://www.google.com/intl/en/privacy/privacy-policy.html',
    'Google ToS' : 'http://www.google.com/accounts/TOS?hl=en',
    'Google Desktop' : 'http://desktop.google.com/privacypolicy.html',
    'Google Groups PP' : 'http://groups-beta.google.com/googlegroups/privacy.html',
    'reddit PP' : 'http://www.reddit.com/help/privacypolicy',
    'reddit ToS' : 'http://www.reddit.com/help/useragreement',
    'Safari Books Online PP' : 'http://safaribooksonline.com/Corporate/Index/privacyPolicy.php',
    'Safari Books Online ToS' : 'http://safaribooksonline.com/Corporate/Index/termsUse.php',
    'Twitter PP' : 'https://twitter.com/privacy',
    'Twitter ToS' : 'https://twitter.com/tos',
    'Yahoo' : 'http://info.yahoo.com/legal/us/yahoo/utos/utos-173.html',
    'DuckDuckGo' : 'https://duckduckgo.com/privacy.html',
    'lulz' : 'http://www.thisaddressdoesnexistnewbplanker.com'
    }
xpaths = {
    'AOL PP' : '//*[@id="article"]',
    'AOL ToS' : '//*[@id="article"]',
    'Digg PP' : '/html/body/div[2]/div/div/div',
    'Digg ToS' : '/html/body/div[2]/div/div/div',
    'Google PP' : '//*[@id="aux"]',
    'Google ToS' : '/html/body/table[2]/tbody/tr/td[4]/div',
    'Google Desktop' : '//*[@id="content"]',
    'Google Groups PP' : '/html/body/div/div[2]/div[2]',
    'Facebook ToS' : '/html/body/div[3]/div/div/div[2]/div/div',
    'Facebook PP' : '//*[@id="contentArea"]',
    'reddit PP' : '/html/body/div[3]/div/div[1]',
    'reddit ToS' : '/html/body/div[3]/div/div[1]',
    'Safari Books Online PP' : '//*[@id="mainContent"]',
    'Safari Books Online ToS' : '//*[@id="mainContent"]',
    'Twitter PP' : '/html/body/div[2]/div/div',
    'Twitter ToS' : '/html/body/div[2]/div/div',
    'DuckDuckGo' : '/html/body/div#c/div#t', # maybe wrong or incomplete
    'Yahoo' : '/html/body/div/div[4]/div/div/div'
    }
    # Thanks Firebug


from lxml import html
from MarkdownTranslator import MarkdownTranslator

def isNewVersion(tosDom):
    return True

# Very hacky convience function for development/testing.
def saveMdToDisk(md, filename):
    import os.path, time

    filename = filename.replace(' ', '_') + '_' + time.strftime('%Y%m%d_%H%M')\
        + '.md'

    if os.path.isfile(filename):
        return

    f = open(filename, 'w')
    f.write(md)
    f.close()

def saveHtmlToDisk(doc, filename):
    import os.path, time

    # Filename is augmented with the current datetime.
    filename = filename.replace(' ', '_') + '_' + time.strftime('%Y%m%d_%H%M')\
        + '.html'

    if os.path.isfile(filename):
        return

    # Probably some efficency issues with buffers or what not that 
    # I don't know about.
    f = open(filename, 'w')
    f.write(doc)
    f.close()

def fetchViaUrllib(key):
    """
        Fetches a webpage, saves the page to a file if the fetched page is a
            new version, then searches the webpage for the corresponding
            document element.

        Input: A key for the urls/xpaths directories 
        Output: A HtmlElement representing the element containing the text 
            of interest
        TODO: Probably brake this up eventually. May need to change the order of
            new dom creation, version testing, file writing, etc...
    """
    import urllib

    # Need to set the agentString, as some sites get snotty with uncommon agents
    class CrawlrURLOpener(urllib.FancyURLopener):
        version = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110613 Firefox/6.0a2"

    urllib._urlopen = CrawlrURLOpener()

    # urllib doesn't play well with https, so make sure we don't connect via
    # https

    # Retreive and try to build a tree
    try:
        socket = urllib.urlopen(urls[key])
        tosDoc = socket.read()
        socket.close()
        tosDom = html.fromstring(tosDoc)
        if isNewVersion(tosDom):
            saveHtmlToDisk(tosDoc, key)
        return tosDom.xpath(xpaths[key])
    except IOError as e:
        # Actually long a network error
        print "Something went wrong with the tubes"

def checkDocuments():
    for doc,url in urls.items():
        if doc == 'lulz': continue
        print "Trying " + doc + ".....\t",
        results = fetchViaUrllib(url, xpaths[doc])
        if len(results) == 1: print "Success"
        elif len(results) == 0: print "FAIL"
        else: print "Multiple Results"

# Just for testing things out and cause I'm sick of retying this all the time.
def foo():
    return fetchViaUrllib('Facebook ToS')

def dumbFoo():
    from lxml.html import fromstring
    return fromstring('<div>Hello there <a href="http://www.google.com">Google</a></div>')

def ulFoo():
    from lxml.html import fromstring
    return fromstring('<ul><li>Hi, this is a list</li>\n<li>with <a href="http://www.wbushey.com">AWESOME LINKS!!!</a></li><li>and <span>text spanning many elements</span></li></ul>')

results = foo()
dumbDom = dumbFoo()
ulDom = ulFoo()
t = MarkdownTranslator(True)
