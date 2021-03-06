#!/usr/bin/python
# -*- coding:utf8 -*-

# .xpath(query) will return a list of lxml.html.HtmlElement

# Eventually pull the sites directory from the DB

from sites_dict import sites
from lxml import html, etree
from Markdownipy import Markdownipy
from git import *
import codecs
import logging
import hashlib
import os
import re
import subprocess
import urllib2
import urlparse

# Set our Unicode enconding of choice
UNICODE_ENCODING = 'utf-8'

## Define function execution statuses
## 2xx are successful, 3xx are completion with warnings, and 4xx are 
## non-completion with errors
## Question, are 4xx statuses needed, since we have exceptions?

SUCCESS = 200
MD_ALREADY_EXISTS = 310
HTML_ALREADY_EXISTS = 311

# Git Variables
GIT_USER_NAME = "Tos Bot"
GIT_USER_EMAIL = "tosbot@friendlytos.org"
REPO_DIR = "./Docs/"
DOCUMENTS_DIR = REPO_DIR + "documents/"


class UrlNotFound(Exception): pass
class XpathNotFound(Exception): pass

logging.basicConfig(filename='scrape.log', 
                    level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d-%y %H:%M:%S')


git_repo = Repo(REPO_DIR)

def isNewVersion(challengeMd, savedMdPath):

    with codecs.open(savedMdPath, 'r', UNICODE_ENCODING) as f:
        savedMd = f.read()

    lm_savedMd = re.sub(r'\[(.*)\]\(.*\)', r'[\1]()',savedMd)
    lm_challengeMd = re.sub(r'\[(.*)\]\(.*\)', r'[\1]()',challengeMd)
    return gitHash(lm_savedMd) != gitHash(lm_challengeMd)

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
    
def setGitVars():
    global git_stage, git_hct, git_docs_tree, git_html_tree, git_md_tree 

    git_stage = git_repo.index
    git_hct = git_repo.head.commit.tree
    git_docs_tree = git_hct['documents']

setGitVars()

def gitHash(data):
    """
        This function assumes data is unicode
    """
    if not isinstance(data, unicode):
        raise ValueError("Expecting unicode, received " + `type(data)`)

    s = hashlib.sha1()
    data_str = data.encode(UNICODE_ENCODING)
    s.update("blob %u\0" % len(data_str))
    s.update(data_str)
    return s.hexdigest()

def gitAdd(filename):
    """
        Adds the provided filename to the git stage, with attribution to the FriendlyTos Bot.

        Variables that control the repo location and attribution are at the top of the file.
    """
    cmd = ['git', 
            '-c', 'user.name=\'' + GIT_USER_NAME + '\'',
            '-c', 'user.email=\'' + GIT_USER_EMAIL + '\'',
            'add', filename]
    subprocess.check_call(cmd, cwd=REPO_DIR)

def gitCommit(message):
    """
        Commits whatever is currently staged, with attribution to the FriendlyToS Bot.

        Variables that control the repo location and attribution are at the top of the file.
    """
    cmd = ['git',
            '-c', 'user.name=\'' + GIT_USER_NAME + '\'',
            '-c', 'user.email=\'' + GIT_USER_EMAIL + '\'',
            'commit', '-m', message]
    subprocess.check_call(cmd, cwd=REPO_DIR)

def writeMdHtml(filenames, md, html):

        f = codecs.open(filenames[0], 'w', UNICODE_ENCODING)
        f.write(md)
        f.close()

        f = codecs.open(filenames[1], 'w', UNICODE_ENCODING)
        f.write(html)
        f.close()

def fetch(org, doc):
    """
        Fetches a webpage and returns the page as a utf-8 encoded unicode

        Input:  org is the organization/company to retrieve from, as a string
                doc is the document to retrieve, as a string
        Output: A utf-8 unicode containing the fetched page
    """
    if not isinstance(org, str):
        raise ValueError("Expecting str for org, received " + `type(org)`)
    if not isinstance(doc, str):
        raise ValueError("Expecting str for doc, received " + `type(doc)`)
    if not org in sites:
        raise ValueError(org + " was not found in the sites directory")
    if not doc in sites[org]:
        raise ValueError(doc + " was not found in sites['" + org + "']")
        
    # Need to set the agentString, as some sites get snotty with uncommon agents
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    socket = opener.open(sites[org][doc]['url'])

    # Retreive the webpage
    real_url = socket.url
    print "HTTP Code: %(code)d" % {"code": socket.getcode()}
    if socket.code == 404:
        raise UrlNotFound('404: The page  %(url)s could not be found.' % {'url':sites[org][doc]['url']})
    elif socket.code == 403:
        raise UrlNotFound('403: The page %(url)s is forbidden.' % {'url':sites[org][doc]['url']})
    charset = UNICODE_ENCODING
    if socket.headers.getparam('charset'): charset = socket.headers.getparam('charset') 
    tosDoc = socket.read()
    socket.close()

    # Turn it into unicode
    tosDocUni = unicode(tosDoc, charset)

    return (tosDocUni, real_url)

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

# Here for testing, and to be an example as to how to fetch and process a page with legalese
# org is a key in the sites directory (see sites_dict.py)
# doc is a key in the sites[org] directory
# t is an instance of Markdownipy
def fetchAndProcess(org, doc, t):
    try:
        (tosHtml, real_url) = fetch(org, doc)      # Retrieve the string of HTMl that makes up the page

        # For DEBUG, print out the recieved page
        with codecs.open('raw.html', 'w', UNICODE_ENCODING) as f:
            f.write(tosHtml)
        tosDom = html.fromstring(tosHtml, real_url)    # Convert string of HTML into an lxml.html.HtmlElement

        # Rewrite links to be absolute where needed
        def link_repl(href):
            if len(href) == 0 or href[0] == "#" or (len(href) > 6 and href[:6].lower() == 'mailto'):
                return href
            else:
                return urlparse.urljoin(tosDom.base_url, href)
        tosDom.rewrite_links(link_repl)

        # Search for the element that contains text. The result of .xpath() is a list of lxml.html.HtmlElements
        xpathResults = tosDom.xpath(sites[org][doc]['xpath']) 
        
        if len(xpathResults) == 0:
            raise XpathNotFound('The xpath query for ' + org + " : " + doc + ' yielded zero results') 
        divHTML = ''
        for rlt in xpathResults:
            if isinstance(rlt, etree.ElementBase):
                divHTML = divHTML + etree.tostring(rlt, encoding=unicode, method='html')
            else:
                divHTML = divHTML + rlt
        md = t.translate(divHTML)

        if isinstance(md, str):
            md = unicode(md, UNICODE_ENCODING)

        # Interact with git
        # First make sure the organization's folders exist
        #if not os.path.isdir(MD_DIR + org): os.mkdir(MD_DIR + org)
        #if not os.path.isdir(HTML_DIR + org): os.mkdir(HTML_DIR + org)
        if not os.path.isdir(DOCUMENTS_DIR + org): os.mkdir(DOCUMENTS_DIR + org)

        # Then see if the document is new or not
        filenames = [   DOCUMENTS_DIR + org + "/" + doc + ".md",
                        DOCUMENTS_DIR + org + "/" + doc + ".html"]
        gitpaths = [    'documents/' + org + '/' + doc + '.md',
                        'documents/' + org + '/' + doc + '.html']
        if not os.path.exists(filenames[0]) or not os.path.exists(filenames[1]) \
                or not 'documents/' + org in git_docs_tree  \
                or not gitpaths[0] in git_docs_tree[org] or not gitpaths[1] in git_docs_tree[org]:
            # New document
            writeMdHtml(filenames, md, divHTML)
            gitAdd(gitpaths[0])
            gitAdd(gitpaths[1])
            gitCommit("Added " + org + " : " + doc)
            setGitVars()
            print "Added a new document"
        elif isNewVersion(md, filenames[0]): 
            # Existing document that is updated
            writeMdHtml(filenames, md, divHTML)
            gitAdd(gitpaths[0])
            gitAdd(gitpaths[1])
            gitCommit("Updated " + org + " : " + doc)
            setGitVars()
            print "Updated a document"
        else:
            print "No changes"

        return md
    except (UrlNotFound, XpathNotFound) as e:
        logging.warning(e)
    except (IOError) as e:
        logging.error(e)
    except (CalledProcessError) as e:
        logging.error('Command Line Execution\n\tReturn Code:' + e.returncode + '\n\tOutput' + e.output)
    return None

def checkAll(t):
    for org in sites:
        for doc in sites[org]:
            print "Checking " + org + " : " + doc
            md = fetchAndProcess(org, doc, t)
            if md: print "Sucess"
            else: print "Failed"
    

# FIXME: if this can be replaced by the instance in the if name = main, then it should be
t = Markdownipy(True,False)

if __name__=='__main__':
    t = Markdownipy(True,False)
    checkAll(t)
