# run_gpu_wordcount.sh
# ./run_gpu_wordcount.sh data
export SJAR=/usr/lib/hadoop/contrib/streaming/hadoop-streaming-0.20.2-CDH3B4.jar
hadoop fs -copyFromLocal $1 $1

hadoop fs -rmr $1_wc
hadoop jar $SJAR -mapper "/usr/bin/python2.6 wordcount.py map" -reducer "/usr/bin/python2.6 wordcount.py reduce" -input shakespeare -output shakespeare_wc -file "files/wordcount.py" -file "files/common.py" -cmdenv PATH=$PATH
