# Testing lxml and urllib here.
#
# Requires lxml - install via http://lxml.de/installation.html#installation or
# your distro's package manager
#
# Requires nltk and and punkt via nltk.download()
#
# .xpath(query) will return a list of lxml.html.HtmlElement
#
# TODO: Proper error handling
#       Check out parser.error_log
#       Put scraped data into the db

# Eventually pull these from the DB

from sites_dict import sites
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
    f.write(md.encode('utf8'))
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

def saveTestCase(tosDoc, md, filename):
    import time

    fileTime = time.strftime('%Y%m%d_%H%M')
    folder = './samples/'
    filename = folder + filename.replace(' ', '_') + '_' + fileTime

    f = open(filename + '.html', 'w')
    f.write(tosDoc)
    f.close()

    f = open(filename + '.md', 'w')
    f.write(md.encode('utf8'))
    f.close()

def fetch(key):
    """
        Fetches a webpage and returns the page as a string

        Input: A string that is a key in the sites directory 
        Output: A string containing the fetched page
    """
    if not isinstance(key, str):
        raise ValueError("Expecting str")
    if not key in sites:
        raise ValueError(key + " was not found in the sites directory")
        
    import urllib

    # Need to set the agentString, as some sites get snotty with uncommon agents
    class CrawlrURLOpener(urllib.FancyURLopener):
        version = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110613 Firefox/6.0a2"

    urllib._urlopen = CrawlrURLOpener()

    # urllib doesn't play well with https, so make sure we don't connect via
    # https

    # Retreive and return the webpage
    try:
        socket = urllib.urlopen(sites[key]['url'])
        tosDoc = socket.read()
        socket.close()
        return tosDoc
    except IOError as e:
        # TODO: Actually log a network error
        print "Something went wrong with the tubes"

def listify(text):
    """
        Input: A string of text
        Output: A list of lists of strings. Each element of the root list
                represents a paragraph. Each element of the sub lists 
                represents a sentence.
                Newlines are maintained in the output
    """

    if not isinstance(text, str):
        raise ValueError("Expecting str")
    
    import nltk.data
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    paras = text.splitlines(True)
    for i in xrange(len(paras)):
        paras[i] = sent_tokenizer.tokenize(paras[i])

    return paras

# Bad/hacky method for checking if our xpaths are working.
def checkDocuments():
    for doc in sites.keys():
        url = sites[doc]['url']
        if doc == 'lulz': continue
        print "Trying " + doc + ".....\t",
        results = fetchViaUrllib(url, sites[doc]['xpath'])
        if len(results) == 1: print "Success"
        elif len(results) == 0: print "FAIL"
        else: print "Multiple Results"

def dumbFoo():
    from lxml.html import fromstring
    return fromstring('<div>Hello there <a href="http://www.google.com">Google</a></div>')

def ulFoo():
    from lxml.html import fromstring
    return fromstring('<ul><li>Hi, this is a list</li>\n<li>with <a href="http://www.wbushey.com">AWESOME LINKS!!!</a></li><li>and <span>text spanning many elements</span></li></ul>')

# Here for testing, and to be an example as to how to fetch and process a page with legalese
def facebookExample(t):
    global tosDoc
    tosDoc = fetch('Facebook ToS')      # Retrieve the string of HTMl that makes up the page
    tosDom = html.fromstring(tosDoc)    # Convert string of HTML into an lxml.html.HtmlElement
    xpathResults = tosDom.xpath(sites['Facebook ToS']['xpath']) # Search for the element that contains text. The result of .xpath() is a list of lxml.html.HtmlElements
    # Ideally, there will only be one element that matches our xpath query. Thus, xpathResults should only have one element.
    md = t.translate(xpathResults[0])   # Use the MarkdownTranslator to convert the text of the found element into Markdown.
    return md


dumbDom = dumbFoo()
ulDom = ulFoo()
t = MarkdownTranslator(True,True)
facebookMd = facebookExample(t)
