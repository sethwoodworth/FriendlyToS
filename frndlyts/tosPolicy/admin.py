from django.contrib import admin
from models import *

admin.site.register(Organization)
admin.site.register(PolicyDocument)
admin.site.register(PolicyVersion)
admin.site.register(PolicyParagraph)
admin.site.register(PolicySentence)
