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
    'Facebook' : 'http://www.facebook.com/terms.php',
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
    'Facebook' : '/html/body/div[3]/div/div/div[2]/div/div',
    'reddit PP' : '/html/body/div[3]/div/div[1]',
    'reddit ToS' : '/html/body/div[3]/div/div[1]',
    'Safari Books Online PP' : '//*[@id="mainContent"]',
    'Safari Books Online ToS' : '//*[@id="mainContent"]',
    'Twitter PP' : '/html/body/div[2]/div/div',
    'Twitter ToS' : '/html/body/div[2]/div/div',
    'Yahoo' : '/html/body/div/div[4]/div/div/div'
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

def checkDocuments():
    for doc,url in urls.items():
        if doc == 'lulz': continue
        print "Trying " + doc + ".....\t",
        results = fetchViaUrllib(url, xpaths[doc])
        if len(results) == 1: print "Success"
        elif len(results) == 0: print "FAIL"
        else: print "Multiple Results"


# HTML -> Markdown translation functions
# All of these functions, except for the ul and ol functions, assume that the
# provided element does not have child elements.
prepend = ""
translater = dict()

translater['li'] = lambda(el) : "" + el.text_content() + "\n"

def translate_ul(el):
    global prepend
    out = ""
    for child in el.iterchildren():
        out += prepend + " * "
        if child.tag == 'li':
            out += translate(child)
        elif child.tag == 'ul':
            prepend += "  "
            out += translater['ul'](child)
            prepend = prepend[:-2]
        elif child.tag == 'ol':
            prepend += "  "
            out += translater['ol'](child)
            prepend = prepend[:-2]
        else :
            out += translater[child.tag]
    out += "\n"
    el.text = out
    el.drop_tag()
    return el.text_content()

translater['ul'] = translate_ul

def translate_ol(el):
    global prepend
    out = ""
    i = 1
    for child in el.iterchildren():
        out += prepend + `i` + ". "
        i += 1
        if child.tag == 'li':
            out += translate(child)
        elif child.tag == 'ol':
            prepend += "  "
            out += translater['ol'](child)
            prepend = prepend[:-2]
        elif child.tag == 'ul':
            prepend += "  "
            out += translater['ul'](child)
            prepend = prepend[:-2]
    out += "\n"
    return out

translater['ol'] = translate_ol

translater['a'] = lambda(el) : "[" + el.attrib['href'] + "](" + el.text_content() + ")"

translater['br'] = lambda(el) : "\n\n"

# <p> and <div> are the samething for this transpation
translater['p'] = lambda(el) : el.text_content() + "\n\n"
translater['div'] = translater['p']

translater['span'] = lambda(el) : el.text_content()

# <b> and <strong> are the same
translater['b'] = lambda(el) : "**" + el.text_content() + "**"
translater['strong'] = translater['b']

# <i> and <em> are the same
translater['i'] = lambda(el) : "*" + el.text_content() + "*"
translater['em'] = translater['i']

translater['img'] = lambda(el) : "![" + el.attrib['alt'] + "](" + el.attrib['src'] + ")"

translater['h1'] = lambda(el) : "#" + el.text_content() + "#"
translater['h2'] = lambda(el) : "##" + el.text_content() + "##"
translater['h3'] = lambda(el) : "###" + el.text_content() + "###"
translater['h4'] = lambda(el) : "####" + el.text_content() + "####"
translater['h5'] = lambda(el) : "#####" + el.text_content() + "#####"
translater['h6'] = lambda(el) : "######" + el.text_content() + "######"

# Probably need to add more to the <pre> function
translater['pre'] = lambda(el) : el.text_content().replace("\n", " ") + "\n\n"

# / Translater functions

# Function called by others to translate an lxml.html.HTMLElement into a string
# of Markdown
def translate(el):
    print prepend + "Tag " + el.tag 
    print prepend + "Number of children: " + `len(el)`
    out = ""
    if el.tag == 'ol' : return translater['ol'](el)
    elif el.tag == 'ul' : return translater['ul'](el)
    else :
        for child in el.iterchildren():
            print prepend + "Child tag: " + child.tag
            child.text = translate(child)
            child.drop_tag()
        if len(el) == 0 : 
            print prepend + "calling '" + el.tag + "' translater"
            return translater[el.tag](el)
    return el.text_content()

# Just for testing things out and cause I'm sick of retying this all the time.
def foo():
    return fetchViaUrllib(urls['Facebook'], xpaths['Facebook'])

def dumbFoo():
    from lxml.html import fromstring
    return fromstring('<div>Hello there <a href="http://www.google.com">Google</a></div>')

def ulFoo():
    from lxml.html import fromstring
    return fromstring('<ul><li>Hi, this is a list</li><li>with <a href="http://www.wbushey.com">AWESOME LINKS!!!</a></li><li>and <span>text spanning many elements</span></li></ul>')


results = foo()
dumbDom = dumbFoo()
ulDom = ulFoo()
