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
from lxml import html, etree
from MarkdownTranslator import MarkdownTranslator
import codecs

# Set our Unicode enconding of choice
UNICODE_ENCODING = 'utf-8'

## Define function execution statuses
## 2xx are successful, 3xx are completion with warnings, and 4xx are 
## non-completion with errors
## Question, are 4xx statuses needed, since we have exceptions?

SUCCESS = 200
MD_ALREADY_EXISTS = 310
HTML_ALREADY_EXISTS = 311

def isNewVersion(tosDom):
    return True

def getCurrentDatetime():
    """
        Returns the current datetime as a string, in the Ymd_HM format.

        Output: A string representing the current datetime
    """
    import time
    return time.strftime('%Y%m%d_%H%M')

def saveMdToDisk(md, filenameBase, datetime):
    """
        Saves the passed Markdown string to a file named in the following 
        format: filenameBase_datetime.md

        Files will be saved using the Unicode Encoding specified by 
        UNICODE_ENCODING
        
        If a  file already exists with the filename base and datetime provided,
        nothing will be written to disk, and the function will return an 
        MD_ALREADY_EXISTS status.

        Input: 
            md: A unicode containing the Markdown representation of a document's
                text
            filenameBase: A string containing the base of the document's
                filename
            datetime: A string containing the datetime that will be used for 
                the document's file
        
        Output: An integer representing a function execution status
    """
    # Type checking
    if not isinstance(md, unicode):
        raise ValueError("Expecting md to be unicode, received " \
                        + `type(md)`)
    if not isinstance(filenameBase, str):
        raise ValueError("Expecting filenameBase to be str, received " \
                        + `type(filenameBase)`)
    if not isinstance(datetime, str):
        raise ValueError("Expecting datetime to be str, received " \
                        + `type(datetime)`)


    import os.path

    # Construct final filename
    filename = filenameBase.replace(' ', '_') + '_' + datetime + '.md'

    if os.path.isfile(filename):
        return MD_ALREADY_EXISTS

    f = codecs.open(filename, 'w', UNICODE_ENCODING)
    f.write(md)
    f.close()

    return SUCCESS

def saveHtmlToDisk(html, filenameBase, datetime):
    """
        Saves the passed HTML string to a file named in the following 
        format: filenameBase_datetime.md
        
        Files will be saved using the Unicode Encoding specified by 
        UNICODE_ENCODING

        If a  file already exists with the filename base and datetime provided,
        nothing will be written to disk, and the function will return an 
        HTML_ALREADY_EXISTS status.

        Input: 
            html: A string containing the HTML representation of a document's
                text
            filenameBase: A string containing the base of the document's
                filename
            datetime: A string containing the datetime that will be used for 
                the document's file
        
        Output: An integer representing a function execution status
    """
    # Type checking
    if not isinstance(html, unicode):
        raise ValueError("Expecting html to be unicode, received " \
                        + `type(html)`)
    if not isinstance(filenameBase, str):
        raise ValueError("Expecting filenameBase to be str, received " \
                        + `type(filenameBase)`)
    if not isinstance(datetime, str):
        raise ValueError("Expecting datetime to be str, received " \
                        + `type(datetime)`)


    import os.path

    # Construct final filename
    filename = filenameBase.replace(' ', '_') + '_' + datetime + '.html'

    if os.path.isfile(filename):
        return HTML_ALREADY_EXISTS

    # Probably some efficency issues with buffers or what not that 
    # I don't know about.
    f = codecs.open(filename, 'w', UNICODE_ENCODING)
    f.write(html)
    f.close()

    return SUCCESS

def saveTestCase(tosDoc, md, filename):

    fileTime = getCurrentDatetime()
    folder = './samples/'
    filename = folder + filename

    saveMdToDisk(md, filename, fileTime)
    saveHtmlToDisk(tosDoc, filename, fileTime)

    return SUCCESS

def fetch(key):
    """
        Fetches a webpage and returns the page as a utf-8 encoded unicode

        Input: A string that is a key in the sites directory 
        Output: A utf-8 unicode containing the fetched page
    """
    if not isinstance(key, str):
        raise ValueError("Expecting str, received " + `type(key)`)
    if not key in sites:
        raise ValueError(key + " was not found in the sites directory")
        
    import urllib

    # Need to set the agentString, as some sites get snotty with uncommon agents
    class CrawlrURLOpener(urllib.FancyURLopener):
        version = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1042.0 Safari/535.21"

    urllib._urlopen = CrawlrURLOpener()

    # urllib doesn't play well with https, so make sure we don't connect via
    # https

    # Retreive and return the webpage
    try:
        socket = urllib.urlopen(sites[key]['url'])
        tosDoc = socket.read()
        socket.close()
        return unicode(tosDoc, UNICODE_ENCODING)
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
# k is a key in the sites directory (see sites_dict.py)
# t is an instance of a MarkdownTranslator
def fetchAndProcess(k, t):
    global tosDoc
    tosHtml = fetch(k)      # Retrieve the string of HTMl that makes up the page
    print "tosHtml type is " + `type(tosHtml)`
    f = codecs.open('raw_html.html','w',UNICODE_ENCODING)
    f.write(tosHtml)
    f.close()
    tosDom = html.fromstring(tosHtml)    # Convert string of HTML into an lxml.html.HtmlElement
    xpathResults = tosDom.xpath(sites[k]['xpath']) # Search for the element that contains text. The result of .xpath() is a list of lxml.html.HtmlElements
    # Ideally, there will only be one element that matches our xpath query. Thus, xpathResults should only have one element.
    divHTML = etree.tostring(xpathResults[0], encoding=unicode, method='html')
    # Now escape some characters that mean something to Markdown.
    md = t.translate(html.fromstring(divHTML))
    if isinstance(md, str):
        md = unicode(md, UNICODE_ENCODING)
    saveTestCase(divHTML, md, k)
    return md


dumbDom = dumbFoo()
ulDom = ulFoo()
t = MarkdownTranslator(True,True)
