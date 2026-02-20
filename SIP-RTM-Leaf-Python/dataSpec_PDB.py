"""
dataSpec_PDB.py

Loads the specific absorption coefficient data for leaf biochemical constituents.

Columns:
    [0] = wavelength (nm)
    [1] = refractive index of leaf material
    [2] = specific absorption coefficient of chlorophyll (a+b) (cm2.microg-1)
    [3] = specific absorption coefficient of carotenoids (cm2.microg-1)
    [4] = specific absorption coefficient of Anthocyanins (cm2.microg-1)
    [5] = specific absorption coefficient of brown pigments (arbitrary units)
    [6] = specific absorption coefficient of water (cm-1)
    [7] = specific absorption coefficient of dry matter (cm2.g-1)

Reference:
    Feret, Gitelson, Noble & Jacquemoud (2017). PROSPECT-D: Towards modeling
    leaf optical properties through a complete lifecycle.
    Remote Sensing of Environment, 193:204-215
    DOI: http://doi.org/10.1016/j.rse.2017.03.004
"""

import os
import numpy as np


def dataSpec_PDB():
    """
    Load and return the specific absorption coefficient data.

    Returns
    -------
    data : np.ndarray
        Array of shape (2101, 8) with spectral data from 400-2500 nm.
    """
    data_path = os.path.join(os.path.dirname(__file__), "dataSpec_PDB.csv")
    data = np.loadtxt(data_path, delimiter=",")
    return data
