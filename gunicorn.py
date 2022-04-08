cmmand = 'gunicorn'  #gunicorn命令的绝对路径
pythonpath = '/usr/Sacob/'   #项目路径
bind = '0.0.0.0:9101'   #运行服务的IP和端口
workers = 3   #开几个线程来执行请求
