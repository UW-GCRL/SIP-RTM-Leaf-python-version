"""
sip_model.py

SIP (Spectral Invariants Parameters) leaf radiative transfer model.
Version 1.0 (November, 5th 2020)

Simulates leaf spectra properties from 400 nm to 2500 nm with 1 nm interval.

Input:
    Cab    = chlorophyll a+b content (ug/cm2)
    Car    = carotenoids content (ug/cm2)
    Ant    = Anthocyanin content (ug/cm2)
    Brown  = brown pigments content (arbitrary units)
    Cw     = equivalent water thickness (g/cm2 or cm)
    Cm     = dry matter content (g/cm2)

Output:
    LRT    = [wavelength, single scattering albedo, reflectance, transmittance]

Reference:
    Wu S., Zeng Y., Hao D., Liu Q., Li J., Chen X., R.Asrar G., Yin G.,
    Wen J., Yang B., Zhu P., Chen M., 2020. Quantifying leaf optical
    properties with spectral invariants theory.
    DOI: https://doi.org/10.1016/j.rse.2020.112131

Acknowledgement:
    The authors thank the PROSPECT team for providing the specific absorption
    coefficient in calctav and dataSpec_PDB.
"""

import numpy as np
from dataSpec_PDB import dataSpec_PDB


def SIP_Model(Cab, Car, Ant, Brown, Cw, Cm):
    """
    Run the SIP leaf radiative transfer model.

    Parameters
    ----------
    Cab   : float  – chlorophyll a+b content (ug/cm2)
    Car   : float  – carotenoids content (ug/cm2)
    Ant   : float  – Anthocyanin content (ug/cm2)
    Brown : float  – brown pigments content (arbitrary units)
    Cw    : float  – equivalent water thickness (g/cm2 or cm)
    Cm    : float  – dry matter content (g/cm2)

    Returns
    -------
    LRT : np.ndarray
        Array of shape (2101, 4) with columns:
        [wavelength(nm), single scattering albedo, reflectance, transmittance]
    """
    alpha = 600.0  # constant for the optimal size of the leaf scattering element

    # input specific absorption coefficient
    data = dataSpec_PDB()
    wavelength = data[:, 0]
    nr = data[:, 1]         # refractive index (not used in SIP model directly)
    Kab = data[:, 2]
    Kcar = data[:, 3]
    Kant = data[:, 4]
    KBrown = data[:, 5]
    Kw = data[:, 6]
    Km = data[:, 7]

    Kall = (Cab * Kab + Car * Kcar + Ant * Kant + Brown * KBrown +
            Cw * Kw + Cm * Km) / (Cm * alpha)
    w0 = np.exp(-Kall)

    # spectral invariant parameters
    eps = np.finfo(float).eps   # machine epsilon, equivalent to MATLAB eps
    fLMA = 2765.0 * Cm
    gLMA = 102.8 * Cm
    p = 1.0 - (1.0 - np.exp(-fLMA)) / (fLMA + eps)
    q = 1.0 - 2.0 * np.exp(-gLMA)
    qabs = np.sqrt(q ** 2)      # equivalent to abs(q)

    # leaf single scattering albedo
    w = w0 * (1.0 - p) / (1.0 - p * w0 + eps)

    # leaf reflectance and leaf transmittance
    refl = w * (0.5 + q / 2.0 * (1.0 - p * w0) / (1.0 - qabs * p * w0))
    tran = w * (0.5 - q / 2.0 * (1.0 - p * w0) / (1.0 - qabs * p * w0))

    LRT = np.column_stack([wavelength, w, refl, tran])

    return LRT
