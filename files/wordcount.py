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
	counts_gpu = cuda.mem_alloc(counts_int.nbytes)
	cuda.memcpy_htod(counts_gpu, counts_int)
	
	mod = SourceModule("""
__global__ void reduction(float *g_data, int n)
{
	int index=blockIdx.x*blockDim.x+threadIdx.x;
    // Do sum reduction from shared memory
	int numberOfCalculationsForThisStep=(blockDim.x+1)/2;
	while(numberOfCalculationsForThisStep>0)
	{
		if(threadIdx.x<numberOfCalculationsForThisStep)
		{
			g_data[index]=g_data[index]+g_data[index+numberOfCalculationsForThisStep];
		}
		numberOfCalculationsForThisStep/=2;
		__syncthreads();
	}
    return;
}
  """)
	
	func = mod.get_function("reduction")
	func(counts_gpu,int_(64),block=(64,1,1))
	counts_return = numpy.empty_like(counts)
	cuda.memcpy_dtoh(counts_return, counts)
	yield("1",counts_return[0])

if __name__ == "__main__":
  common.main(map, reduce)
