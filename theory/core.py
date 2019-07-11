import numpy as np
from scipy import signal

from dcrhino3.signal_processing.filters import FIRLSFilter

class Pipe(object):
    """
    Args:
        Ro (np.array or float): Outer radius of pipe
        Ri (np.array or float): Inner radius of pipe
        Rb (np.array or float): Effective bit radius contacting rock (m)
        alpha (np.array or float): Axial velocity of the drill stem.
        rho (np.array or float): Density of the drill stem.
    """

    def __init__(self, Ro=0.1365, Ri=0.0687, Rb=0.16, alpha=4875,
                 rho=7200, beta=2368, component='axial'):

        self.Ro = Ro
        self.Ri = Ri
        self.Rb = Rb
        self.alpha = alpha
        self.rho = rho
        self.beta = beta
        self.component = component

    @property
    def A1(self):
        """
        Effective drill stem area for axial.
        """
        return np.pi * ((self.Ro ** 2) - (self.Ri ** 2))

    @property
    def Ab(self):
        """
        Area of the bit contacting rock.
        """
        return np.pi * (self.Rb ** 2)

    @property
    def Z1(self):
        """
        Steel impedance.
        """
        if self.component == 'axial':
            return self.Ab * self.rho * self.alpha
        if self.component == 'tangential':
            return self.Ab * self.rho * self.beta

class Rock(object):
    """
    Args:
        alpha (np.array or float): Velocity of the rock.
        rho (np.array or float): Density of the rock.
    """

    def __init__(self, alpha=None, rho=None, beta=None, component='axial'):
        self.alpha = alpha
        self.rho = rho
        self.beta = beta


class TheoreticalWavelet(object):

    def __init__(self,
                 pipe,
                 rock,
                 frequency_resolution=0.5,
                 nyquist=5000,
                 filterby=[40, 50, 200, 240],
                 component='axial'):


        self.rock = rock
        self.pipe = pipe
        self.component = component

        self.pipe.component = component
        self.rock.component = component

        self.frequency_resolution = frequency_resolution
        self.nyquist = nyquist
        self.sampling_rate = 2 * nyquist
        self.sampling_interval = (1 / self.sampling_rate)
        self.number_of_samples = 1 / (self.frequency_resolution * self.sampling_interval)

        self.frequencies = np.arange(0, self.nyquist + self.frequency_resolution, self.frequency_resolution)

        if not (type(self.frequencies) in (int, float)):
            self.symmetric_frequencies = np.r_[-self.frequencies[1:-1][::-1], self.frequencies]

        if self.component == 'axial':
            self.k = 2 * np.pi * self.frequencies / self.rock.alpha  # wave_number
        if self.component == 'tangential':
            self.k = 2 * np.pi * self.frequencies / self.rock.beta  # wave_number

        self.cot_phi = -1 * (self.k * self.pipe.Rb * (1 + 6 * np.sqrt(3)) / 12)

        if filterby:
            corners = filterby

            filter_duration = 0.1
            firls = FIRLSFilter(corners, filter_duration)
            self.fir_taps = firls.make(self.sampling_rate)

    def get_time_range_for_window(self, window):
        time_sampling_window = (np.arange(
                0 - (window / 2 * self.sampling_interval),
                0 + (window / 2 * self.sampling_interval),   self.sampling_interval,)* 1000)
        return time_sampling_window

    @property
    def Zb(self):
        '''
        Elastic impedance of the rock. dens x Vp^2
        Measures compressional modulus.
        '''
        if self.component == 'axial':
            return (
                ((self.pipe.Ab * self.rock.rho * self.rock.alpha) / (self.k * self.pipe.Rb))
                / (1j - self.cot_phi))
        if self.component == 'tangential':
            array = (
                ((self.pipe.Ab * self.rock.rho * self.rock.beta) / (self.k * self.pipe.Rb))
                / (1j - self.cot_phi))
            return array


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
    def primary_in_frequency_domain_complex(self):

        RC_complex = (self.pipe.Z1 * self.Zb) / (self.pipe.Z1 + self.Zb)

        if not (type(self.frequencies) in (int, float)):
            RC_complex = self._fill_complex_nans(RC_complex)

        return (RC_complex)

    @property
    def reflected_in_frequency_domain_complex(self):

        #brunos implementation
        RC_complex = (self.pipe.Z1 - self.Zb) / (self.pipe.Z1 + self.Zb)
        if not (type(self.frequencies) in (int, float)):
            RC_complex = self._fill_complex_nans(RC_complex)
        return RC_complex


    @property
    def primary_in_frequency_domain(self):
        """
        returns: (amplitude, phase)
        """
        RC_complex = self.primary_in_frequency_domain_complex
        return (np.abs(RC_complex)), (np.arctan(RC_complex.imag / RC_complex.real))

    @property
    def reflected_in_frequency_domain(self):
        """
        returns: (amplitude, phase)
        """
        RC_complex = self.reflected_in_frequency_domain_complex
        return (np.abs(RC_complex)), (np.arctan(RC_complex.imag / RC_complex.real))


    @classmethod
    def make_symmetry_on_complex(cls, freq_domain):
        freq_domain_real = np.r_[freq_domain.real, freq_domain.real[:-1][::-1]][:-1]
        freq_domain_imag = np.r_[freq_domain.imag, freq_domain.imag[:-1][::-1]][:-1]

        freq_domain_imag[int(len(freq_domain_imag) / 2) :] = -freq_domain_imag[
            int(len(freq_domain_imag) / 2) :
        ]
        return freq_domain_real + freq_domain_imag * 1j

    @classmethod
    def amp_phase2complex(cls, amplitude, phase):
        """
        Convert amplitude and phase to a complex array.
        """
        freq_domain = amplitude * np.cos(phase) + (amplitude * np.sin(phase)) * 1j
        if (type(amplitude) in (int, float)):
            return freq_domain.real + freq_domain.imag * 1j
        # Quick hack to make array symmetric and imaginary part be flipped

        return cls.make_symmetry_on_complex(freq_domain)

    @classmethod
    def inverse_transform(cls, complex_array):
        complex_array = cls._fill_complex_nans(complex_array)
        time_domain = np.fft.ifft(complex_array)
        return np.fft.fftshift(time_domain)

    def _wavelet_to_timedomain(self, amplitude, phase):
        complex_array = self.amp_phase2complex(amplitude, phase)
        return self.inverse_transform(complex_array)

    def primary_in_time_domain(self, window=None, resample=None, skip_derivative=False, filtered=True):
        """
        """
        time_domain = self._wavelet_to_timedomain(
            *self.primary_in_frequency_domain
        ).real
        if self.component == 'tangential':
            if not skip_derivative:
                time_domain = np.gradient(time_domain, 1)
        if filtered:
            time_domain = signal.filtfilt(self.fir_taps, 1, time_domain)
        if window:
            center_index = int(time_domain.shape[0] / 2)
            time_domain = time_domain[
                center_index - int(window / 2) : center_index + int(window / 2)
            ]
        if resample:
            return signal.resample(time_domain, resample)
        else:
            return time_domain


    def reflected_in_time_domain(self, window=None, resample=None, skip_derivative=False, filtered=False):
        """
        """
        time_domain = self._wavelet_to_timedomain(
            *self.reflected_in_frequency_domain
        ).real
        if self.component == 'tangential':
            if not skip_derivative:
                time_domain = np.gradient(time_domain, 1)
        if filtered:
            time_domain = signal.filtfilt(self.fir_taps, 1, time_domain)
        if window:
            center_index = int(time_domain.shape[0] / 2)
            time_domain = time_domain[
                center_index - int(window / 2) : center_index + int(window / 2)
            ]
        if resample:
            return signal.resample(time_domain, resample)
        else:
            return time_domain


    def multiple_in_time_domain(self, window=None, resample=None, filtered=False):
        primary, reflected = (
            self.primary_in_time_domain(window, filtered=filtered),
            self.reflected_in_time_domain(window, skip_derivative=True, filtered=filtered),
        )
        convolved = signal.convolve(primary, reflected, mode="same", method="direct")
        if self.component == 'tangential':
            convolved = np.gradient(convolved, 1)
        if resample:
            return signal.resample(convolved, resample)
        else:
            return convolved

class MultipleWavelets(object):
    def __init__(self, rho_range=None, alpha_range=None, beta_range=None, pipe=None):
        pass


