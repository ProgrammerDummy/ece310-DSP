import numpy as np
import scipy as sp
from scipy.io import loadmat
from scipy.signal import remez, lfilter
from utilities import plot_dtft


if __name__ == '__main__':
    #load data in
    mat = loadmat('baseband1.mat')
    print(mat.keys())
    
    baseband_data = mat['data'].flatten()
    
    print(baseband_data.shape, baseband_data.dtype, len(baseband_data)/256000, "seconds")
    plot_dtft(baseband_data)
    
    #limiter
    post_limiter_baseband = baseband_data/np.abs(baseband_data)
    
    print(np.min(np.abs(baseband_data)))
    print(np.allclose(np.abs(post_limiter_baseband), 1))
    plot_dtft(post_limiter_baseband)
    
    M = 1000 #placeholder for now
    
    #FIR differentiator
    
    #complex conjugate
    baseband_conj = np.conj(baseband_data)
    #apply delay here too
    
    
    
    pass


    """
    todo/build list
    
    1) input 
    load sample .mat file using scipy loadmat func
    sample at 256 kHz
    
    2) limiter
    divide signal from point-wise magnitude
    use numpy abs func
    
    3) FIR differentiator
    design a linear-phase FIR filter to approximate the ideal discrete time differentatior
    use parks-mcclellan algo
    use scipy remez func w/ setting type to "differentiator"
    
    4) complex conjuggate
    take complex conjugate w/ numpy conj function
    add differentiator group delay (M/2)
    
    5) mix steps 3 and 4 together
    
    """