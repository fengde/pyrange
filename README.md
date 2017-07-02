1. # pyrange
      提供文件分片下载和上传的接口

      **暂时已经完成了分片下载（也支持普通下载）的接口**

      ------
   
      **使用example**（以下载https://www.python.org/ftp/python/2.7.13/python-2.7.13-macosx10.6.pkg为例)

      ​	1）普通下载

      ``import pyrange``

      `task = pyrange.Download("https://www.python.org/ftp/python/2.7.13/python-2.7.13-macosx10.6.pkg")`

      `task.start()`

      ​	2）指定下载线程数和保存路径，阻塞模式

      `import pyrange`

      `task = pyrange.Download("https://www.python.org/ftp/python/2.7.13/python-2.7.13-macosx10.6.pkg", thread_num=5, path="./python-2.7.13-macosx.pkg")`

      `task.start()`

      ​	3)  指定下载线程数和保存路径，非阻塞模式，支持下载完成回调函数

      `import pyrange`

      `def func(url, filepath):`

      ​    `print "finished"`

      `task = pyrange.Download("https://www.python.org/ftp/python/2.7.13/python-2.7.13-macosx10.6.pkg", thread_num=5, path="./python-2.7.13-macosx.pkg", block=False, callback=func)`

      `task.start()`

      `task.join()`

     
