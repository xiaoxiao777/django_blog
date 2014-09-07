#!/usr/bin/python

import urllib
import urllib2
page=urllib2.Request(url = "http://www.baidu.com")
data=urllib2.urlopen(page)
print data.read()
