from django.db import models

class Organization(models.Model):
    """
    Base model for a website.
    """
    name        = models.CharField(max_length=50)
    url         = models.URLField()                 # Org's main operating URL
    created_at  = models.DateTimeField()            # time and date org was added to this list

class PolicyDocument(models.Model):
    """
    Policy Document. Can be many documents per organization.
    """
    orgid           = models.ForeignKey('Organization')
    documentPath    = models.CharField(max_length=255)      # this might just be a textfield
    title           = models.CharField(max_length=100)      # What the org calls this document (privacy policy, terms of service, other)
    url         = models.URLField()                         # current full URL to the policy

class PolicyVersion(models.Model):
    """
    Each recorded revision of a Policy document.
    """
    docid           = models.ForeignKey('PolicyDocument')
    # I think we can get by following fkeys backwards, don't need bidirectional fkeys
    #firstParagraph  = models.ForeignKey('PolicyParagraph')
    dateAdded       = models.DateTimeField()                # when we saw/saved the policy update
    # TODO: checkSum MUST be unique, what are we doing here?
    checkSum        = models.CharField(max_length=100, unique=True)      # longer than we need

class PolicyParagraph(models.Model):
    """
    Each paragraph of the policy.
    """
    versionId       = models.ForeignKey('PolicyVersion')
    # previous is the prev paragraph as you read the document
    # null and blank if first paragraph
    previous        = models.ForeignKey('PolicyParagraph', null=True, related_name="Previous Paragraph")
    # ancestor is the last revision of the paragraph
    # previous null and blank if first PolicyVersion of PolicyDocument
    ancestor        = models.ForeignKey('PolicyParagraph', null=True, blank=True)
    checkSum        = models.CharField(max_length=100)      # longer than we need

class PolicySentence(models.Model):
    """
    Store each sentence of the policy, with references to PolicyVersion.
    """
    paragraphId     = models.ForeignKey('PolicyParagraph')  # must be owned by a Paragraph
    previous        = models.ForeignKey('PolicySentence', null=True, blank=True)
    text            = models.TextField()                    # The actual content! (finally)
    checkSum        = models.CharField(max_length=100)      # longer than we need

