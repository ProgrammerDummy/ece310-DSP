import numpy as np
from utilities import plot_dtft, make_test_signal, hz_to_omega
from filters import lowpass, bandpass
from equalizer import equalizer
import soundfile as sf

from rateconv import expansion, decimation, rate_conversion



if __name__ == '__main__':
    # Example usage
    fs = 48000
    N = 24000 #start at 24000 samples
    
    n = np.arange(N)
    
    f = np.array([100, 1000, 5000, 15000, 23000])
    
    x = np.zeros(N)
    
    for freq in f:
        x += 0.2 * np.sin(hz_to_omega(freq, fs) * n)
    
    
    #x[n] = sin(omega * n)
    print(x.shape, x.dtype, np.max(np.abs(x)))
    
    #plot_dtft(x)
    
    
    M = np.array([10, 100, 1000, 10000])
    
    #for m in M:
        #plot_dtft(lowpass(np.pi/4, m))
        
    #plot_dtft(bandpass(np.pi/4, np.pi, 10000))
    #to produce an actual bandpass instead of a lowpass, wc < wh < pi-wc


    x = make_test_signal(8000, 0.5, freqs=(500, 1500, 2800, 3500))
    y = rate_conversion(x, 3, 4, 200)
    
    #plot_dtft(y)
    
    M = 1000
    
    imp = np.zeros(4*M+1)
    imp[0] = 1
    #plot_dtft(equalizer(imp, 44100, M, 1, 1, 1))

    #plot_dtft(equalizer(imp, 44100, M, 1, 0, 0))
    
    #plot_dtft(equalizer(imp, 44100, M, 0, 1, 0))
    
    #plot_dtft(equalizer(imp, 44100, M, 0, 0, 1))


    data, sr = sf.read('funk.mp3')
    if data.ndim == 2:
        data = data.mean(axis=1) #sum to mono
    assert sr == 48000
    
    x = data[:15*48000]
    
    converted_x = rate_conversion(x, 147, 160, 1000)
    
    equalizer_result = equalizer(converted_x, 44100, 1000, 6, 1, 1) 
    
    sf.write('output.wav', equalizer_result, 44100)
    #for this example i made it bass boosted
    
    
    
    
    
