tosCrawl
--------

Naive crawler that looks for things that seem to be ToS'

 * TODO: decide method of crawl list (Alexa?)

Features:

 * given domain, find ToS'
    find ToS' by url guessing (try sitemap)
    find ToS' by parsing domain front page
 * parse ToS html into a list of paragraphs, to be passed to the analysis engine
 * on fail, save error types and domains (error at find or parse?)
    * feeds "new ToS' status" progress bar in django
    * to start categorizing errors to improve crawler
 * Note/ branch relationship to other entities
    * Self Regulation bodies (IAB, DMA(?), add more)
    * Non-consumer facing data brokers
    * 3rd party trackers (see Ghostery for list)
 * other xml/metadata (P3P)
 * Grab/save cookies (or make note of who provided them)
