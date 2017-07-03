# -*- coding:utf-8 -*-

import pyrange
import unittest
import time

url = "https://www.python.org/ftp/python/2.7.13/python-2.7.13-macosx10.6.pkg"
class TestDownload(unittest.TestCase):
    def test_common(self):
        print "{unixtime} common start".format(unixtime=time.time())
        task = pyrange.Download(url, path="./python-common.pkg")
        task.start()
        print "{unixtime} common finished".format(unixtime=time.time())

    def test_rangebytes(self):
        print "{unixtime} rangebytes start".format(unixtime=time.time())
        task = pyrange.Download(url, thread_num=2, path="./python-rangebytes.pkg")
        task.start()
        print "{unixtime} rangebytes finished".format(unixtime=time.time())

    def test_unblock(self):
        def func(url, filepath):
            print "callback exec.url={}, filepath={}".format(url, filepath)

        print "{unixtime} unblock start".format(unixtime=time.time())
        task = pyrange.Download(url, thread_num=2, path="./python-unblock",  block=False, callback=func)
        task.start()
        print "{unixtime} unblock here".format(unixtime=time.time())
        task.wait()
        print "{unixtime} unblock finished".format(unixtime=time.time())

if __name__ == "__main__":
    unittest.main()