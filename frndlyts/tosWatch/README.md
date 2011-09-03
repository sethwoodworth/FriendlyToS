ToS Watch
---------

ToS Watch, checks Terms of Services for changes.  It is a scraping engine that has "ToS profiles" containing the code needed to parse the ToS' html and translate it into the FriendlyToS db format.

A Python project that calls Javascript to parse html, probably.

Determining if a paragraph from a new version matches a paragraph of the previous version

```
 Compare checksums of policyVersions.  
   If same, no change -> log no change & return
   If different -> compare checksums for each paragraph
     If same, no change
     If different -> log paragraph i changed & add to list of changed paragraphs
   For each paragraph in list of changed paragraphs
     If relative position of new text matches relative position of prevoius text && have X% same content -> same paragraph with new version
 Move forward comments on any paragraphs that are unchanged or have new version
```
