# run_pagerank.sh
# ./run_pagerank.sh data num_reducers
export SJAR=/usr/lib/hadoop/contrib/streaming/hadoop-streaming-0.20.2-CDH3B4.jar
hadoop fs -copyFromLocal scowiki-20090929-one-page-per-line scowiki-20090929-one-page-per-line

hadoop fs -rmr linkmap0
hadoop jar $SJAR -mapper "$(pwd)/linkmap.py map" -reducer "$(pwd)/linkmap.py reduce" -input $1 -output linkmap0
for i in {0..9}
do
input_linkmap="linkmap$i"
output_linkmap="linkmap$((i+1))"
reducer_output="results$i"
hadoop fs -rmr $output_linkmap
if [ -n $2]
then
echo "Using default reducers"
hadoop jar $SJAR -mapper "$(pwd)/pagerank.py map" -reducer "$(pwd)/pagerank.py reduce" -input $input_linkmap -output $output_linkmap
else
echo "Using $2 reducers"
hadoop jar $SJAR -mapper "$(pwd)/pagerank.py map" -reducer "$(pwd)/pagerank.py reduce" -input $input_linkmap -output $output_linkmap -numReduceTasks $2
fi
hadoop fs -rmr $reducer_output
hadoop jar $SJAR -mapper "$(pwd)/pr_out.py map" -reducer "sort" -input $output_linkmap -output $reducer_output
done

