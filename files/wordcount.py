#!/usr/bin/python

import common
import pyopencl
from pyopencl.scan import InclusiveScanKern
import pyopencl.array as cl_array

def map(line):
	common.ununicode(line)
	for word in line.split:
		yield(1,1)

def reduce(word, counts):
	ctx = pyopencl.create_some_context()
	queue = cl.CommandQueue(ctx)
	knl = InclusiveScanKernel(ctx, np.int32, "a+b")
	counts_gpu = cl_array.to_device(queue,counts)
	
	knl(counts_gpu)
	counts_cpu=counts_gpu.get
	yield(1,counts_cpu[len(counts_cpu)-1])

if __name__ == "__main__":
  common.main(map, reduce)
