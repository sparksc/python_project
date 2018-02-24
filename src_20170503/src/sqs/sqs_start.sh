#!/bin/bash
ARGV="$@"
cd /home/develop/src/sqs
start(){
	echo "启动查询服务"
    nohup python  report_proxy.py 8082 &
	nohup python  report_proxy.py 9970 &
	nohup python  report_proxy.py 9971 &
	nohup python  report_proxy.py 9972 &
	nohup python  report_proxy.py 9973 &
	nohup python  report_proxy.py 9974 &
	nohup python  report_proxy.py 9975 &
	nohup python  report_proxy.py 9976 &
	nohup python  report_proxy.py 9977 &
	nohup python  report_proxy.py 9978 &
	nohup python  report_proxy.py 9979 &
	nohup python  report_proxy.py 9980 &
	nohup python  report_proxy.py 9981 &
	nohup python  report_proxy.py 9982 &
	nohup python  report_proxy.py 9983 &
	nohup python  report_proxy.py 9984 &
	nohup python  report_proxy.py 9985 &
	nohup python  report_proxy.py 9986 &
	nohup python  report_proxy.py 9987 &
	nohup python  report_proxy.py 9988 &
	nohup python  report_proxy.py 9989 &
	nohup python  report_proxy.py 9990 &
	nohup python  report_proxy.py 9991 &
	nohup python  report_proxy.py 9992 &
	nohup python  report_proxy.py 9993 &
	nohup python  report_proxy.py 9994 &
	nohup python  report_proxy.py 9995 &
	nohup python  report_proxy.py 9996 &
	nohup python  report_proxy.py 9997 &
	nohup python  report_proxy.py 9998 &
	nohup python  report_proxy.py 9999 &
	echo "启动完成"
}

stop(){
	echo "停止查询服务"
	ps -ef|grep python|grep -v grep|grep report_proxy.py|awk '{print $2}'|xargs kill -9

}

case $ARGV 
	in
	start)
	start
	ERROR=$?
	;;
	stop)
	stop
	ERROR=$?
	;;
	restart)
	stop
	start
	ERROR=$?
	;;
	*)
	echo "start.sh [start|restart|stop]"
	esac
	exit $ERROR


