#!/usr/bin/python

import common
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy

def map(line):
	common.ununicode(line)
	for word in line.split():
		yield("1","1")

def reduce(word, counts):
	counts_int=numpy.array(counts,int)
	counts_gpu = cuda.mem_alloc(64)
	#cuda.memcpy_htod(counts_gpu, counts_int)
	
	mod = SourceModule("""
__global__ void reduction(float *g_data)
{
	int index=blockIdx.x*blockDim.x+threadIdx.x;
	g_data[index]=index;
    return;
}
  """)
	
	func = mod.get_function("reduction")
	func(counts_gpu,block=(1,1,1))
	counts_return = numpy.empty_like(counts_gpu)
	cuda.memcpy_dtoh(counts_return, counts_gpu)
	counts_gpu.free()
	yield("1","1")

if __name__ == "__main__":
  common.main(map, reduce)
