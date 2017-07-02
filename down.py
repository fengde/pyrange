# -*- coding:utf8 -*-

import requests
import os, os.path
import multiprocessing

class Download(object):
    ''' Use Download object to download http resource. 
    The Download class support range bytes.
    block-down example:
        task = Download("https://www.python.org/ftp/python/2.7.13/python-2.7.13-macosx10.6.pkg", 
            thread_num=2, path="./python2.7.13-mac.pkg")
        task.start()
    unblock-down example:
        task = Download("https://www.python.org/ftp/python/2.7.13/python-2.7.13-macosx10.6.pkg", 
            thread_num=2, path="./python2.7.13-mac.pkg", block=False)
        task.start()
        task.wait()
    in unblock-down mode, you are be allowed to give the "callback" function to __init__, just like:
        def func(url, path):
            print "finished"

        task = Download("https://www.python.org/ftp/python/2.7.13/python-2.7.13-macosx10.6.pkg", 
            thread_num=2, path="./python2.7.13-mac.pkg", block=False, callback=func)
        task.start()
        task.wait()
    '''
    def __init__(self, url, **kwargs):
        ''' url: the resource's url which you need to download.
            **kwargs support:
                thread_num: how many subporcess to download the resource. 1 is default 
                    if you haven't pass the parameter or pass a number which is less than 1.
                path: where to save the resource. If you haven't pass the parameter, the tail of url
                    will be used as the resource filename, and save in current dir.
                block: download mode, block(True) or unblock(False). Block(True) is defalut.
                callback: when you choice the unblock mode to download resource, you can pass 
                    a callback function which will be executed when the download task finished.
                    Callback function format is:  def xx(url, path).
        '''
        self.url = url
        self.subprocess_num = kwargs.get("thread_num", 1)
        self.subprocess_num = 1 if self.subprocess_num < 1 else self.subprocess_num
        self.path = kwargs.get("path", "")
        if not self.path:
            import urlparse
            pr = urlparse.urlparse(self.url)
            self.path =os.path.join(os.path.abspath(os.curdir), pr.path.split("/")[-1])

        self.block = kwargs.get("block", True)
        self.callback = kwargs.get("callback", None)

    def support(self):
        ''' judge whether the url support the range bytes. '''
        resp = requests.head(self.url)
        return "Accept-Ranges" in resp.headers.keys()

    def get_content_length(self):
        ''' get the resource content length. '''
        resp = requests.head(self.url)
        return int(resp.headers.get("Content-Length"), 0)

    def info(self):
        ''' get the download task infomation.'''
        return {
            "url": self.url,
            "thread_num": self.subprocess_num,
            "path": self.path,
            "block": self.block,
            "callback": self.callback,
        }

    def start(self):
        ''' start the download task'''
        if self.subprocess_num > 1 and (not self.support()):
            print "Error:{} 不支持分片下载".format(self.url)
            return

        self.filedir, self.filename = os.path.split(os.path.abspath(self.path))
        # if the dir doesn't exist, then create it.
        if not os.path.exists(self.filedir):
            os.makedirs(self.filedir)

        if self.block:
            self.__down(self.url, self.get_content_length(), self.subprocess_num, 
                self.filedir, self.filename, self.block, self.callback)
        else:
            self.process = multiprocessing.Process(target=Download.__down, 
                args=(self.url, self.get_content_length(), self.subprocess_num, 
                    self.filedir, self.filename, self.block, self.callback))
            self.process.start()

    def wait(self):
        ''' wait until the download task is finished.
        '''
        if hasattr(self, "process"):
            self.process.join()

    @staticmethod
    def __down_worker(url, filepath, range_start, range_end):
        with open(filepath, "wb") as f:     
            r = requests.get(url, headers={"Range":"bytes={start}-{end}".format(start=range_start, end=range_end)},
                stream=True)
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

    @staticmethod
    def __down(url, content_length, subprocess_num, filedir, filename, block, callback):
        slice= content_length / subprocess_num

        paths, workers = [], []
        for i in range(subprocess_num):
            if i < (subprocess_num-1):
                range_start, range_end = i*slice, (i+1)*slice-1
            else:
                range_start, range_end = i*slice, content_length

            subpath = os.path.join(filedir, "{}{}_{}".format(filename, range_start, range_end))
            p = multiprocessing.Process(target=Download.__down_worker, args=(url, subpath, range_start, range_end))
            p.start()
            workers.append(p)
            paths.append(subpath)

        for worker in workers:
            worker.join()

        filepath = os.path.join(filedir, filename)
        Download.__merge_file(from_file_paths=paths, to_file_path=filepath)
        Download.__clear(paths)

        if (not block) and callable:
            self.callback(url, filepath)

    @staticmethod
    def __merge_file(from_file_paths, to_file_path):
        with open(to_file_path, "wb") as f:
            for from_file_path in from_file_paths:
                with open(from_file_path, "rb") as sub_f:
                    while 1:
                        bytes = sub_f.read(1024)
                        if not bytes:
                            break
                        f.write(bytes)

    @staticmethod
    def __clear(paths):
        for path in paths:
            os.remove(path)


if __name__ == "__main__":
    task = Download("https://www.python.org/ftp/python/2.7.13/python-2.7.13-macosx10.6.pkg", 
            thread_num=2, path="./python2.7.13-mac.pkg", block=False)
    task.start()
    print "here!!!"