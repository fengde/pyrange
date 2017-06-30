# -*- coding:utf8 -*-
import requests
import os, os.path

def is_support(url):
    ''' 检查url是否支持分片下载
    返回True/False
    '''
    resp = requests.head(url)
    return "Accept-Ranges" in resp.headers.keys()

def get_content_length(url):
    ''' 判断url是否支持分片下载的同时，获取下载内容的长度 
    返回是否支持分片下载 True/False, 以及内容长度
    '''
    resp = requests.head(url)
    if "Accept-Ranges" in resp.headers.keys():
        return True, int(resp.headers.get("Content-Length"), 0)
    else:
        return False, 0

def _down_worker(url, filepath, range_start, range_end):
    with open(filepath, "wb") as f:     
        r = requests.get(url, headers={"Range":"bytes={start}-{end}".format(start=range_start, end=range_end)},
            stream=True)
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

def _merge_file(from_file_paths, to_file_path):
    with open(to_file_path, "wb") as f:
        for from_file_path in from_file_paths:
            with open(from_file_path, "rb") as sub_f:
                while 1:
                    bytes = sub_f.read(1024)
                    if not bytes:
                        break
                    f.write(bytes)

def _clear_tmp(paths):
    for path in paths:
        os.remove(path)

def down(url, thread_num=1, path=""):
    ''' 输入url，分成thread_num个线程下载，保存的文件名path
    thread_num默认为1，path默认当前文件夹下
    '''
    # 检查url是否支持分片下载
    support, length = get_content_length(url)
    if not support:
        print "url不支持分片下载"
        return
    if thread_num < 0:
        thread_num = 1

    if not path:
        import urlparse
        pr = urlparse.urlparse(url)
        path =os.path.join(os.path.abspath(os.curdir), pr.path.split("/")[-1])

    dir, filename = os.path.split(os.path.abspath(path))
    # 检查dir是否存在，不存在则新建
    if not os.path.exists(dir):
        os.makedirs(dir)

    slice= length / thread_num
    paths = []
    workers = []
    import multiprocessing
    for i in range(thread_num):
        if i < (thread_num-1):
            range_start, range_end = i*slice, (i+1)*slice-1
        else:
            range_start, range_end = i*slice, length

        subpath = os.path.join(dir, "{}{}_{}".format(filename, range_start, range_end))
        p = multiprocessing.Process(target=_down_worker, args=(url, subpath, range_start, range_end))
        p.start()
        workers.append(p)
        paths.append(subpath)

    for worker in workers:
        worker.join()

    _merge_file(from_file_paths=paths, to_file_path=path)
    _clear_tmp(paths)

if __name__ == "__main__":
    down("https://www.python.org/ftp/python/2.7.13/python-2.7.13-macosx10.6.pkg", 5, "python.pkg")