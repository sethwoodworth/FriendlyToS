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
translate = dict()

translate['li'] = lambda(el) : "" + el.text_content() + "\n"

def translate_ul(el, prepend=""):
    out = ""
    for child in el.iter():
        out += prepend + " * "
        if child.tag == 'li':
            out += translate['li'](child)
        elif child.tag == 'ul':
            out += translate['ul'](child, prepend + "  ")
        elif child.tag == 'ol':
            out += translate['ol'](child, prepend + "  ")
        else :
            out += translate[child.tag]
    out += "\n"
    return out

def translate_ol(el, prepend=""):
    out = ""
    i = 1
    for child in el.iter():
        out += prepend + i + ". "
        i += 1
        if child.tag == 'li':
            out += translate['li'](child)
        elif child.tag == 'ol':
            out += translate['ol'](child, prepend + "  ")
        elif child.tag == 'ul':
            out += translate['ul'](child, prepend + "  ")
    out += "\n"
    return out

translate['ol'] = translate_ol

translate['a'] = lambda(el) : "[" + el.attrib['href'] + "](" + el.text_content() + ")"

translate['br'] = lambda(el) : "\n\n"

# <p> and <div> are the samething for this transpation
translate['p'] = lambda(el) : el.text_content() + "\n\n"
translate['div'] = translate['p']

translate['span'] = lambda(el) : el.text_content()

# <b> and <strong> are the same
translate['b'] = lambda(el) : "**" + el.text_content() + "**"
translate['strong'] = translate['b']

# <i> and <em> are the same
translate['i'] = lambda(el) : "*" + el.text_content() + "*"
translate['em'] = translate['i']

translate['img'] = lambda(el) : "![" + el.attrib['alt'] + "](" + el.attrib['src'] + ")"

translate['h1'] = lambda(el) : "#" + el.text_content() + "#"
translate['h2'] = lambda(el) : "##" + el.text_content() + "##"
translate['h3'] = lambda(el) : "###" + el.text_content() + "###"
translate['h4'] = lambda(el) : "####" + el.text_content() + "####"
translate['h5'] = lambda(el) : "#####" + el.text_content() + "#####"
translate['h6'] = lambda(el) : "######" + el.text_content() + "######"

# Probably need to add more to the <pre> function
translate['pre'] = lambda(el) : el.text_content().replace("\n", " ") + "\n\n"

# / Translate functions

# Function called by others to translate an lxml.html.HTMLElement into a string
# of Markdown
def translate(el):
    print "Tag " + el.tag 
    out = ""
    if el.tag == 'ol' : return translate['ol'](el)
    elif el.tag == 'ul' : return translate['ul'](el)
    elif len(el) == 0 : return translate[child.tag](el)
    for child in el.iter():
        child.text = translate(child)
        child.drop_tag()
    return el.text_content()

# Just for testing things out and cause I'm sick of retying this all the time.
def foo():
    return fetchViaUrllib(urls['Facebook'], xpaths['Facebook'])

def dumbFoo():
    from lxml.html import fromstring
    return fromstring('<div>Hello there <a href="http://www.google.com">Google</a></div>')


results = foo()
dumbDom = dumbFoo()
