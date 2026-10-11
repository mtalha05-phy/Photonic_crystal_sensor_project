# Research Extension Questions

Use these questions to turn the baseline project into a stronger research study.

## Q1 — How does the number of periods affect resonance quality?
N = 2, 3, 5, 7, 10

Measure:
- resonance wavelength
- peak transmission
- full width at half maximum (FWHM)
- Q-factor = lambda_res / FWHM

## Q2 — How does defect thickness affect sensitivity?
Test:
150, 200, 250, 300, 350 nm

For each case:
- sweep sensing index
- calculate resonance shift
- calculate sensitivity

## Q3 — Which operating wavelength is best?
Repeat the simulation using different material/index combinations so the resonance occurs in visible or near-infrared bands.

## Q4 — Can sensitivity and spectral sharpness be optimized simultaneously?
Define an objective such as:

FOM = Sensitivity / FWHM

Then search over defect thickness and number of periods.

## Q5 — How robust is the design?
Introduce small random thickness errors, e.g. ±1%, ±2%, ±5%, and repeat the simulation.

This moves the project toward fabrication-tolerance analysis.

## Q6 — What changes when realistic material dispersion is included?
Replace constant refractive indices with wavelength-dependent data from reliable literature/databases. Clearly cite the source of every material dataset.
