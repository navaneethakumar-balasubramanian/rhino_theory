import numpy as np
from scipy import signal


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
                 rho=7200,
                 beta=2368):
        self.Ro = Ro
        self.Ri = Ri
        self.Rb = Rb
        self.alpha = alpha
        self.rho = rho
        self.beta = beta

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
    def Z1_axial(self):
        """
        Steel impedance.
        """
        return self.Ab * self.rho * self.alpha * 0.00001

    @property
    def Z1_tangential(self):
        """
        Steel impedance.
        """
        return self.Ab * self.rho * self.beta * 0.00001

class Rock(object):
    """
    Args:
        alpha (np.array or float): Velocity of the rock.
        rho (np.array or float): Density of the rock.
    """

    def __init__(self, alpha=None, rho=None, beta=None):
        self.alpha = alpha
        self.rho = rho
        self.beta = beta


class TheoreticalWavelet(object):
    def __init__(self, pipe, rock, frequencies):
        self.rock = rock
        self.pipe = pipe
        self.frequencies = frequencies

        self.k = 2 * np.pi * self.frequencies / self.rock.alpha  # wave_number
        self.cot_phi = -1 * (self.k * self.pipe.Rb * (1 + 6 * np.sqrt(3)) / 12)

        if not (type(self.frequencies) in (int, float)):
            self.symmetric_frequencies = np.r_[-frequencies[1:-1][::-1], frequencies]
            self.nyquist = self.frequencies.max()
            self.max_frequency = self.nyquist * 2
            self.time_sampling = 1 / self.max_frequency


    def get_time_range_for_window(self, window):
        time_sampling_window = (np.arange(
                0 - (window / 2 * self.time_sampling),
                0 + (window / 2 * self.time_sampling),   self.time_sampling,)* 1000)
        return time_sampling_window

    @property
    def Zb(self):
        return (
            ((self.pipe.Ab * self.rock.rho * self.rock.alpha) / (self.k * self.pipe.Rb))
            / (1j - self.cot_phi)
            * 0.00001
        )

    @property
    def Zb_tangential(self):
        return (
            ((self.pipe.Ab * self.rock.rho * self.rock.beta) / (self.k * self.pipe.Rb))
            / (1j - self.cot_phi)
            * 0.00001) * (2*np.pi*self.frequencies/self.pipe.Rb)

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
        # jamies implementation
        RC_complex_real = (self.pipe.Z1_axial*self.Zb.real*(self.pipe.Z1_axial-self.Zb.real) + self.pipe.Z1_axial * self.Zb.imag**2) / ((self.pipe.Z1_axial + self.Zb.real)**2 + (self.Zb.imag)**2)
        RC_complex_imag = (self.pipe.Z1_axial*self.Zb.imag * (self.pipe.Z1_axial - self.Zb.real)) / ((self.pipe.Z1_axial + self.Zb.real)**2 + (self.Zb.imag)**2)
        RC_complex = RC_complex_real + RC_complex_imag * 1j

        # RC_complex = (self.pipe.Z1_axial * self.Zb) / (self.pipe.Z1_axial + self.Zb)

        if not (type(self.frequencies) in (int, float)):
            RC_complex = self._fill_complex_nans(RC_complex)

        return RC_complex

    @property
    def primary_in_frequency_domain_complex_tangential(self):
        # jamies implementation
        RC_complex_real = (self.pipe.Z1_tangential*self.Zb_tangential.real*(self.pipe.Z1_tangential-self.Zb_tangential.real) + self.pipe.Z1_tangential * self.Zb_tangential.imag**2) / ((self.pipe.Z1_tangential + self.Zb_tangential.real)**2 + (self.Zb_tangential.imag)**2)
        RC_complex_imag = (self.pipe.Z1_tangential*self.Zb_tangential.imag * (self.pipe.Z1_tangential - self.Zb_tangential.real)) / ((self.pipe.Z1_tangential + self.Zb_tangential.real)**2 + (self.Zb_tangential.imag)**2)
        RC_complex = RC_complex_real - RC_complex_imag * 1j

        # RC_complex = (self.pipe.Z1_axial * self.Zb) / (self.pipe.Z1_axial + self.Zb)

        if not (type(self.frequencies) in (int, float)):
            RC_complex = self._fill_complex_nans(RC_complex)

        return RC_complex


    @property
    def reflected_in_frequency_domain_complex(self):

        #brunos implementation
        RC_complex = (self.pipe.Z1_axial - self.Zb) / (self.pipe.Z1_axial + self.Zb)
        if not (type(self.frequencies) in (int, float)):
            RC_complex = self._fill_complex_nans(RC_complex)
        return RC_complex

    @property
    def reflected_in_frequency_domain_complex_tangential(self):

        #brunos implementation
        RC_complex = (self.pipe.Z1_tangential - self.Zb_tangential) / (self.pipe.Z1_tangential + self.Zb_tangential)
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
    def primary_in_frequency_domain_tangential(self):
        """
        returns: (amplitude, phase)
        """
        RC_complex = self.primary_in_frequency_domain_complex_tangential
        return (np.abs(RC_complex)), (np.arctan(RC_complex.imag / RC_complex.real))

    @property
    def reflected_in_frequency_domain(self):
        """
        returns: (amplitude, phase)
        """
        RC_complex = self.reflected_in_frequency_domain_complex
        return (np.abs(RC_complex)), (np.arctan(RC_complex.imag / RC_complex.real))

    @property
    def reflected_in_frequency_domain_tangential(self):
        """
        returns: (amplitude, phase)
        """
        RC_complex = self.reflected_in_frequency_domain_complex_tangential
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
        freq_domain_real = np.r_[freq_domain.real, freq_domain.real[:-1][::-1]][:-1]
        freq_domain_imag = np.r_[freq_domain.imag, freq_domain.imag[:-1][::-1]][:-1]

        freq_domain_imag[int(len(freq_domain_imag) / 2) :] = -freq_domain_imag[
            int(len(freq_domain_imag) / 2) :
        ]

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
        """
        """
        time_domain = self._wavelet_to_timedomain(
            *self.primary_in_frequency_domain
        ).real
        if window:
            center_index = int(time_domain.shape[0] / 2)
            time_domain = time_domain[
                center_index - int(window / 2) : center_index + int(window / 2)
            ]
        if resample:
            return signal.resample(time_domain, resample)
        else:
            return time_domain

    def primary_in_time_domain_tangential(self, window=None, resample=None):
        """
        """
        time_domain = self._wavelet_to_timedomain(
            *self.primary_in_frequency_domain_tangential
        ).real
        if window:
            center_index = int(time_domain.shape[0] / 2)
            time_domain = time_domain[
                center_index - int(window / 2) : center_index + int(window / 2)
            ]
        if resample:
            return signal.resample(time_domain, resample)
        else:
            return time_domain

    def reflected_in_time_domain(self, window=None, resample=None):
        """
        """
        time_domain = self._wavelet_to_timedomain(
            *self.reflected_in_frequency_domain
        ).real
        if window:
            center_index = int(time_domain.shape[0] / 2)
            time_domain = time_domain[
                center_index - int(window / 2) : center_index + int(window / 2)
            ]
        if resample:
            return signal.resample(time_domain, resample)
        else:
            return time_domain

    def reflected_in_time_domain_tangential(self, window=None, resample=None):
        """
        """
        time_domain = self._wavelet_to_timedomain(
            *self.reflected_in_frequency_domain_tangential
        ).real
        if window:
            center_index = int(time_domain.shape[0] / 2)
            time_domain = time_domain[
                center_index - int(window / 2) : center_index + int(window / 2)
            ]
        if resample:
            return signal.resample(time_domain, resample)
        else:
            return time_domain

    def multiple_in_time_domain(self, window=None, resample=None):
        primary, reflected = (
            self.primary_in_time_domain(window),
            self.reflected_in_time_domain(window),
        )
        convolved = signal.convolve(primary, reflected, mode="same", method="direct")
        if resample:
            return signal.resample(convolved, resample)
        else:
            return convolved

    def multiple_in_time_domain_tangential(self, window=None, resample=None):
        primary, reflected = (
            self.primary_in_time_domain_tangential(window),
            self.reflected_in_time_domain_tangential(window),
        )
        convolved = signal.convolve(primary, reflected, mode="same", method="direct")
        if resample:
            return signal.resample(convolved, resample)
        else:
            return convolved
