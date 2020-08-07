import logging
import numpy as np
from scipy.signal import find_peaks, cwt, windows
from scipy.ndimage import label

logger = logging.getLogger(__name__)


def velocity_to_fracture_factor(
    velocity_array,
    spline_order=3,
    dspline=None,
    wavelets_widths=None,
    velocity_lower_threshold=None,
    velocity_upper_threshold=None,
    debug=False,
):
    """
    From a velocity array, detect fractures.
    """
    from obspy.signal import detrend

    dspline = int(len(velocity_array) / 25.0) if dspline is None else dspline
    wavelets_widths = (
        np.arange(1, int(len(velocity_array) / 50)) + 1
        if wavelets_widths is None
        else wavelets_widths
    )
    velocity_array_detrend = detrend.spline(
        velocity_array.copy(), spline_order, dspline
    )
    t = cwt(velocity_array_detrend, windows.triang, wavelets_widths)
    st = scale(t.min(0))
    st[st > 0.0] = 0.0
    if velocity_upper_threshold:
        st[velocity_array >= velocity_upper_threshold] = 0
    if velocity_lower_threshold:
        st[velocity_array < velocity_lower_threshold] = st.min()
    if debug:
        return minmax_scale(st), velocity_array_detrend, t
    return minmax_scale(st)


def fracture_factor_to_RQD(fracture_factor_array, sample_interval=0.01):
    """
    From Rhino Fracture Factor, compute RQD.
    """
    labels, nlabels = label(np.isclose(fracture_factor_array, 1))
    core_pieces = np.unique(labels, return_counts=True)[1][1:] * sample_interval
    valid_core_pieces = core_pieces[core_pieces > 0.1]
    return valid_core_pieces.sum() / (len(fracture_factor_array) * sample_interval)
