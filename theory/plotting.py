import numpy as np
import matplotlib.pyplot as plt

def wiggle_plot(wavelets, offsets, time_range, gain=20, color='k', ax=None):

    if not ax:
        fig, ax = plt.subplots()

    y = time_range

    for offset, wavelet in zip(offsets,wavelets):
        x = ((wavelet - wavelet.mean()) / wavelet.std()) * gain + offset
        ax.plot(x, y ,'-', color=color)
        ax.fill_betweenx(y, offset, x, where=(x>=offset), color=color, interpolate=True)

    return fig, ax
