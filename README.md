FriendlyToS
-----------
FriendlyToS is a project to explain Terms of Services in a friendly way to the users of the web.

This is the technical implementation of FriendlyToS and contains four subprojects:
 * HTML and MD of ToSes being monitored     ('./documents')
 * FriendlyToS' Django website              ('./frndlyts')
 * Terms of Service monitoring framework    ('./tosWatch')
 * Natural language ToS annotation system   ('./tosGrokr')
 * Web Crawler for ToS'                     ('./tosCrawl')

TODOs
=====
 * create Goal words list from Anton, Veil, &etc for parsing
   * pg. 14 of Anton & Earp
   * (i.e. TRACK, AGGREGATE, PROVIDE)
 * Pull goal/vulnerability descriptions from Anton & Earp
   * type up in spreadsheet with extra fields of metadata
   * (i.e. "PREVENT use of cookies to send spam")
 * Initial Crawl list (source ToSBACK)
   * Source for list of trackers: Ghostery
 * Decide if ToS diff engine is in tosWatch or tosGrokr
 * Decide when a paragraph has changed enough to be considered a different paragraph instead of merly a revision of a paragraph.
 * Decide if and how comments on a paragraph will relate to later versions of that paragraph.

### Installation Requirements ###
 * OS packages
   * python-lxml
     * *or* libxml2-dev and libxslt1-dev plus lxml in requirements.txt (haven't tried this yet)
   * git
 * Python
    * Use requirements.txt
    * nltk punkt
      * Use nltk.download() in an interactive session to download the punkt package
 

### Database ###
Database diagram at https://cacoo.com/diagrams/DFHkFqrvdvr863xi

TODO: finish db schema (draft 1)
TODO: decide what tool implements database schema
TODO: research South for db migrations

    Paragraph
        key > prev Paragarph
        key > next Paragraph
        fk > first Sentence
        fk > prev revision of paragraph;
        key > version
    Sentence
        fk > parent Setence
        key > prev Paragarph
        key > next Sentence
    Comments
        fkey > user
        fkey > paragraph_id

### Logging ###
Use <a href="https://docs.djangoproject.com/en/1.3/topics/logging/">Django's logging</a>, which is basically just <a href="http://docs.python.org/library/logging.html">Python's logging</a> with a couple of added methods.

Django and Python both do not provide a handler for logging to a database, so we'll need to write that.

Need to define log formats and the <a href="https://docs.djangoproject.com/en/1.3/topics/logging/#configuring-logging">dictConfig</a>

We should define what happens for each log level, and when they are used in FriendlyToS:

 * critical - use DB and AdminEmailHandler handlers
 * error - use DB handler
 * warning - use DB handler
 * info - use DB handler
 * debug - ???

Should filter for DB messages and send those to a file.

Notes & Bookmarks
=================
[Pro Bono Privacy Initiative](https://www.privacyassociation.org/publications/pro_bono_privacy_initiative_pilot_gets_underway) - Provides data privacy expertise to non-profits

Python Parsing:
lxml - http://lxml.de/ - looks like a possible solution for building DOMs that can be queried via Xpath. I've had some success retreiving the content I want from a page, but more experimentation is needed.

lxml supports at least three seperate parsers:

 * libxml2 - The default
 * BeautifulSoup - Via lxml.html.ElementSoup
 * html5lib - For parsing HTML 5, via lxml.html.html5parser

There are some functions/methods in Lxml that might be of interest:

 * lxml.html.HtmlElement.interlinks() - Returns (element, attribute, link, pos) for every link in the element
 * lxml.html.diff.htmldiff(doc1, doc2) - A diff function that wraps differences in \<ins\> and \<del\> elements
 * lxml.html.diff.html_annotate - Another diff function that behaves like svn blame
 * See http://lxml.de/lxmlhtml.html#html-diff for the above two

Python Markdown Reading:
[python-markdown2](https://github.com/trentm/python-markdown2)

**Python and Git**
[GitPython](https://github.com/gitpython-developers/GitPython) - Python library for interacting with git repos


**Thoughts on Scraping**

Default lxml seems to work on the few sites tried so far. However, it  might be a good idea to support multiple forms of scraping. Lxml includes three parsers (default, BeautifulSoup, HTML5). Regexs could be a fallback. BTE is a potential last result.

Dumping content into the database: convert \<div\>, \<span\>, \<p\>, \<hX\>, \<tr\>, &nbsp into paragraphs in the table. Will have to split \<pre\> on newlines. Will we keep the formatting of lists? And will we keep links? 

**Thoughts on Errors in Scraping**

Should log IOErrors when they are thrown. 

A message should be generated when a urlopen results in some error response (4xx). The message should include the url attempted, the error returned, and the timestamp of the attempt.

A message (ScrapeError ?) should be generated when html.parse returns an empty list, as we can assume that the xpath query in the database has successfully tested before. The generated message should include a timestamp of when the scrape was attempted, the last-modified header from the response, the url called, and the xpath query attempted.

**Javascript Runtimes**

 * https://github.com/davisp/python-spidermonkey/  - Python module based on SpiderMonkey
   * Bug tracking and old code/instructions at http://code.google.com/p/python-spidermonkey/
   * Possible issue: Doesn't provide useful error feedback from Javascript execution
   * Possible issue: Can't call functions defiend in javascript (WTF?? how does it do anything then?)
   * Coolness: Smooth transition of objects to/from Javascript
   * TODO: Install and play around with it.
 * https://developer.mozilla.org/en/SpiderMonkey - C/C++ Javascript runtime
 * http://www.mozilla.org/rhino/ - This is for Java

**Future Blog Content Ideas**

Discussing history of law, some background on privacy policies, policy analysis of various new laws/cases/etc..., some background of privacy theory


**Important Laws and Statutes**

 * Communications Decency Act
 * DMCA
 * Video Privacy Protection Act

**Interesting or Related Projects**

* [Collusion](http://collusion.toolness.org/) - Firefox plugin that lets you see connections between trackers you have encountered.
* [Privacy Score](http://privacyscore.com/) - As of 3/5/2012, scores 1600+ websites based on how risky a privacy policy is to a user.
* [OpenCalais](http://www.opencalais.com/about) - Semantic analysis and linking service provided for free by Thomson Reuters.
* [WikiSummary](http://www.wikisummaries.org/index.php?title=Special%3ASearch&search=terms&go=Go) - WikiSummary created summaries of a handful of ToSes five years ago.

**Academic References**

* [Barth - Design and analysis of privacy policies (Dissertation)](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.167.8017&rep=rep1&type=pdf)
* Anton - A Requirements taxonomy for reducing web site privacy vulnerabilities
* [Anton - A taxonomy for web site privacy requirements](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.67.8001&rep=rep1&type=pdf)
* [FTC - Privacy Online: Fair information practices in the marketplace](http://www.ftc.gov/reports/privacy2000/privacy2000.pdf)
* [Schwaig - Compliance to the fair information practices: How are the Fortune 500 handling online privacy disclosures?](http://www.profkane.com/uploads/7/9/1/3/79137/schwaig_compliance-to-the-fair-information-practices-how-are-the-fortune-500-handling-online-privacy-disclosures_2006.pdf)
* [Vail - An empirical study of consumer perceptions and comprehension of web site privacy policies](http://www.truststc.org/wise/articles2009/article1.pdf)
* Williams - Internet Privacy Policies: A composite index for measuring compliance to the fair information principles
