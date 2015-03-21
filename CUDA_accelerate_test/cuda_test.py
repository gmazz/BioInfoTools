'''
Demonstrate the vectorize API with automatical memory transfer and
manual memory transfer.
'''
from timeit import default_timer as timer
import numpy
from numbapro import vectorize, float64, cuda

@vectorize([float64(float64, float64)], target='gpu')
def vector_mul(a, b):
    return  a * b

a = numpy.random.rand(10000000)
b = numpy.random.rand(10000000)

# Let NumbaPro automatically convert host memory to device memory
ts = timer()
for i in xrange(10):

    result = vector_mul(a, b)
te = timer()

print ('auto', te - ts)