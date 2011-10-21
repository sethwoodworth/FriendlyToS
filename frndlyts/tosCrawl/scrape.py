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

        Input: A key for the urls/xpaths directories 
        Output: A string containing the fetched page
    """
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
        Output: A list of paragraphs, which are themselves lists of sentences.
                Newlines are maintained in the output
    """
    import nltk.data
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    paras = text.splitlines(True)
    for i in xrange(len(paras)):
        paras[i] = sent_tokenizer.tokenize(paras[i])

    return paras

def checkDocuments():
    for doc in sites.keys():
        url = sites[doc]['url']
        if doc == 'lulz': continue
        print "Trying " + doc + ".....\t",
        results = fetchViaUrllib(url, sites[doc]['xpath'])
        if len(results) == 1: print "Success"
        elif len(results) == 0: print "FAIL"
        else: print "Multiple Results"

# Just for testing things out and cause I'm sick of retying this all the time.
def foo():
    global tosDoc
    tosDoc = fetch('Facebook ToS')
    tosDom = html.fromstring(tosDoc)
    return tosDom.xpath(sites['Facebook ToS']['xpath'])

def dumbFoo():
    from lxml.html import fromstring
    return fromstring('<div>Hello there <a href="http://www.google.com">Google</a></div>')

def ulFoo():
    from lxml.html import fromstring
    return fromstring('<ul><li>Hi, this is a list</li>\n<li>with <a href="http://www.wbushey.com">AWESOME LINKS!!!</a></li><li>and <span>text spanning many elements</span></li></ul>')

results = foo()
dumbDom = dumbFoo()
ulDom = ulFoo()
t = MarkdownTranslator(True,True)
