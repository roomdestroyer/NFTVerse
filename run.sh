ps aux|grep gunicorn|grep -v grep|cut -c 9-17|xargs kill -9
gunicorn -w 1 -b 0.0.0.0:9100 manage:app
