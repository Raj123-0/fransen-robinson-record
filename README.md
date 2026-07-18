This repository contains the heavily optimized Python scripts and verification engines used to compute the decimal expansion of the Fransén-Robinson constant to 1,500 significant digits, establishing a new unofficial computational record.

The previous known record (approx. 1,025 digits) was extended using purely consumer hardware by mathematically determining finite integral truncation points and distributing asymmetric algorithmic workloads across a multi-core CPU.

 The Constant

The Fransén-Robinson constant ($F$) is defined as the area between the reciprocal Gamma function and the positive x-axis. It cannot be expressed in a simple closed form using other known constants.

$$F = \int_0^\infty \frac{1}{\Gamma(x)} dx \approx 2.8077702420...$$

 The Computational Achievement

Arbitrary-precision integration of the reciprocal gamma function is notoriously CPU-intensive. This computation was achieved by bypassing standard floating-point bottlenecks using mpmath backed by the C-level gmpy2 library, combined with dynamic multiprocessing.

Machine: ASUS/Dell G15 Mobile CPU

Environment: Python 3.x

Workload: 100% sustained multi-core utilization over multiday runs.

Result: 1,500 digits successfully calculated and independently verified.

 Verification & Methodology

To eliminate the possibility of hardware-induced floating-point drift over the multiday computation, the 1,500 digits were calculated twice using two mathematically orthogonal computational pathways.

Both engines yielded a 100% exact character-by-character match for all 1,500 digits.

Feature

Primary Engine (fransen_robinson.py)

Verification Engine (fransen_robinson_verifier.py)

Quadrature Method

Tanh-Sinh (Double Exponential)

Gauss-Legendre

Chunking Strategy

Asymmetric Curve-Based Slicing

Uniform Geometric Progression

Function Call

Direct rgamma() bypass

Inverse 1 / gamma()

Integration Bounds

Mathematically truncated at $10^{-1515}$ precision

Truncated using extended geometric buffer bounds

 Repository Contents

fransen_robinson.py - The primary high-speed Tanh-Sinh integration engine.

fransen_robinson_verifier.py - The secondary Gauss-Legendre verification engine with built-in strict diff-checking.

generate_b_file.py - A utility script to format the raw output into an OEIS-compliant text file.

fransen_robinson_1500_digits.txt - The raw 1,500 digit computational output.

b058655.txt - The correctly indexed b-file submitted to the OEIS for review.

 How to Reproduce

If you wish to verify the computational integrity of these scripts on your own machine, you can run the engines locally.

1. Install Dependencies

You must have gmpy2 installed to bypass Python's native math bottleneck. Without it, the calculation will take exponentially longer.

pip install mpmath gmpy2


2. Run the Primary Engine

(Note: Target precision is set at the bottom of the script. Start with a target of 100 to benchmark your CPU before attempting higher precisions).

python fransen_robinson.py


3. Run the Verification Engine

Ensure fransen_robinson_1500_digits.txt is in your directory. The script will compute the constant using Gauss-Legendre quadrature and automatically diff-check its results against the text file.

python fransen_robinson_verifier.py


🏆 Acknowledgments

Fredrik Johansson for the prior 1,000-digit computation of this constant.

The OEIS Foundation for maintaining sequence A058655.
