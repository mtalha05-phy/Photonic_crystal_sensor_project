# Numerical Study of a Photonic Crystal Structure for Refractive-Index Sensing

## Project goal
This project investigates a one-dimensional dielectric photonic crystal as a simple refractive-index sensor. The model calculates the transmission spectrum using the transfer-matrix method (TMM), sweeps the refractive index of a defect/cavity layer, and estimates wavelength sensitivity.

## Research question
How does a small change in the refractive index of an optical sensing region shift the resonant transmission wavelength?

## Physics
A periodic multilayer creates photonic band gaps. Introducing a defect layer inside the periodic structure produces a localized transmission resonance. If the refractive index of the defect/sensing layer changes, the optical phase accumulated in that layer changes and the resonance wavelength shifts.

The basic optical phase condition is related to:

    2 n L cos(theta) = m lambda

so, for fixed geometry and mode order, a change in n can shift lambda.

## Model used
- Normal incidence
- Lossless, non-magnetic dielectric layers in the baseline model
- Alternating layers A/B
- A central defect/sensing layer
- Transfer Matrix Method
- Wavelength sweep
- Refractive-index sweep
- Resonance detection
- Linear sensitivity fit

## Baseline structure
(A/B)^N / Defect / (B/A)^N

Default parameters:
- Layer A refractive index: 1.45
- Layer B refractive index: 2.00
- A thickness: 120 nm
- B thickness: 90 nm
- Defect thickness: 250 nm
- Number of periods on each side: 5
- Sensing index: 1.33
- Wavelength range: 500–900 nm

## Run

Create a virtual environment if desired:

    python -m venv .venv

Windows:
    .venv\Scripts\activate

Linux/macOS:
    source .venv/bin/activate

Install:
    pip install -r requirements.txt

Run:
    python src/photonic_crystal_sensor.py

The program generates:
- transmission_spectrum.png
- resonance_shift.png
- sensitivity_fit.png
- results.csv

## What to investigate
Do not stop at the default plots. Repeat the study by changing:
1. Sensing refractive index
2. Defect-layer thickness
3. Number of periods
4. Layer refractive indices
5. Wavelength range

## Main performance metric
Bulk refractive-index sensitivity:

    S = Delta(lambda_res) / Delta(n)

Unit: nm/RIU

where RIU means refractive-index unit.

## Important limitation
This is a 1D educational/research-grade numerical model, not a full 2D/3D electromagnetic solver. For a stronger paper, validate selected cases against an analytical/independent model or FEM/FDTD software such as COMSOL or Lumerical when available.

## Suggested final title
"Numerical Investigation of a One-Dimensional Photonic Crystal for Refractive-Index Sensing Using the Transfer Matrix Method"
