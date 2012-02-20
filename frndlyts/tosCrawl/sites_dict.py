# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #
# This file is to replicate the response of a database response.
# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- #
# TODO: replace this with the database

sites = {
    'AOL PP': {'url': 'http://privacy.aol.com/privacy-policy/',
        'xpath': '//*[@id="article"]'},
    'AOL ToS': {'url': 'http://legal.aol.com/terms-of-service/full-terms/',
        'xpath': '//*[@id="article"]'},
    'Digg PP': {'url': 'http://about.digg.com/privacy',
        'xpath': '/html/body/div[2]/div/div/div'},
    'Digg ToS': {'url': 'http://about.digg.com/terms-use',
        'xpath': '/html/body/div[2]/div/div/div'},
    'DuckDuckGo': {'url': 'https://duckduckgo.com/privacy.html',
        'xpath': '/html/body/div#c/div#t'},
    'Facebook PP': {'url': 'http://www.facebook.com/full_data_use_policy',
        'xpath': '//*[@id="contentArea"]'},
    'Facebook ToS': {'url': 'http://www.facebook.com/terms.php',
        'xpath': '/html/body/div[3]/div/div/div[2]/div/div'},
    'Google Desktop': {'url': 'http://desktop.google.com/privacypolicy.html',
        'xpath': '//*[@id="content"]'},
    'Google Groups PP': {'url': 'http://groups-beta.google.com/googlegroups/privacy.html',
        'xpath': '/html/body/div/div[2]/div[2]'},
    'Google PP': {'url': 'http://www.google.com/intl/en/privacy/privacy-policy.html',
        'xpath': '//*[@id="aux"]'},
    'Google ToS': {'url': 'http://www.google.com/accounts/TOS?hl=en',
        'xpath': '/html/body/table[2]/tbody/tr/td[4]/div'},
    'MITx ToS': {'url': 'https://6002x.mitx.mit.edu/t/tos.html', 
        'xpath': '/html/body/section.tos/div'},
    'MITx PP': {'url': 'https://6002x.mitx.mit.edu/t/privacy.html',
        'xpath': '/html/body/section.privacy-policy/div'},
    'MITx Copyright': {'url': 'https://6002x.mitx.mit.edu/t/copyright.html',
        'xpath': '/html/body/section.copyright/div'},
    'MITx Honor Code': {'url': 'https://6002x.mitx.mit.edu/t/honor.html',
        'xpath': '/html/body/section.honor-code/div'},
    'Safari Books Online PP': {'url': 'http://safaribooksonline.com/Corporate/Index/privacyPolicy.php',
        'xpath': '//*[@id="mainContent"]'},
    'Safari Books Online ToS': {'url': 'http://safaribooksonline.com/Corporate/Index/termsUse.php',
        'xpath': '//*[@id="mainContent"]'},
    'Twitter PP': {'url': 'https://twitter.com/privacy',
        'xpath': '/html/body/div[2]/div/div'},
    'Twitter ToS': {'url': 'https://twitter.com/tos',
        'xpath': '/html/body/div[2]/div/div'},
    'Yahoo': {'url': 'http://info.yahoo.com/legal/us/yahoo/utos/utos-173.html',
        'xpath': '/html/body/div/div[4]/div/div/div'},
    'reddit PP': {'url': 'http://www.reddit.com/help/privacypolicy',
        'xpath': '/html/body/div[3]/div/div[1]'},
    'reddit ToS': {'url': 'http://www.reddit.com/help/useragreement',
        'xpath': '/html/body/div[3]/div/div[1]'},
    'NewEgg TaC': {'url': 'http://www.newegg.com/Info/AllTermsAndConditions.aspx',
        'xpath': '/html/body/div[3]/div[2]/table/tbody/tr/td/div/div/div[3]/dl/dd/div'},
    'NewEgg PP': {'url': 'http://www.newegg.com/Info/AllTermsAndConditions.aspx',
        'xpath': '/html/body/div[3]/div[2]/table/tbody/tr/td/div/div/div[3]/dl[2]/dd/div'},
    'NewEgg Return Policy': {'url': 'http://www.newegg.com/Info/AllTermsAndConditions.aspx',
        'xpath': '/html/body/div[3]/div[2]/table/tbody/tr/td/div/div/div[3]/dl[3]'}
    }

