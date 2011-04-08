# run_gpu_wordcount.sh
# ./run_gpu_wordcount.sh data
export SJAR=/usr/lib/hadoop/contrib/streaming/hadoop-streaming-0.20.2-CDH3B4.jar
hadoop fs -copyFromLocal $1 $1

hadoop fs -rmr $(1)_wc
hadoop jar $SJAR -mapper "/usr/bin/python wordcount.py map" -reducer "/usr/bin/python wordcount.py reduce" -input $1 -output linkmap0 -file "files/wordcount.py" -file "files/common.py"
