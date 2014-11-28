# -*- coding: utf-8 -*-
 
"""
The MIT License (MIT)
 
Copyright (c) 2013 Joan Creus <joan.creus.c@gmail.com>
 
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
 
import re
from datetime import datetime, date
 
import pywikibot as wikipedia
#import query as query
import pywikibot.data.api
 
site = wikipedia.Site('it','wikisource')
punts = {}
vali = {}
revi = {}
llibres = [u'Patria Esercito Re.djvu', u'Operette morali.djvu', u'Zibaldone di pensieri IV.djvu', u'Zibaldone di pensieri V.djvu', u'Zibaldone di pensieri VI.djvu', u'Zibaldone di pensieri VII.djvu', u'Rime (Cavalcanti).djvu', u'Eneide (Caro).djvu', u'I colloqui.djvu|I colloqui', u'Ultime lettere di Jacopo Ortis', u'Canne al vento.djvu', u'Il podere.djvu', u'Cuore (1889).djvu', u'Lettere sulla Alceste seconda (Bettoni 1808).djvu', u'Verri - Meditazioni sulla economia politica, 1771.pdf', u'Vasco - Della moneta, 1788.djvu', u'Delle cinque piaghe della Santa Chiesa (Rosmini).djvu', u'Così parlò Zarathustra.djvu', u'Sopra lo amore.djvu', u'Saul.djvu', u'Manuale 150 ricette di cucina di guerra.djvu']
begin = 1
"""
Put your local last page of books in the right order. ex: Foggerty.djvu is 376"
"""
end = [427, 436, 451, 444, 462, 496, 228, 668, 174, 394, 312, 256, 338, 104, 273, 208, 144, 312, 170, 92, 84]
if len(llibres) == len(end):
        print "OK, sono uguali"
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
                data = pywikibot.data.api.CachedRequest(5, **params).submit()
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
                        if a == 3 and old < 3 and data >= datetime(2014, 11, 24, 0, 0, 0) and data < datetime(2014, 12, 2, 0, 0, 0):
                                print u"%s proofreads the page %d." % (b, pag)
                                if old == None: print u"Page doesn't exist before."
                                punts[b] = punts.get(b, 0)+2
                                revi[b] = revi.get(b, 0)+1
                        if a == 3 and old == 4 and data >= datetime(2014, 11, 24, 0, 0, 0) and data < datetime(2014, 12, 2, 0, 0, 0):
                                if (oldData >= datetime(2014, 11, 14, 0, 0, 0) and oldData < datetime(2014, 11, 25, 0, 0, 0)):
                                        punts[oldUser] = punts.get(oldUser, 0)-1
                                        vali[oldUser] = vali.get(oldUser, 0)-1
                        if a == 4 and old == 3 and data >= datetime(2014, 11, 24, 0, 0, 0) and data < datetime(2014, 12, 2, 0, 0, 0):
                                print u"%s validates page %d." % (b, pag)
                                punts[b] = punts.get(b, 0)+1
                                vali[b] = vali.get(b, 0)+1
                        if a < 3 and old == 3 and data >= datetime(2014, 11, 24, 0, 0, 0) and data < datetime(2014, 12, 2, 0, 0, 0):
                                if (oldData >= datetime(2014, 11, 24, 0, 0, 0) and oldData < datetime(2014, 12, 2, 0, 0, 0)):
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