from django.db import models

class ScapeLog(models.Model):
    """
    A log of ToS scraping activities.
    """
    #scrapId        FIXME: What was this supposed to be?
    timestamp       = models.DateTimeField(blank=False) # Time and date of scrape
    machineId       = models.CharField(max_length=30)   # hostname of machine running scraper
    codeId          = models.CharField(max_length=30)   # tag/commit of scraper code
    errorId         = models.CharField(max_length=30)   # error detected by scraper
    errorData       = models.TextField()                # Longer TextField to dump debug info
    isSuccess       = models.BooleanField()             # Does the scraper think it succeeded?

class CrawlQueue(models.Model):
    """
    Sites to be crawled. Probably generated from the organizations table and a priority value.
    """
    url             = models.URLField()                 # May cause errors if verify_exists fails
