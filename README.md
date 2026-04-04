# Carry-Reuse: Breaking Elliptic Curve Cryptography with Fewer Qubits

**Author:** Tidoshi  
**Contact:** satoshirising420@gmail.com  
**Version:** 2.0 — Extended and Revised

## Abstract

We present **carry-reuse**, a modified quantum circuit architecture for the elliptic curve discrete logarithm problem (ECDLP). Standard Shor implementations uncompute intermediate carry bits from modular arithmetic, roughly doubling gate cost and preventing ancilla reuse. We measure carry registers mid-circuit instead, freeing workspace qubits via measurement-based reset.

### Key Results

1. **Information Content** — The carry function in a single modular multiplication encodes *b − 1.44* bits of its *b*-bit operand (Theorem 1, verified with zero error across 500 test cases).
2. **QFT Preservation** — Carry measurement preserves periodicity detection with per-run success probability ≥ 4/π² ≈ 0.405, independent of bit width (Theorem 2).
3. **Deterministic Structure** — Carry bits in the full ECDLP oracle are deterministic functions of the superposition variable with staircase structure at each arithmetic step (Theorem 3).
4. **Simulation Validation** — Simulation at b = 4–8 confirms 95–100% QFT quality under carry measurement.

### Architectural Result

Using a serial schoolbook multiplier with measurement-based ancilla reset, the circuit requires **863 logical qubits** for 256-bit curves — a **1.38× reduction** from the best published 1,193-qubit implementation. This trades ~15–30× more circuit depth per run for fewer qubits.

### Conditional Projections

If carry information is fully exploitable, 3–8 runs suffice for key recovery. Under QLDPC error correction at 30:1 ratio, this maps to ~30,000 physical qubits. Both the compound carry analysis and the QLDPC ratio remain open problems.

## Paper

The full paper is available in this repository:

- [`Carry_Reuse_v3_tidoshi.pdf`](Carry_Reuse_v3_tidoshi.pdf)

## Keywords

Quantum computing, elliptic curve cryptography, ECDLP, Shor's algorithm, carry-reuse, measurement-based uncomputation, qubit optimization, QFT, modular arithmetic, post-quantum migration, QLDPC codes
