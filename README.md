# Carry-Reuse: Breaking Elliptic Curve Cryptography with Fewer Qubits

**Author:** Tidoshi  
**Contact:** satoshirising420@gmail.com  
**Version:** 4.2 — 520-Qubit Single-Run Architecture

## Abstract

We present **carry-reuse**, a modified quantum circuit architecture for the elliptic curve discrete logarithm problem (ECDLP). Standard Shor implementations uncompute intermediate carry bits from modular arithmetic, roughly doubling gate cost and preventing ancilla reuse. We measure carry registers mid-circuit instead, freeing workspace qubits via measurement-based reset.

### Key Results

1. **Information Content** — The carry function in a single modular multiplication encodes *b − 1.44* bits of its *b*-bit operand (Theorem 1, verified with zero error across 500 test cases).
2. **QFT Preservation** — Carry measurement preserves periodicity detection with per-run success probability ≥ 4/π² ≈ 0.405, independent of bit width (Theorem 2).
3. **Deterministic Structure** — Carry bits in the full ECDLP oracle are deterministic functions of the superposition variable with staircase structure (Theorem 3).
4. **Compound Carry Uniqueness** — The compound carry vector determines *x* uniquely for all *x* ≥ 2, with P(collision) ≤ 2⁻²⁵⁶, verified on 180 prime-order curves with zero exceptions (Theorem 4).
5. **Simulation Validation** — Simulation at b = 4–8 confirms 95–100% QFT quality under carry measurement.

### Architectural Result (Unconditional)

Using Beauregard in-place modular arithmetic with measurement-based ancilla reset and a Montgomery ladder structure, the circuit requires **520 logical qubits** for 256-bit Montgomery-compatible curves — a **2.29× reduction** from the best published 1,193-qubit implementation. For non-Montgomery curves, a **780-qubit** fallback architecture provides a 1.53× reduction.

### Single-Run Recovery (Near-Unconditional)

Theorem 4 establishes that carry measurements determine the superposition variable k₀ uniquely. With |S| = 1 after carry collapse, the semiclassical QFT extracts the phase d·k₀/n exactly, enabling high-probability single-run key recovery. Simulation confirms **100% single-run success** across 14 prime-order curves (280/280 trials). Under QLDPC error correction at 30:1 ratio (projected), this maps to **~15,600 physical qubits**.

## Paper

The full paper is available in this repository:

- [`Carry_Reuse _v4_2.pdf`](Carry_Reuse%20_v4_2.pdf)

## Keywords

Quantum computing, elliptic curve cryptography, ECDLP, Shor's algorithm, carry-reuse, measurement-based uncomputation, qubit optimization, Beauregard arithmetic, Montgomery ladder, QLDPC codes, Dirichlet kernel
