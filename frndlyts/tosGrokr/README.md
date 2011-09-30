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
