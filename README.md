Fransén-Robinson Constant: 1,500 Digit Computation
This repository contains the heavily optimized Python scripts and verification engines used to compute the decimal expansion of the Fransén-Robinson constant (OEIS A058655) to 1,500 significant digits, setting a new unofficial computational record.
The computation was achieved purely on consumer hardware (a G15 laptop) by mathematically determining finite integral truncation points and distributing asymmetric algorithmic workloads across a multi-core CPU.
The Constant
The Fransén-Robinson constant () is the area between the reciprocal Gamma function and the positive x-axis:

Methodology & Verification
To eliminate the possibility of floating-point arithmetic drift and hardware errors, the 1,500 digits were computed twice using two mathematically distinct orthogonal integration methods.
Primary Pass (fransen_robinson.py):
Method: Tanh-Sinh (Double Exponential) Quadrature.
Engine: mpmath backed by gmpy2 (C-level).
Optimization: Asymmetric workload chunking and direct reciprocal gamma (rgamma) bypass.
Verification Pass (fransen_robinson_verifier.py):
Method: Gauss-Legendre Quadrature.
Engine: mpmath backed by gmpy2.
Optimization: Uniform geometric progression intervals.
Result: Both computational pathways yielded a 100% exact character-by-character match for all 1,500 digits.
Hardware Used
Machine: ASUS/Dell G15 Mobile CPU
Environment: Python 3.x with Multiprocessing
Sustained Load: 100% multi-core utilization over multiday runs.
How to Reproduce
If you wish to verify the integrity of these scripts on your own machine:
Install Dependencies:
You must have gmpy2 installed to bypass Python's native math bottleneck, otherwise the calculation will take weeks.
pip install mpmath gmpy2


Run the Primary Engine:
python fransen_robinson.py

(Note: Target precision is set at the bottom of the script. Start with a target of 100 to benchmark your CPU before attempting 1,500).
Run the Verification Engine:
python fransen_robinson_verifier.py

This will automatically cross-reference its output against fransen_robinson_1500_digits.txt if the file is present in the directory.
Repository Contents
fransen_robinson.py - Primary calculation engine.
fransen_robinson_verifier.py - Secondary Gauss-Legendre engine.
generate_b_file.py - OEIS compliant formatter.
fransen_robinson_1500_digits.txt - The raw 1,500 digit output.
b058655.txt - The OEIS-formatted b-file submitted for review.
