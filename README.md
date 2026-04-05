# Carry-Reuse: Breaking Elliptic Curve Cryptography with Fewer Qubits

**Author:** Tidoshi  
**Contact:** satoshirising420@gmail.com  
**Version:** 4.2 — 520-Qubit Single-Run Architecture

## Overview

This repository contains the paper and all simulation code supporting the claims in "Carry-Reuse: Breaking Elliptic Curve Cryptography with Fewer Qubits." The paper introduces carry-reuse, a quantum circuit architecture that replaces standard uncomputation with mid-circuit measurement and reset, reducing the logical qubit count for ECDLP from 1,193 to 780 (unconditional, all curves) or 520 (conditional, Montgomery-compatible curves).

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

- [`Carry_Reuse_v4_2_Tidoshi.pdf`](Carry_Reuse_v4_2_Tidoshi.pdf)

## Scripts

| Script | Validates | Runtime |
|--------|-----------|---------|
| `compound_carry_uniqueness.py` | Theorem 4 (carry vector determines k uniquely) | ~3s (p≤2000), ~60s (p≤4000) |
| `per_step_carry_analysis.py` | Lemma 2 (per-step detection rate ≥ 0.90) | ~1s |
| `single_run_recovery.py` | §7.5 (single-run d-recovery protocol) | ~5s |
| `carry_information_content.py` | Theorem 1 (carry entropy = b − 1.44 bits) | <1s |
| `qft_quality_simulation.py` | Theorem 2 (QFT quality under carry measurement) | ~10s |

## Quick Start

```bash
# Verify Theorem 4: compound carry uniqueness (180 curves, 0 exceptions)
python3 compound_carry_uniqueness.py --max-prime 4000

# Measure per-step carry detection rate (replaces hand-wavy 7/8 bound)
python3 per_step_carry_analysis.py

# End-to-end single-run key recovery (280/280 success)
python3 single_run_recovery.py

# Verify Theorem 1: carry information content
python3 carry_information_content.py

# Full QFT quality simulation at b = 4–8
python3 qft_quality_simulation.py
```

## Requirements

- Python 3.8+
- No external dependencies (standard library only)

## Simulation Results

- **Theorem 4:** Compound carry vector produces exactly n−1 equivalence classes on 180/180 tested curves (zero exceptions)
- **Lemma 2:** Per-step carry detection rate = 0.904 (≥ 7/8 = 0.875, confirmed). Persistence after first detection = 1.000
- **Single-run:** 280/280 = 100% success across 14 prime-order curves
- **Theorem 1:** Zero discrepancy between analytical formula and exact enumeration across 500 test cases per bit width
- **Theorem 2:** QFT quality ratio 0.947–1.061 with no degradation trend

## Keywords

Quantum computing, elliptic curve cryptography, ECDLP, Shor's algorithm, carry-reuse, measurement-based uncomputation, qubit optimization, Beauregard arithmetic, Montgomery ladder, QLDPC codes, Dirichlet kernel

## Citation

```
Tidoshi (2026). "Carry-Reuse: Breaking Elliptic Curve Cryptography
with Fewer Qubits." Version 4.2.
Contact: satoshirising420@gmail.com
```

## License

MIT License. See [LICENSE](LICENSE) file.
