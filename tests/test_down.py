# -*- coding:utf-8 -*-

import pyrange
import unittest
import time

url = "http://zipzapmac.com/DMGs/Go2Shell.dmg"
class TestDownload(unittest.TestCase):
    def test_common(self):
        print "{unixtime} common start".format(unixtime=time.time())
        task = pyrange.Download(url, path="./Go2Shell.dmg")
        task.start()
        print "{unixtime} common finished".format(unixtime=time.time())

    def test_rangebytes(self):
        print "{unixtime} rangebytes start".format(unixtime=time.time())
        task = pyrange.Download(url, thread_num=2, path="./Go2Shell.dmg")
        task.start()
        print "{unixtime} rangebytes finished".format(unixtime=time.time())

    def test_unblock(self):
        def func(url, filepath):
            print "callback exec.url={}, filepath={}".format(url, filepath)

        print "{unixtime} unblock start".format(unixtime=time.time())
        task = pyrange.Download(url, thread_num=2, path="./Go2Shell.dmg",  block=False, callback=func)
        task.start()
        print "{unixtime} unblock here".format(unixtime=time.time())
        task.wait()
        print "{unixtime} unblock finished".format(unixtime=time.time())

if __name__ == "__main__":
    unittest.main()