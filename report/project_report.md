# Numerical Investigation of a One-Dimensional Photonic Crystal for Refractive-Index Sensing

## Abstract
A numerical model of a one-dimensional dielectric photonic crystal is developed to investigate refractive-index sensing. The structure consists of alternating dielectric layers surrounding a central defect/sensing layer. The Transfer Matrix Method (TMM) is used to calculate the wavelength-dependent transmission spectrum. By varying the refractive index of the sensing region, the shift of the defect-mode resonance is tracked. The resonance shift is then used to estimate bulk refractive-index sensitivity in nm/RIU. The project demonstrates how multilayer photonic structures can be studied computationally using Python.

## 1. Introduction
Photonic crystals are periodic optical structures that control electromagnetic-wave propagation through interference. Their periodicity can produce photonic band gaps in which propagation is strongly suppressed. A defect introduced into an otherwise periodic structure can create a localized optical mode inside a band gap.

This property can be used for sensing. When the refractive index of the defect/sensing region changes, the optical phase inside the region changes. Consequently, the resonant wavelength moves. Measuring or calculating this wavelength shift provides a method of refractive-index sensing.

## 2. Research question
How does changing the refractive index of a defect/sensing layer affect the resonance wavelength of a one-dimensional photonic crystal?

## 3. Objectives
1. Build a transfer-matrix model of a 1D photonic crystal.
2. Calculate its transmission spectrum.
3. Introduce a central sensing/defect layer.
4. Sweep the sensing refractive index.
5. Extract the resonance wavelength.
6. Calculate sensitivity in nm/RIU.
7. Examine the linearity of the resonance shift.
8. Identify parameters that can improve sensor performance.

## 4. Structure
The simulated structure is:

(A/B)^N / Defect / (B/A)^N

where A and B are dielectric layers and the defect layer is the sensing region.

Baseline parameters:
- n_A = 1.45
- n_B = 2.00
- d_A = 120 nm
- d_B = 90 nm
- defect thickness = 250 nm
- N = 5 periods per side
- sensing-index range = 1.30–1.38
- wavelength range = 500–900 nm

## 5. Numerical method

For a dielectric layer, the characteristic matrix at normal incidence is

M = [[cos(delta), i sin(delta)/n],
     [i n sin(delta), cos(delta)]]

where

delta = 2*pi*n*d/lambda.

The matrices of all layers are multiplied in sequence:

M_total = M_1 M_2 ... M_N

The transmission coefficient is then obtained from the total matrix. The implementation in `src/photonic_crystal_sensor.py` performs this calculation for every wavelength.

## 6. Resonance extraction
A transmission resonance is identified as a local maximum in the calculated spectrum. The strongest relevant transmission peak is used as the resonance wavelength for the baseline model.

## 7. Sensitivity
The bulk refractive-index sensitivity is defined as:

S = Delta(lambda_res) / Delta(n)

where lambda_res is the resonance wavelength and n is the sensing refractive index.

A linear regression of resonance wavelength against refractive index provides an estimated sensitivity and R² value.

## 8. Results
Run the program before finalizing this section. Copy the numerical values from `results/summary.txt` and insert the generated figures:

- `results/transmission_spectrum.png`
- `results/resonance_shift.png`
- `results/sensitivity_fit.png`

Discuss:
1. Where the defect resonance appears.
2. Whether the resonance shifts monotonically.
3. Whether the shift is approximately linear.
4. The calculated sensitivity.
5. The limitations of the model.

## 9. Further parameter studies
A stronger research version should investigate:

### 9.1 Number of periods
Compare N = 2, 3, 5, 7, 10.

Questions:
- Does the resonance become narrower?
- Does the transmission peak change?
- Does the spectral resolution improve?

### 9.2 Defect thickness
Compare defect thicknesses such as:
150, 200, 250, 300, 350 nm.

Questions:
- How does the resonance position change?
- Does the resonance move into or out of the chosen wavelength window?

### 9.3 Refractive-index contrast
Change n_A and n_B.

Questions:
- How does stronger index contrast affect the band gap?
- Does it alter resonance visibility?

### 9.4 Sensing-index range
Use a smaller range around the expected operating point, e.g. 1.330–1.335, to estimate local sensitivity.

## 10. Discussion
The simulation demonstrates the fundamental sensing mechanism: the refractive index of the defect region modifies the optical phase and shifts the resonance. A practical sensor would need an optical source, detector, and a method of identifying the resonance wavelength. Environmental temperature, fabrication tolerances, absorption, surface roughness, and material dispersion could also influence the result.

The present model assumes ideal lossless, nondispersive materials and normal incidence. These assumptions should be stated clearly rather than presenting the simulation as a complete experimental sensor model.

## 11. Conclusion
A one-dimensional photonic crystal refractive-index sensor can be modeled using the Transfer Matrix Method with a standard Python environment. The project provides a computational framework for studying photonic band gaps, defect modes and resonance-based sensing. The next stage is to perform a systematic parameter optimization and validate selected cases using an independent electromagnetic solver.

## 12. Future work
- Add wavelength-dependent refractive indices.
- Include material absorption.
- Model oblique incidence and TE/TM polarization.
- Optimize layer thicknesses automatically.
- Calculate Q-factor and figure of merit.
- Add a 2D/3D electromagnetic model.
- Compare TMM results with COMSOL/FDTD.
- Investigate specific sensing materials and realistic analytes.
