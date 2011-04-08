# run_pagerank.sh
# ./run_pagerank.sh data num_reducers
export SJAR=/usr/lib/hadoop/contrib/streaming/hadoop-streaming-0.20.2-CDH3B4.jar
hadoop fs -copyFromLocal $1 $1

hadoop fs -rmr linkmap0
hadoop jar $SJAR -mapper "/usr/bin/python linkmap.py map" -reducer "/usr/bin/python linkmap.py reduce" -input $1 -output linkmap0 -file "files/linkmap.py" -file "files/common.py"
for i in {0..9}
do
input_linkmap="linkmap$i"
output_linkmap="linkmap$((i+1))"
reducer_output="results$i"
hadoop fs -rmr $output_linkmap
if [ $2 ]
then
echo "Using $2 reducers"
hadoop jar $SJAR -mapper "/usr/bin/python pagerank.py map" -reducer "/usr/bin/python pagerank.py reduce" -input $input_linkmap -output $output_linkmap -numReduceTasks $2 -file "files/pagerank.py" -file "files/common.py"
else
echo "Using default reducers"
hadoop jar $SJAR -mapper "/usr/bin/python pagerank.py map" -reducer "/usr/bin/python pagerank.py reduce" -input $input_linkmap -output $output_linkmap -file "files/pagerank.py" -file "files/common.py"
fi
hadoop fs -rmr $reducer_output
hadoop jar $SJAR -mapper "/usr/bin/python pr_out.py map" -reducer "/usr/bin/sort" -input $output_linkmap -output $reducer_output -file "files/pr_out.py" -file "files/common.py"
done

