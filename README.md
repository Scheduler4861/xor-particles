# xor-particles

This repository contains a minimal theoretical framework describing particle-like structures as localized invariants in XOR-based causal dynamics.

## Paper

- [Read on GitHub (PDF)](./xor_local_invariants.pdf)
- [Read on Zenodo (DOI)](https://doi.org/10.5281/zenodo.19600725)

## Summary

We study a discrete binary lattice evolving under a local XOR operator.
Invariant observables are defined via weight functions satisfying a fixed-point condition under the same causal operator.

Localized invariant modes correspond to persistent particle-like structures.

## Key Idea

Particle-like structures are not fundamental objects but emergent features corresponding to invariant modes of the causal operator.

## Usage

Clone the repository:

git clone https://github.com/Scheduler4861/xor-particles.git

cd xor-particles

Install dependencies:

pip install -r requirements.txt

Run the simulation:

python xor_model.py

## What this code does

- Simulates XOR-based causal dynamics on a 2D lattice
- Demonstrates global parity invariance
- Tests localized invariant candidates
- Detects persistent structures ("particles")
- Estimates velocity and stability of emergent patterns

## Theory–Code Correspondence

- Causal operator K → implemented in step() and K(x)
- Invariant observable I_w → implemented in invariant()
- Fixed point condition K(w) = w → is_fixed_point()
- Localized modes → generate_weight_local()
- Particle detection → detect_persistent()

## Citation

If you use this work, please cite:

Scheduler4861. (2026).
*Invariant Structure of XOR Causal Dynamics under Finite Propagation.*
Zenodo. https://doi.org/10.5281/zenodo.19600725

## License

This work is licensed under the Creative Commons Attribution 4.0 International License.
