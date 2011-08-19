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
 * Decide if ToS diff engine is in tosWatch or tosGrokr

### Database ###
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
Javascript Runtimes:
 * code.google.com/p/python-spidermonkey/
 * http://www.mozilla.org/rhino/runtime.html

Future Blog Content Ideas:
    Discussing history of law, some background on privacy policies, policy analysis of various new laws/cases/etc..., some background of privacy theory
