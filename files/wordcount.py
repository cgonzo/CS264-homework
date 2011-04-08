#!/usr/bin/python

import common
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy
import math

def map(line):
	common.ununicode(line)
	i=0
	for word in line.split():
		i=i+1
	yield("1",str(i))

def reduce(word, counts):
	counts_int=numpy.array(counts,numpy.int32)
	counts_gpu = cuda.mem_alloc(len(counts_int)*4)
	cuda.memcpy_htod(counts_gpu, counts_int)
	mod = SourceModule("""
__global__ void reduction(float *g_data)
{
	int index=blockIdx.x*blockDim.x+threadIdx.x;
	int numberOfCalculationsForThisStep=(blockDim.x+1)/2;
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
	
	totalsize=len(counts)
	threadsPerBlock=512;
	numBlocks=math.ceil(totalsize/threadsPerBlock)
	print "totalsize:"+str(totalsize)+" numBlocks:"+str(numBlocks)
	while(numBlocks>0):
		func(counts_gpu,block=(threadsPerBlock,1,1),grid=(int(numBlocks),1))
		numelements=numBlocks
		if(numBlocks==1):
			numBlocks=0
		else:
			numBlocks=math.ceil(numelements/threadsPerBlock)
	counts_return = numpy.empty_like(counts_int)
	cuda.memcpy_dtoh(counts_return, counts_gpu)
	yield("1",str(counts_return[0]))

if __name__ == "__main__":
  common.main(map, reduce)
