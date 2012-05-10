# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #
# This file is to replicate the response of a database response.
# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #
# TODO: replace this with the database

sites = {
    '500px' : {
        'Privacy Policy' : {'url': 'http://500px.com/privacy',
            'xpath': '//*[@id="terms"]'},
        'Terms of Service' : {'url': 'http://500px.com/terms',
            'xpath': '//*[@id="terms"]'}
    },
    'Amazon': {
	    'Bill of Rights': {'url': 'http://www.amazon.com/gp/help/customer/display.html?nodeId=508092',
		    'xpath': '/html/body/table/tr[1]/td[2]/node()[not(@class="cBox primary")]'},
	    'Conditions of Use': {'url': 'http://www.amazon.com/gp/help/customer/display.html?nodeId=508088',
		    'xpath': '/html/body/table/tr[1]/td[2]/node()[not(@class="cBox primary")]'},
	    'Privacy Notice': {'url': 'http://www.amazon.com/gp/help/customer/display.html?nodeId=468496',
		    'xpath': '/html/body/table/tr[1]/td[2]/span[1]'}
    },
    'AOL': {
        'Privacy Policy': {'url': 'http://privacy.aol.com/privacy-policy/',
            'xpath': '//*[@id="article"]'},
        'Terms of Service': {'url': 'http://legal.aol.com/terms-of-service/full-terms/',
            'xpath': '//*[@id="article"]'}
    },
    'craigslist': {
	    'Privacy Policy': {'url': 'http://www.craigslist.org/about/privacy_policy',
		    'xpath': '/html/body/div/div[2]/div'},
	    'Terms of Use': {'url': 'http://www.craigslist.org/about/terms.of.use',
		    'xpath': '/html/body/blockquote'}
    },
    'Digg': {
        'Privacy Policy': {'url': 'http://about.digg.com/privacy',
            'xpath': '/html/body/div[2]/div/div/div'},
        'Terms of Service': {'url': 'http://about.digg.com/terms-use',
            'xpath': '/html/body/div[2]/div/div/div'}
    },
    'Disney': {
	    'Go Communications Choices': {'url': 'http://corporate.disney.go.com/corporate/pp_communication-choices.html',
		    'xpath': '//*[@id="TERMS"]'},
	    'Go Kids\' Privacy Policy': {'url': 'http://corporate.disney.go.com/corporate/kids.html',
		    'xpath': '//*[@id="TERMS"]'},
	    'Go Notice to California Residents': {'url': 'http://corporate.disney.go.com/corporate/pp_california.html',
		    'xpath': '//*[@id="TERMS"]'},
	    'Go Online Tracking and Advertising': {'url': 'http://corporate.disney.go.com/corporate/pp_online-tracking-advertising.html',
		    'xpath': '//*[@id="TERMS"]'},
	    'Go Privacy Policy': {'url': 'http://corporate.disney.go.com/corporate/pp.html',
		    'xpath': '//*[@id="TERMS"]'},
	    'Go Terms of Use': {'url': 'http://corporate.disney.go.com/corporate/terms.html',
		    'xpath': '//*[@id="TERMS"]'}
    },
    'DuckDuckGo': {
        'Privacy': {'url': 'https://duckduckgo.com/privacy.html',
            'xpath': '//*[@id="content_internal"]'}
    },
    'Facebook': {
        'Privacy Policy': {'url': 'http://www.facebook.com/full_data_use_policy',
            'xpath': '//*[@id="contentArea"]'},
        'Terms of Service': {'url': 'http://www.facebook.com/terms.php',
            'xpath': '/html/body/div[3]/div/div/div/div[2]/div/div'}
    },
    'eBay': {
	    'Privacy Policy': {'url': 'http://pages.ebay.com/help/policies/privacy-policy.html',
		    'xpath': '//div[@class="HelpContent"]/form/div/div[2]'},
	    'User Agreement': {'url': 'http://pages.ebay.com/help/policies/user-agreement.html',
		    'xpath': '//div[@class="HelpContent"]/form/div/div[2]'}
    },
    'Google': {
        'Privacy Policy': {'url': 'http://www.google.com/intl/en/policies/privacy/',
            'xpath': '/html/body/div[3]/div[2]'},
        'Terms of Service': {'url': 'https://www.google.com/intl/en/policies/terms/',
            'xpath': '/html/body/div[3]/div[2]'}
    },
    'LinkedIn': {
	    'Privacy Policy': {'url': 'http://www.linkedin.com/static?key=privacy_policy',
		    'xpath': '/html/body/div[2]/div[2]/div[2]/div'},
	    'User Agreement': {'url': 'http://www.linkedin.com/static?key=user_agreement',
		    'xpath': '/html/body/div[2]/div[2]/div[2]/div'}
    },
    'Microsoft': {
	    'Online Privacy Statement': {'url': 'http://privacy.microsoft.com/en-us/fullnotice.mspx',
		    'xpath': '/html/body/div[2]/div'},
	    'Services Agreement': {'url': 'http://windows.microsoft.com/en-US/windows-live/microsoft-service-agreement',
		    'xpath': '//*[@id="aspnetForm"]'},
        'MSN Privacy Supplement': {'url': 'http://privacy.microsoft.com/en-us/msn.mspx',
		    'xpath': '/html/body/div[2]/div'}
    },
    'MIT': {
        'MITx Terms of Service': {'url': 'https://6002x.mitx.mit.edu/t/tos.html', 
            'xpath': '/html/body/section/div'},
        'MITx Privacy Policy': {'url': 'https://6002x.mitx.mit.edu/t/privacy.html',
            'xpath': '/html/body/section/div'},
        'MITx Copyright': {'url': 'https://6002x.mitx.mit.edu/t/copyright.html',
            'xpath': '/html/body/section/div'},
        'MITx Honor Code': {'url': 'https://6002x.mitx.mit.edu/t/honor.html',
            'xpath': '/html/body/section/div'}
    },
	'msnbc': {
	    'Terms and Conditions': {'url': 'http://www.msnbc.msn.com/id/3303540/ns/about/t/terms-conditions/',
		    'xpath': '/html/body/div[5]/div/div[3]/div[2]/div'}
    },
    'NewEgg': {
        'Terms and Conditions': {'url': 'http://www.newegg.com/Info/AllTermsAndConditions.aspx',
            'xpath': '//*[@id="bcaInfoContainer"]'}
    },
    'Pinterest': {
	    'Acceptable Use Policy': {'url': 'http://pinterest.com/about/use/',
		    'xpath': '//*[@id="legal"]'},
	    'Privacy Policy': {'url': 'http://pinterest.com/about/privacy/',
		    'xpath': '//*[@id="legal"]'},
	    'Terms of Service': {'url': 'http://pinterest.com/about/terms/',
		    'xpath': '//*[@id="legal"]'}
    },
    'reddit': {
        'Privacy Policy': {'url': 'http://www.reddit.com/help/privacypolicy',
            'xpath': '//*[@id="content"]'},
        'Terms of Service': {'url': 'http://www.reddit.com/help/useragreement',
            'xpath': '//*[@id="content"]'}
    },
    'Safari Books Online': {
        'Privacy Policy': {'url': 'http://www.safaribooksonline.com/privacy-policy',
            'xpath': '/html/body/div[3]/div/div/div[3]/div/div/div/div/div/div/div'},
        'Terms of Service': {'url': 'http://www.safaribooksonline.com/terms-service',
            'xpath': '//*[@id="internal_content"]'}
    },
    'Wikimedia': {
	    'Privacy Policy': {'url': 'https://wikimediafoundation.org/wiki/Privacy_policy',
		    'xpath': '//*[@id="mw-content-text"]'},
	    'Terms of Use': {'url': 'http://wikimediafoundation.org/wiki/Terms_of_Use',
		    'xpath': '//*[@id="mw-content-text"]'}
    },
    'Twitter': {
        'Privacy Policy': {'url': 'https://twitter.com/privacy',
            'xpath': '/html/body/div[2]/div/div'},
        'Terms of Service': {'url': 'https://twitter.com/tos',
            'xpath': '/html/body/div[2]/div/div'}
    },
    'Yahoo': {
        'Privacy Policy': {'url': 'http://info.yahoo.com/privacy/us/yahoo/',
            'xpath': '//*[@id="pp-content1"]'},
        'Terms of Service': {'url': 'http://info.yahoo.com/legal/us/yahoo/utos/utos-173.html',
            'xpath': '/html/body/div/div[4]/div/div/div'}
    }
}

