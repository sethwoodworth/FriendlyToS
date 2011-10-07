tosGrokr
--------
ToS Grokr is a command line python program to analyze and annotate Terms of Service agreements.

Features
========
 * Named entity detection (should be: YOU, US, 3rd PARTY)
    * Store the list of named entities for further research
 * pull URIs for crawler queue
 * Detect goals/vulnerabilities by use of GOAL WORDS
 * map violations to "principles" (FIPP) and take notice when vulnerability present
 * based on Goal words, detect when a vulnerability was a /required/ disclosure by law
 * detect if statues are referenced (COPPA, HIPAA)
    * detect compliance as best we can

TODOs
=====
* TODO: Create goal words list
* TODO: Create goal/vulnerability list

### Approach
Once I have a goal list with synonyms, I can see how ambigious NP VP(v pp) looks

Discussion on Detecting Safe Harbor
=====
:: Moar text about Section 230 ::  
Which is a reference to the Communications Decency Act, Section 230, aka the Safe Harbor exemption.  This in particular is an important legal citation to highlight, I wonder if there are any papers on auto-magically detecting legal citations via NLP.  If not, we should talk to Robot, Robot and Hwang.

:: Discuss what effect Section 230 has on the internet ::

:: Brief discussion on what it would take to detect the string ""47 U.S.C. S 230(c)(1)" and its variants ::  
Yeah, that would be good to highlight, along with the other Safe Harbor - DMCA. It would be interesting to see if work has happened with detecting legal citations. My initial thought is it wouldn't be that hard to just use regexes, though that can balloon quickly with statues, public laws, rules, federal/state, etc...