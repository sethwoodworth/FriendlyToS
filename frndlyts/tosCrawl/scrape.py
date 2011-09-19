# Testing lxml and urllib here. 
#
# Have been successful in scraping desired content when a page is retrieved 
# via the lxml.html.parse function. However, I don't know how lxml retrieves
# pages, or if that retreival method can be customized to the level we need,
# including setting the agent string and grabbing cookies. I suspect lxml might
# rely on urllib, but at this point I don't know.
#
# Had some trouble feeding lxml.html.parse the results of urllib.urlopen, but
# most recently I have been successful with the fetchViaUrllib function below.
# For some reason, downloading a page via urllib and feeding either the 
# resulting object or the result's string to parse() or document_fromstring()
# yielded a parsing error before.
#
# Requires lxml - install via http://lxml.de/installation.html#installation or 
# your distro's package manager
#
# .xpath(query) will return a list of lxml.html.HtmlElement
#
# TODO: Proper error handling

# Eventually pull these from the DB
url = 'http://info.yahoo.com/legal/us/yahoo/utos/utos-173.html'
xpathQuery = '/html/body/div/div[4]/div/div/div' 	# Thanks Firebug

    
import lxml.html

def fetchViaLxml(url):
    tosDom = lxml.html.parse(url)
    return tosDom.xpath(xpathQuery)
    
def fetchViaUrllib(url):
    import urllib
    
    # Need to set the agentString, as some sites get snotty with uncommon agents
    class CrawlrURLOpener(urllib.FancyURLopener):
        version = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110613 Firefox/6.0a2"
    urllib._urlopen = CrawlrURLOpener()

    # urllib doesn't play well with https, so make sure we don't connect via 
    # https

    # Retreive and try to build a tree
    try:
        tosDoc = urllib.urlopen(url)
	tosDom = lxml.html.parse(tosDoc)
        tosDoc.close()
	return tosDom.xpath(xpathQuery)
    except IOError as e:
        # Actually long a network error
        print "Something went wrong with the tubes"
