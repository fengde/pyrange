1. # pyrange
      **just support download by range now.**

      ------

      **example**

      ​     1）common download.

      `import pyrange`

      `task = pyrange.Download("https://www.python.org/ftp/python/2.7.13/python-2.7.13-macosx10.6.pkg")`

      `task.start()`

      ​     2）download in block mode.

      `import pyrange`

      `task = pyrange.Download("https://www.python.org/ftp/python/2.7.13/python-2.7.13-macosx10.6.pkg", thread_num=5, path="./python-2.7.13-macosx.pkg")`

      `task.start()`

      ​     3)  download in unblock mode, also support callback.

      `import pyrange`

      `def func(url, filepath):`

      ​    `print "finished"`

      `task = pyrange.Download("https://www.python.org/ftp/python/2.7.13/python-2.7.13-macosx10.6.pkg", thread_num=5, path="./python-2.7.13-macosx.pkg", block=False, callback=func)`

      `task.start()`

      `task.wait()`