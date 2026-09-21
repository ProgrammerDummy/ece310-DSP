import numpy as np
from filters import lowpass, bandpass
from utilities import hz_to_omega
from scipy.signal import lfilter

def equalizer(x, fs, M, g_low, g_mid, g_high):
    h_low = g_low * lowpass(hz_to_omega(300, fs), M)
    
    fh_mid = (300+2000)/2
    fc_mid = (2000-300)/2
    
    h_mid = g_mid * bandpass(hz_to_omega(fc_mid, fs), hz_to_omega(fh_mid, fs), M)
    
    fh_high = (2000+20000)/2
    fc_high = (20000-2000)/2
    
    h_high = g_high * bandpass(hz_to_omega(fc_high, fs), hz_to_omega(fh_high, fs), M)
    
    
    h_total = h_low + h_mid + h_high
    

    
    return lfilter(h_total, 1, x)




