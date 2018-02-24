################################
# simple flask app run
################################
# ps ux|grep python|grep -v grep|awk '{print $2}'|xargs kill -9
# python run_app.py


################################
# adapet uwsgi server
################################
# ps ux|grep uwsgi|grep -v grep|awk '{print $2}'|xargs kill -9
# uwsgi --http :3000 --wsgi-file wsgi.py  --master --processes 2 --threads 1


################################
# adapet uwsgi+gevent  server
################################
# ps ux|grep uwsgi|grep -v grep|awk '{print $2}'|xargs kill -9
# uwsgi --http :3000 --wsgi-file wsgi.py --master  --gevent 2000 --gevent-monkey-patch  -l 1000 -p 4 -L


################################
# adapet gunicorn+gevent  server
################################
export HOME=/home/develop
source $HOME/.bash_profile
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib64:/usr/lib64/samba

cd /home/develop/src/web/server
ps ux|grep gunicorn|grep -v grep|awk '{print $2}'|xargs kill -9
# gunicorn -b 0.0.0.0:3000  --config --workers=5 wsgi:application
nohup gunicorn -c gun.conf  gun:app &
