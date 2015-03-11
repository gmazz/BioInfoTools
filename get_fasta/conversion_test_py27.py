# Working only on Python 2.7!!
# http://www.uniprot.org/help/programmatic_access#batch_retrieval_of_entries


import urllib,urllib2

url = 'http://www.uniprot.org/mapping/'

params = {
'from':'ACC',
'to':'P_REFSEQ_AC',
'format':'tab',
'query':'P13368 P20806 Q9UM73 P97793 Q17192'
}

params_2 = {
'from':'ACC',
'to':'P_REFSEQ_AC',
'format':'tab',
'query':'P13368 P20806 Q9UM73 P97793 Q17192'
}

data = urllib.urlencode(params)
request = urllib2.Request(url, data)
contact = "" # Please set your email address here to help us debug in case of problems.
request.add_header('User-Agent', 'Python %s' % contact)
response = urllib2.urlopen(request)
page = response.read(200000)
print(page)