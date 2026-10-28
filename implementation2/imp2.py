import numpy as np
import scipy as sp
from scipy.io import loadmat
from scipy.signal import remez, lfilter
from utilities import plot_dtft

import soundfile as sf


if __name__ == '__main__':
    #load data in
    mat = loadmat('baseband7.mat')
    #print(mat.keys())
    
    baseband_data = mat['data'].flatten()
    
    #print(baseband_data.shape, baseband_data.dtype, len(baseband_data)/256000, "seconds")
    plot_dtft(baseband_data)
    
    #limiter
    post_limiter_baseband = baseband_data/np.abs(baseband_data)
    
    #print(np.min(np.abs(baseband_data)))
    #print(np.allclose(np.abs(post_limiter_baseband), 1))
    #plot_dtft(post_limiter_baseband)
    
    #FIR differentiator
    numtaps = 31
    M = numtaps-1
    #group delay is M/2 so 15 samples

    fs = 256000

    wd = 2.5 #2.5 rad/sample is my omega_d

    #note: increasing my cutoff/boundary frequency wd to a higher value resulted in ripples within the transfer function graph for [-wd, wd]
    #it was nonlinear

    #also, decreasing my wd to numbers such as 1.2 failed to converge, message: "try reducing transition band"
    #but above that, such as 1.5, resulted in the area before the cutoff being linear but reduced in width as expected
    #2.4 was a nice sweet spot

    fd = wd*fs/(2*np.pi) #wd in hertz

    fir_diff = remez(numtaps, [0, fd], [1], fs=fs, type='differentiator')

    plot_dtft(fir_diff)

    #differentiating my post_limiter_baseband
    diff_baseband = lfilter(fir_diff, 1, post_limiter_baseband)


    #complex conjugate
    baseband_conj = np.conj(post_limiter_baseband)

    #apply delay of M/2
    zeroes = M//2
    delayed_baseband_conj = np.concatenate((np.zeros(zeroes), baseband_conj))
    delayed_baseband_conj = delayed_baseband_conj[:len(baseband_conj)]


    #multiplication
    y = np.imag(diff_baseband*delayed_baseband_conj)

    plot_dtft(y)
    
    #de-emphasis filter

    tau = 75e-6
    alpha = 2 * tau * fs

    b = [1/(1+alpha), 1/(1+alpha)]
    a = [1, (1-alpha)/(1+alpha)]

    deemph = lfilter(b, a, y)

    plot_dtft(deemph)


    #low pass filter
    lpf_numtaps = 201
    lpf = remez(lpf_numtaps, [0, 15000, 18000, fs/2], [1, 0], fs=fs)
    #filter length is 201 and transition band is 15kHz to 18000kHz

    plot_dtft(lpf)

    filtered = lfilter(lpf, 1, deemph)
    out = filtered[::4]

    plot_dtft(out)

    out = out - np.mean(out)

    out = out / np.max(np.abs(out))

    sf.write('output.wav', out, 64000)

    