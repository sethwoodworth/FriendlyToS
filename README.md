FriendlyToS
-----------
FriendlyToS is a project to explain Terms of Services in a friendly way to the users of the web.

This is the technical implementation of FriendlyToS and contains four subprojects:
 * FriendlyToS' Django website              ('./frndlyts')
 * Terms of Service monitoring framework    ('./tosWatch')
 * Natural language ToS annotation system   ('./tosGrokr')
 * Web Crawler for ToS'                     ('./tosCrawl')

TODOs
=====
 * research javascript web parsers/scrapers for ease of use
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

Notes & Bookmarks
=================
Python Parsing:
lxml - http://lxml.de/ - looks like a possible solution for building DOMs that can be queried via Xpath. I've had some success retreiving the content I want from a page, but more experimentation is needed.
lxml supports at least three seperate parsers:
 * libxml2 - The default
 * BeautifulSoup - Via lxml.html.ElementSoup
 * html5lib - For parsing HTML 5, via lxml.html.html5parser

There are some functions/methods in Lxml that might be of interest:
 * lxml.html.HtmlElement.interlinks() - Returns (element, attribute, link, pos) for every link in the element
 * lxml.html.diff.htmldiff(doc1, doc2) - A diff function that wraps differences in <ins> and <del> elements
 * lxml.html.diff.html_annotate - Another diff function that behaves like svn blame
 * See http://lxml.de/lxmlhtml.html#html-diff the above two

Javascript Runtimes:

 * https://github.com/davisp/python-spidermonkey/  - Python module based on SpiderMonkey
   * Bug tracking and old code/instructions at http://code.google.com/p/python-spidermonkey/
   * Possible issue: Doesn't provide useful error feedback from Javascript execution
   * Possible issue: Can't call functions defiend in javascript (WTF?? how does it do anything then?)
   * Coolness: Smooth transition of objects to/from Javascript
   * TODO: Install and play around with it.
 * https://developer.mozilla.org/en/SpiderMonkey - C/C++ Javascript runtime
 * http://www.mozilla.org/rhino/ - This is for Java

Future Blog Content Ideas:
    Discussing history of law, some background on privacy policies, policy analysis of various new laws/cases/etc..., some background of privacy theory
