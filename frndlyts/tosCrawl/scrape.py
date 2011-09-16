# Some pretty nasty webpage retrevial going on up in here
# TODO: Some error handling
import urllib

# Need to set the agentString, as some sites get snotty with uncommon agents
class CrawlrURLOpener(urllib.FancyURLopener):
    version = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110613 Firefox/6.0a2"
urllib._urlopen = CrawlrURLOpener()

# Eventually pull this from the DB
url = "http://www.facebook.com/full_data_use_policy"

# urllib doesn't play well with https, so make sure we don't connect via https

# Retreive and read
document = urllib.urlopen(url)
for line in document:
    print line

document.close()

