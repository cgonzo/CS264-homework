#!/usr/bin/python

import common
import pycuda
import numpy

def map(line):
	common.ununicode(line)
	for word in line.split():
		yield("1","1")

def reduce(word, counts):
	counts_int=numpy.array(counts,int)
	counts_gpu = pycuda.mem_alloc(counts.nbytes)
	pycuda.memcpy_htod(counts_gpu, counts)
	
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
    // Store result from shared memory  back to global memory
	if(threadIdx.x==0)
	{
		g_data[blockIdx.x]=s_data[threadIdx.x];
	}
    return;
}
  """)
	
	func = mod.get_function("reduction")
	func(counts_gpu)
	counts_return = numpy.empty_like(counts)
	pycuda.memcpy_dtoh(counts_return, counts)
	yield("1",counts_return[0])

if __name__ == "__main__":
  common.main(map, reduce)
