# pyrangebyte
提供文件分片下载和上传的接口

**暂时已经完成了分片下载的接口**

------



供第三方使用的API如下：

  1.  **down(url, thread_num=1, path="")** 
      功能：指定thread_num个进程进行下载，保存于path，如果thread_num，path未指定，则使用一个进程下载，保存跟url尾部一致的文件名
      输入：下载链接，下载进程数，保存文件路径
      返回：无

  2.  **is_support(url)**
      功能：检测url是否支持分片下载
      输入：下载链接
      返回：True/False
  3.  **get_content_length(url)**
      功能：获取下载资源的文件大小
      输入：下载链接
      返回：True, int   （是否支持分片，文件大小）
