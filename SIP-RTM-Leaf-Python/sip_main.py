"""
sip_main.py

Main function for the SIP leaf radiative transfer model.
Version 1.0 (November, 5th 2020)

For any question or request, please contact:
    Dr. Yelu Zeng & Dr. Min Chen
    Joint Global Change Research Institute, PNNL, College Park, MD 20740, USA
    E-mail: zengyelu@163.com & chenminbnu@gmail.com

    Dr. Shengbiao Wu & Dr. Dalei Hao
    E-mail: wushengbiao90@163.com & dalei.hao.93@gmail.com

    https://github.com/chenminbnu/SIP-RTM-Leaf

Simulates leaf spectra properties from 400 nm to 2500 nm with 1 nm interval.
Input:
    Cab    = chlorophyll a+b content (ug/cm2)
    Car    = carotenoids content (ug/cm2)
    Anth   = Anthocyanin content (ug/cm2)
    Cbrown = brown pigments content (arbitrary units)
    Cw     = equivalent water thickness (g/cm2 or cm)
    Cm     = dry matter content (g/cm2)
Output:
    leaf single scattering albedo, reflectance and transmittance

Reference:
    Wu S., Zeng Y., Hao D., Liu Q., Li J., Chen X., R.Asrar G., Yin G.,
    Wen J., Yang B., Zhu P., Chen M., 2020. Quantifying leaf optical
    properties with spectral invariants theory.
    DOI: https://doi.org/10.1016/j.rse.2020.112131
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from sip_model import SIP_Model


def SIP_Main(do_plot=True):
    """Run the SIP model and optionally plot results."""

    # input leaf structural and biochemical traits
    param_path = os.path.join(os.path.dirname(__file__), "leaf_parameter.txt")
    leaf_parameter = np.loadtxt(param_path)
    Cab    = leaf_parameter[0]
    Car    = leaf_parameter[1]
    Anth   = leaf_parameter[2]
    Cbrown = leaf_parameter[3]
    Cw     = leaf_parameter[4]
    Cm     = leaf_parameter[5]

    LRT = SIP_Model(Cab, Car, Anth, Cbrown, Cw, Cm)

    # write output file
    out_path = os.path.join(os.path.dirname(__file__), "leaf_spectrum.txt")
    with open(out_path, "w") as f:
        f.write("Wavelength(nm)\tsingle scattering albedo\tReflectance\tTransmittance\n")
        for i in range(LRT.shape[0]):
            f.write(f"{int(LRT[i, 0])}\t{LRT[i, 1]:.3f}\t{LRT[i, 2]:.3f}\t{LRT[i, 3]:.3f}\n")

    if do_plot:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        # --- Left panel: leaf single scattering albedo ---
        ax1.scatter(LRT[:, 0], LRT[:, 1], s=4)
        ax1.set_xlim(400, 2400)
        ax1.set_xticks(range(400, 2401, 400))
        ax1.set_ylim(0, 1)
        ax1.set_yticks(np.arange(0, 1.01, 0.2))
        ax1.set_yticklabels(["0.0", "0.2", "0.4", "0.6", "0.8", "1.0"])
        ax1.set_xlabel("Wavelength (nm)", fontsize=14)
        ax1.set_ylabel("Leaf single scattering albedo", fontsize=14)
        ax1.tick_params(labelsize=14)
        for spine in ax1.spines.values():
            spine.set_linewidth(1.2)

        # --- Right panel: reflectance (left y) and transmittance (right y) ---
        ax2.scatter(LRT[:, 0], LRT[:, 2], s=4, color="tab:blue", label="Reflectance")
        ax2.set_xlim(400, 2400)
        ax2.set_xticks(range(400, 2401, 400))
        ax2.set_ylim(0, 1)
        ax2.set_yticks(np.arange(0, 1.01, 0.2))
        ax2.set_yticklabels(["0.0", "0.2", "0.4", "0.6", "0.8", "1.0"])
        ax2.set_xlabel("Wavelength (nm)", fontsize=14)
        ax2.set_ylabel("Leaf reflectance", fontsize=14, color="tab:blue")
        ax2.tick_params(labelsize=14)

        # transmittance on twin y-axis (inverted, matching MATLAB code: 1 - tran)
        ax2r = ax2.twinx()
        ax2r.scatter(LRT[:, 0], 1.0 - LRT[:, 3], s=4, color="tab:orange", label="Transmittance")
        ax2r.set_ylim(0, 1)
        ax2r.set_yticks(np.arange(0, 1.01, 0.2))
        ax2r.set_yticklabels(["1.0", "0.8", "0.6", "0.4", "0.2", "0.0"])
        ax2r.set_ylabel("Leaf transmittance", fontsize=14, color="tab:orange")
        ax2r.tick_params(labelsize=14)

        for spine in ax2.spines.values():
            spine.set_linewidth(1.2)
        for spine in ax2r.spines.values():
            spine.set_linewidth(1.2)

        plt.tight_layout()
        fig_path = os.path.join(os.path.dirname(__file__), "leaf_spectrum.png")
        plt.savefig(fig_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"Figure saved to {fig_path}")

    print(f"Output saved to {out_path}")
    return LRT


if __name__ == "__main__":
    SIP_Main()
