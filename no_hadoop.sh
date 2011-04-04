#!/bin/bash
python linkmap.py map scowiki-20090929-one-page-per-line|sort>out_lm_map.txt
python linkmap.py reduce out_lm_map.txt>out_lm_reduce.txt
python pagerank.py map out_lm_reduce.txt|sort>out_pr_map.txt
python pagerank.py reduce out_pr_map.txt>out_pr_reduce.txt
python pr_out.py map out_pr_reduce.txt|sort>results.txt
