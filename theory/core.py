import numpy as np
from scipy import signal

class Pipe(object):
    '''
    Args:
        Ro (np.array or float): Outer radius of pipe
        Ri (np.array or float): Inner radius of pipe
        Rb (np.array or float): Effective bit radius contacting rock (m)
        alpha (np.array or float): Axial velocity of the drill stem.
        rho (np.array or float): Density of the drill stem.
    '''
    def __init__(self,
             Ro=.1365,
             Ri=.0687,
             Rb=.16,
             alpha=4875,
             rho=7800
                ):
        self.Ro = Ro
        self.Ri = Ri
        self.Rb = Rb
        self.alpha = alpha
        self.rho = rho

    @property
    def A1(self):
        '''
        Effective drill stem area.
        '''
        return np.pi*((self.Ro**2)-(self.Ri**2))

    @property
    def Ab(self):
        '''
        Area of the bit contacting rock.
        '''
        return np.pi * (self.Rb**2)

    @property
    def Z1(self):
        '''
        Steel impedance.
        '''
        return self.Ab * self.rho * self.alpha * 0.00001


class Rock(object):
    '''
    Args:
        alpha (np.array or float): Velocity of the rock.
        rho (np.array or float): Density of the rock.
    '''
    def __init__(self, alpha, rho):
        self.alpha = alpha
        self.rho = rho


class TheoreticalWavelet(object):
    def __init__(self, pipe, rock, frequencies):
        self.rock = rock
        self.pipe = pipe
        self.frequencies = frequencies
        self.symmetric_frequencies = np.r_[-frequencies[1:-1][::-1], frequencies]

        self.k = 2 * np.pi * self.frequencies / self.rock.alpha # wave_number
        self.cot_phi = -1 * (self.k * self.pipe.Rb * (1+6*np.sqrt(3))/12)

        self.nyquist = self.frequencies.max()
        self.max_frequency = self.nyquist * 2
        self.time_sampling = 1 / self.max_frequency

    @property
    def Zb(self):
        return ((self.pipe.Ab * self.rock.rho * self.rock.alpha) / (
            self.k * self.pipe.Rb)) / (1j - self.cot_phi) * .00001

    @property
    def wave_number(self):
        return self.k

    @classmethod
    def _fill_complex_nans(cls, complex_array):
        if np.isnan(complex_array[0]):
            inds = np.indices(complex_array.shape).ravel()
            complex_array.real[0] = np.interp(0, inds[1:], complex_array.real[1:])
            complex_array.imag[0] = np.interp(0, inds[1:], complex_array.imag[1:])
        return complex_array

    @property
    def primary_in_frequency_domain(self):
        '''
        returns: (amplitude, phase)
        '''
        RC_complex = (self.pipe.Z1 * self.Zb) / (self.pipe.Z1 + self.Zb)
        RC_complex = self._fill_complex_nans(RC_complex)
        return (np.abs(RC_complex)), (np.arctan(RC_complex.imag/RC_complex.real))

    @property
    def reflected_in_frequency_domain(self):
        '''
        returns: (amplitude, phase)
        '''
        RC_complex = (self.pipe.Z1 - self.Zb) / (self.pipe.Z1 + self.Zb)
        RC_complex = self._fill_complex_nans(RC_complex)
        return (np.abs(RC_complex)), (np.arctan(RC_complex.imag/RC_complex.real))

    @classmethod
    def amp_phase2complex(cls, amplitude, phase):
        '''
        Convert amplitude and phase to a complex array.
        '''
        freq_domain = amplitude * np.cos(phase) + (amplitude * np.sin(phase)) * 1j

        # Quick hack to make array symmetric and imaginary part be flipped
        freq_domain_real = np.r_[freq_domain.real, freq_domain.real[:-1][::-1]][:-1]
        freq_domain_imag = np.r_[freq_domain.imag, freq_domain.imag[:-1][::-1]][:-1]

        freq_domain_imag[int(len(freq_domain_imag)/2):] = - freq_domain_imag[int(len(freq_domain_imag)/2):]

        # freq_domain_imag[self.symmetric_frequencies == 0

        return freq_domain_real + freq_domain_imag * 1j

    @classmethod
    def inverse_transform(cls, complex_array):
        time_domain = np.fft.ifft(complex_array)
        return np.fft.fftshift(time_domain)

    def _wavelet_to_timedomain(self, amplitude, phase):
        complex_array = self.amp_phase2complex(amplitude, phase)
        return self.inverse_transform(complex_array)

    def primary_in_time_domain(self, window=None, resample=None):
        '''
        '''
        time_domain = self._wavelet_to_timedomain(*self.primary_in_frequency_domain).real
        if window:
            center_index = int(time_domain.shape[0]/2)
            time_domain = time_domain[center_index-int(window/2):center_index+int(window/2)]
        if resample:
            return signal.resample(time_domain, resample)
        else:
            return time_domain

    def reflected_in_time_domain(self, window=None, resample=None):
        '''
        '''
        time_domain = self._wavelet_to_timedomain(*self.reflected_in_frequency_domain).real
        if window:
            center_index = int(time_domain.shape[0]/2)
            time_domain = time_domain[center_index-int(window/2):center_index+int(window/2)]
        if resample:
            return signal.resample(time_domain, resample)
        else:
            return time_domain

    def multiple_in_time_domain(self, window=None, resample=None):
        primary, reflected = (
            self.primary_in_time_domain(window),
            self.reflected_in_time_domain(window))
        convolved = signal.convolve(primary, reflected, mode='same', method='direct')
        if resample:
            return signal.resample(convolved, resample)
        else:
            return convolved
