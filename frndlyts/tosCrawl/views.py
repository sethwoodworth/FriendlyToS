import datetime
import hashlib
from tosPolicy.models import Organization, PolicyDocument
from tosPolicy.models import PolicyVersion, PolicyParagraph, PolicySentence

def store_tos(org, policy, document):
    """
    unique_together: paragraph, and nonce_pkey
    This method will not create a new Organization nor PolicyDocument.
    """
    print org, policy, document
    # $document must be a list(document), containing list(paragraphs), containing sentences
    if not isinstance(document, list) or \
            not isinstance(document[0], list) or \
            not isinstance(document[0][0], str):
        raise Exception('Document data is not in the expected list format', document)
    else:
        print "Ok, the data looks good. Let's continue"

    doc_hash = hashlib.md5(str(document)).hexdigest()
    print "document hash: %s" % (doc_hash)
    currentPolicyVersion = PolicyVersion.objects.filter(checkSum=doc_hash).all()[0]

    # if the document hashes are unchanged, no new policy version need be created
    if doc_hash == currentPolicyVersion.checkSum:
        # break the flow, and return a success
        return 'Success: Document unchanged, carry on.'

    # Since the hashes are different, we need to create a new PolicyVersion
    pv = PolicyVersion()
    pv.docid = currentPolicyVersion # make reference to the last version of the policy
    pv.dateAdded = datetime.datetime.now()
    pv.checkSum = doc_hash # we already calculated this
    pv.save()
    print "created a new PolicyVersion"

    # now for each paragraph we will need to create another structure
    for paragraph in document:
        # TODO: find ancestor paragraph via search
        p = PolicyParagraph()
        p.versionId = pv # the new PolicyVersion we just created
        try:
            p.previous = prev_p
        except:
            pass
        p.checkSum = hashlib.md5(str(paragraph)).hexdigest()
        p.save()
        print "created a new PolicyParagraph"
        for sentence in paragraph:
            s = PolicySentence()
            s.paragraphId = p
            try:
                s.previous = prev_s
            except:
                pass
            s.text = sentence
            s.checkSum = hashlib.md5(str(sentence)).hexdigest()
            s.save()
            print "created a new PolicySentence"
            prev_s = s # store last iteration's sentence for making a fkey to
        prev_p = p # store last loop's paragraph for making a fkey to


document = [ 
                ['This agreement was written in English (US).', 'To the extent any translated version of this agreement conflicts with the English version, the English version controls.', 'Please note that Section 16 contains certain changes to the general terms for users outside the United States.'],
                ['Date of Last Revision: April 26, 2011.'],
                ['Statement of Rights and Responsibilities'],
                ['This Statement of Rights and Responsibilities (Statement) derives from the Facebook Principles, and governs our relationship with users and others who interact with Facebook.', 'By using or accessing Facebook, you agree to this Statement.'],
                ['Privacy'],
                ['Your privacy is very important to us.'],
                ['We designed our Privacy Policy to make important disclosures about how you can use Facebook to share with others and how we collect and can use your content and information.']
            ]

def test_store():
    """
    use this to test and debug the storage process with some example variables
    """
    org = Organization.objects.filter(name="Facebook llc.").all()[0]
    p   = PolicyDocument.objects.filter(title="Statement of Rights and Responsibilities").all()[0]
    document.append(['Sharing Your Content and Information'])
    store_tos(org, p, document)


def test_tables():
    o = Organization()
    o.name          = "Facebook llc."
    o.url           = 'http://www.facebook.com/'
    o.created_at    = datetime.datetime.now()
    o.save()
    print "Org... saved"
    pd              = PolicyDocument()
    pd.orgid        = o
    pd.title        = 'Statement of Rights and Responsibilities'
    pd.url          = 'http://www.facebook.com/terms.php'
    pd.documentPath = '/html/body/div[3]/div/div/div[2]/div/div'
    pd.save()
    print "Document... saved"
    pv              = PolicyVersion()
    pv.docid        = pd
    pv.dateAdded    = datetime.datetime.now()
    pv.checkSum     = hashlib.md5(str(document)).hexdigest()
    pv.save()
    print "Version... saved"
    #store_tos(o, pd, document)
    return o, pd, pv, document
