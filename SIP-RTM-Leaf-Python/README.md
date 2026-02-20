# SIP-RTM-Leaf (Python Version)

Python port of the SIP (Spectral Invariants Parameters) leaf radiative transfer model,
originally written in MATLAB by Wu et al. (2020).

## Requirements

- Python 3.7+
- NumPy
- Matplotlib

## Usage

```bash
python sip_main.py
```

This reads `leaf_parameter.txt` (6 values: Cab, Car, Anth, Cbrown, Cw, Cm),
runs the SIP model, writes `leaf_spectrum.txt`, and saves a plot to `leaf_spectrum.png`.

You can also use the model programmatically:

```python
from sip_model import SIP_Model

# Cab=30, Car=10, Anth=1.0, Cbrown=0.0, Cw=0.015, Cm=0.009
LRT = SIP_Model(30.0, 10.0, 1.0, 0.0, 0.015, 0.009)
# LRT columns: [wavelength(nm), single_scattering_albedo, reflectance, transmittance]
```

## File Description

| File               | Description                                              |
|--------------------|----------------------------------------------------------|
| `sip_main.py`      | Main script — reads parameters, runs model, plots output |
| `sip_model.py`     | Core SIP model (few lines beyond parameter loading)      |
| `calctav.py`       | Dielectric surface transmittivity (from PROSPECT)        |
| `dataSpec_PDB.py`  | Loads specific absorption coefficients from CSV          |
| `dataSpec_PDB.csv` | Spectral data: 400–2500 nm, 8 columns                   |
| `leaf_parameter.txt` | Input parameters                                       |
| `leaf_spectrum.txt`  | Output spectra (tab-separated)                         |

## Validation

Output has been verified to be **identical** to the original MATLAB version
(`diff` on `leaf_spectrum.txt` shows zero differences).

## Reference

Wu S., Zeng Y., Hao D., Liu Q., Li J., Chen X., R.Asrar G., Yin G.,
Wen J., Yang B., Zhu P., Chen M., 2020. Quantifying leaf optical
properties with spectral invariants theory.
DOI: https://doi.org/10.1016/j.rse.2020.112131
