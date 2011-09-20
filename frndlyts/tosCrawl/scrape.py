# Testing lxml and urllib here. 
#
# Requires lxml - install via http://lxml.de/installation.html#installation or 
# your distro's package manager
#
# .xpath(query) will return a list of lxml.html.HtmlElement
#
# TODO: Proper error handling
#	    Check out parser.error_log
#       Put scraped data into the db

# Eventually pull these from the DB
urls = { 
	'yahoo' : 'http://info.yahoo.com/legal/us/yahoo/utos/utos-173.html',
	'facebook' : 'http://www.facebook.com/terms.php',
	'lulz' : 'http://www.thisaddressdoesnexistnewbplanker.com'
	}
xpaths = {
	'yahoo' : '/html/body/div/div[4]/div/div/div',
	'facebook' : '/html/body/div[3]/div/div/div[2]/div/div'
	}
 	# Thanks Firebug

    
from lxml import html

# Function for testing retrieval via lxml. I think this will be dropped, since
# retrieving via urllib is more flexible in terms of agent string, error/status
# handling, cookies, etc...
def fetchViaLxml(url, xpathQuery):
    tosDom = html.parse(url)
    return tosDom.xpath(xpathQuery)
    
# Function for testing lxml and retrieval via urllib.
def fetchViaUrllib(url, xpathQuery):
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
	tosDom = html.parse(tosDoc)
        tosDoc.close()
	return tosDom.xpath(xpathQuery)
    except IOError as e:
        # Actually long a network error
        print "Something went wrong with the tubes"
