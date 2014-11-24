    # -*- coding: utf-8 -*-
     
    """
  Original code from here:
  http://pastebin.com/Vk6ikCUg#
  

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
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
     
    import re
    from datetime import datetime, date
     
    import pywikibot as wikipedia
    import pywikibot.compat.query as query
    import pywikibot.data.api
    import operator
     
    site = wikipedia.getSite('it','wikisource')
    points = {}
    """
    Change the books of Catalan contest for your local books. ex. "Mar y cel (1903).djvu" --> "Foggerty.djvu"
    """
    books = [u'Patria Esercito Re.djvu', u'Operette morali.djvu', u'Zibaldone di pensieri IV.djvu', u'Zibaldone di pensieri V.djvu', u'Zibaldone di pensieri VI.djvu', u'Zibaldone di pensieri VII.djvu', u'Rime (Cavalcanti).djvu', u'Eneide (Caro).djvu', u'I colloqui.djvu|I colloqui', u'Ultime lettere di Jacopo Ortis', u'Canne al vento.djvu', u'Il podere.djvu', u'Cuore (1889).djvu', u'Lettere sulla Alceste seconda (Bettoni 1808).djvu', u'Vasco - Della moneta, 1788.djvu', u'Delle cinque piaghe della Santa Chiesa (Rosmini).djvu', u'Così parlò Zarathustra.djvu', u'Sopra lo amore.djvu', u'Saul.djvu']
    begin = 1
    """
    Put your local last page of books in the right order. ex: Foggerty.djvu is 376"
    """
    end = [427, 436, 451, 444, 462, 496, 228, 668, 174, 394, 312, 256, 338]
    i = 0
    for book in books:
            for pag in range(begin, end[i]+1):
                    params = {
                                    'action'        :'query',
                                    'prop'          :'revisions',
                                    'titles'        :u'Pàgina:%s/%d' % (book, pag),
                                    'rvlimit'       :'50',
                                    'rvprop'        :'user|timestamp|content',
                    }
                    data = pywikibot.data.api.CachedRequest(5, site=site, **params).submit()
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
                                    print u"Book %s" % book
                                    print u"%s proofreads the page %d." % (b, pag)
                                    if old == None: print u"Page doesn't exist before."
                                    else: print u"Page change from %d to %d quality." % (old, a)
                                    points[b] = points.get(b, 0)+3
                            if a == 3 and old == 4 and data >= datetime(2013, 11, 24, 0, 0, 0) and data < datetime(2013, 12, 2, 0, 0, 0):
                                    if (oldData >= datetime(2013, 11, 24, 0, 0, 0) and oldData < datetime(2013, 12, 2, 0, 0, 0)):
                                            points[oldUser] = points.get(oldUser, 0)-1
                            if a == 4 and old == 3 and data >= datetime(2013, 11, 24, 0, 0, 0) and data < datetime(2013, 12, 2, 0, 0, 0):
                                    print u"%s validates page %d." % (b, pag)
                                    points[b] = points.get(b, 0)+1
                            old = a
                            oldUser = b
                            oldData = data
                    print "-------"
            i+= 1
    points = sorted(points.iteritems(), key=operator.itemgetter(1), reverse=True)
    print u"{| Class=\"wikitable sortable\" border=\"1\" cellpadding=\"2\" cellspacing=\"0\" align=\"center\""
    print u"! Classifica || Utente || Punti"
    j = 1
    for point in points:
            print "|-----"
            print ("| %d ||[[User:"+point[0]+"|"+point[0]+"]] || %d") % (j, point[1])
            j += 1
    print u"|}"