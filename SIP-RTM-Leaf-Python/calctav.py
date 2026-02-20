"""
calctav.py

Stern F. (1964), Transmission of isotropic radiation across an
interface between two dielectrics, Appl. Opt., 3(1):111-113.
Allen W.A. (1973), Transmission of isotropic light across a
dielectric surface in two and three dimensions, J. Opt. Soc. Am.,
63(6):664-666.
"""

import numpy as np


def calctav(alfa, nr):
    """
    Calculate the average transmittivity of a dielectric plane surface
    over the hemisphere for an angle of incidence alfa.

    Parameters
    ----------
    alfa : float
        Angle of incidence (degrees).
    nr : np.ndarray
        Refractive index array.

    Returns
    -------
    tav : np.ndarray
        Average transmittivity.
    """
    rd = np.pi / 180.0
    n2 = nr ** 2
    npx = n2 + 1       # 'np' in MATLAB; renamed to avoid shadowing numpy
    nm = n2 - 1
    a = (nr + 1) * (nr + 1) / 2.0
    k = -(n2 - 1) * (n2 - 1) / 4.0
    sa = np.sin(alfa * rd)

    b1 = (alfa != 90) * np.sqrt((sa ** 2 - npx / 2.0) ** 2 + k)
    b2 = sa ** 2 - npx / 2.0
    b = b1 - b2
    b3 = b ** 3
    a3 = a ** 3
    ts = (k ** 2 / (6.0 * b3) + k / b - b / 2.0) - \
         (k ** 2 / (6.0 * a3) + k / a - a / 2.0)

    tp1 = -2.0 * n2 * (b - a) / (npx ** 2)
    tp2 = -2.0 * n2 * npx * np.log(b / a) / (nm ** 2)
    tp3 = n2 * (1.0 / b - 1.0 / a) / 2.0
    tp4 = 16.0 * n2 ** 2 * (n2 ** 2 + 1) * \
          np.log((2.0 * npx * b - nm ** 2) / (2.0 * npx * a - nm ** 2)) / \
          (npx ** 3 * nm ** 2)
    tp5 = 16.0 * n2 ** 3 * \
          (1.0 / (2.0 * npx * b - nm ** 2) - 1.0 / (2.0 * npx * a - nm ** 2)) / \
          (npx ** 3)
    tp = tp1 + tp2 + tp3 + tp4 + tp5
    tav = (ts + tp) / (2.0 * sa ** 2)

    return tav
