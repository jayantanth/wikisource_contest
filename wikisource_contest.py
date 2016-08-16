# -*- coding: utf-8 -*-
 
import re
from datetime import datetime, date
 
import pywikibot as wikipedia
#import query as query
import pywikibot.data.api
 
site = wikipedia.Site('bn','wikisource')
punts = {}
vali = {}
revi = {}
llibres = [u'কাদম্বরী.djvu', u'শকুন্তলা (সিগনেট প্রেস সংস্করণ).djvu']
begin = 1
"""
Put your local last page of books in the right order. ex: Foggerty.djvu is 376"
"""
end = [151, 56] # mancano dai romanzi in poi
if len(llibres) == len(end):
        print "OK, they're the same"
i = 0
for llibre in llibres:
        print llibre
        for pag in range(begin, end[i]+1):
                print pag
                params = {
                                'action'        :'query',
                                'prop'          :'revisions',
                                'titles'        :u'Page:%s/%d' % (llibre, pag),
                                'rvlimit'   :'50',
                                'rvprop'        :'user|timestamp|content',
                }
                data = pywikibot.data.api.CachedRequest(5, **params).submit() #data = pywikibot.data.api.CachedRequest(0, site=site, **params).submit() 
                try:    
                        revs = data["query"]["pages"].values()[0]["revisions"][::-1]
                except KeyError:
                        continue
                old = None
                oldUser = None
                oldData = None
                for rev in revs:
                        data = datetime.strptime(rev["timestamp"], '%Y-%m-%dT%H:%M:%SZ')
                        user = rev["user"]
                        txt = rev["*"]
                        a,b = re.findall('<pagequality level="(\d)" user="(.*?)" />', txt)[0]
                        a = int(a)
                        b = user
                        if a == 3 and old < 3 and data >= datetime(2015, 11, 23, 0, 0, 0) and data < datetime(2015, 12, 8, 0, 0, 0):
                                print u"%s proofreads the page %d." % (b, pag)
                                if old == None: print u"Page doesn't exist before."
                                punts[b] = punts.get(b, 0)+2
                                revi[b] = revi.get(b, 0)+1
                        if a == 3 and old == 4 and data >= datetime(2015, 11, 23, 0, 0, 0) and data < datetime(2015, 12, 8, 0, 0, 0):
                                if (oldData >= datetime(2015, 11, 23, 0, 0, 0) and oldData < datetime(2015, 11, 24, 0, 0, 0)):
                                        punts[oldUser] = punts.get(oldUser, 0)-1
                                        vali[oldUser] = vali.get(oldUser, 0)-1
                        if a == 4 and old == 3 and data >= datetime(2015, 11, 23, 0, 0, 0) and data < datetime(2015, 12, 8, 0, 0, 0):
                                print u"%s validates page %d." % (b, pag)
                                punts[b] = punts.get(b, 0)+1
                                vali[b] = vali.get(b, 0)+1
                        if a < 3 and old == 3 and data >= datetime(2015, 11, 23, 0, 0, 0) and data < datetime(2015, 12, 8, 0, 0, 0):
                                if (oldData >= datetime(2015, 11, 23, 0, 0, 0) and oldData < datetime(2015, 12, 8, 0, 0, 0)):
                                        punts[oldUser] = punts.get(oldUser, 0)-2
                                        revi[oldUser] = vali.get(oldUser, 0)-1
                                       
                               
                        old = a
                        oldUser = b
                        oldData = data
                print "-------"
        i=i+1
print "punt",sorted(punts.iteritems(), key=lambda x: x[1], reverse=True)
print "vali",sorted(vali.iteritems(), key=lambda x: x[1], reverse=True)
print "revi",sorted(revi.iteritems(), key=lambda x: x[1], reverse=True)
