#!/bin/bash

pwd=`pwd`
export HOME=/home/develop
PATH=$PATH:/home/develop/bin export PATH
source /home/develop/env/bin/activate

export PYTHONPATH=/home/develop/src/etl/..
#export JAVA_HOME=/usr/local/java/jdk1.6.0_45
#export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export PATH=$JAVA_HOME/bin:$PATH
export DYLD_LIBRARY_PATH=/opt/IBM/db2/V10
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/IBM/db2/V10/lib64

#export IBM_DB_HOME=/opt/ibm/clidriver
#export IBM_PATH=/opt/ibm/clidriver
export IBM_DB_HOME=/opt/IBM/db2/V10
export IBM_PATH=/opt/IBM/db2/V10
export IBM_DB_DIR=${IBM_PATH?}
export IBM_DB_LIB=${IBM_PATH?}/lib
export IBM_DB_INCLUDE=${IBM_PATH?}/include
export DB2LIB=/opt/IBM/db2/V10/lib64
export PATH=$JAVA_HOME/bin:$PATH:$IBM_DB_HOME/bin

#pids=`ps -elf | grep develop|grep auto_run2.py| grep -v grep| awk '{print $4}'`
pids=`ps -elf | grep develop|grep auto_run.py| grep -v grep| awk '{print $4}'`
printf "pids:$pids\n"
if [ ! "X$pids" = "X" ]; then
    printf "服务已经在运行,进程号:$pids\n"
    exit 1
fi
printf "ok,运行"
#python /home/develop/src/etl/star/update/auto_run2.py >> /home/develop/src/etl/star/update/log/auto_run2.log
python /home/develop/src/etl/star/update/auto_run.py >> /home/develop/src/etl/star/update/log/auto_run.log
