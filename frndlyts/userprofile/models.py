from django.db import models
import tosPolicy

class Userprofile(models.Model):
    """
    This model extends the user model via a setting in settings.py. We can put
    any additional user data here.
    """
    favorite_color  = models.CharField()

class FollowedPolicy(models.Model):
    """
    A list of policies a user wishes to be notified upon update of ToS at site.
    """
    userid      = models.ForeignKey(Userprofile)
    policyid    = models.ForeignKey(tosPolicy.PolicyDocument)
