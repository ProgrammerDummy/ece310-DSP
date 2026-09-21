import numpy as np
import scipy as sp

def lowpass(wc, M):
    #N = 2M + 1 taps
    
    n = np.arange(-M, M+1) #ints from -M to M
    h = np.sin(wc*n)/(np.pi*n) #calculate the value for each tap
    h[n == 0] = wc/np.pi #account for discontinuity at n == 0
    
    return h #return the impulse respons/e function

def bandpass(wc, wH, M):
    #this is using the lowpass but the central frequency is shifted
    h = lowpass(wc, M)
    
    #shift the frequency by mulitiplying 2cos(w_h * n) to impulse response function h
    
    modulator = np.arange(-M, M+1)
    modulator = 2*np.cos(wH * modulator)
    
    return h * modulator #return the impulse response function after applying the shift
    
   

