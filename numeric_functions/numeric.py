import numpy as np

# One line factorial
def fact(v) : return reduce(lambda x, y: x * y, np.arange(1,v+1))