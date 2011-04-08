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
__global__ void reduction(float *g_data, int n)
{
	int index=blockIdx.x*blockDim.x+threadIdx.x;
	int numberOfCalculationsForThisStep=n/2;
	while(numberOfCalculationsForThisStep>0)
	{
		if(index<numberOfCalculationsForThisStep)
		{
			g_data[index]=g_data[index]+g_data[index+numberOfCalculationsForThisStep];
		}
		numberOfCalculationsForThisStep/=2;
	}
    return;
}
  """)
	
	func = mod.get_function("reduction")
	func(counts_gpu,numpy.int32(64),block=(512,1,1))
	counts_return = numpy.empty_like(counts_gpu)
	cuda.memcpy_dtoh(counts_return, counts_gpu)
	yield("1","1")

if __name__ == "__main__":
  common.main(map, reduce)
