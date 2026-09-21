from filters import lowpass
import numpy as np
from scipy.signal import lfilter

def expansion(L, x):
    expanded_x = np.zeros(len(x) * L)
    #create an array of size len(x)*L filled iwth 0
    
    expanded_x[::L] = x
    #start:stop:step, for every L zeroes, place the original data point
    
    return expanded_x
    

def decimation(D, x):
    decimated_x = x[::D]
    #take only Dth data points of x by slicing at D steps 
    
    return decimated_x

def rate_conversion(x, L, D, M):
    
    wc = min(np.pi/L, np.pi/D)
    
    expanded_x = expansion(L, x)
    
    h = L*lowpass(wc, M)
    
    filtered_x = lfilter(h, 1, expanded_x)
    
    decimated_x = decimation(D, filtered_x)
    
    return decimated_x
    