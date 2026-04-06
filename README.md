# Carry Injectivity Creates a Depth–Superposition Trade-Off in Quantum ECDLP Circuits

**Author:** Brad Merrill  
[`carry_injectivity_SUBMISSION.pdf`](carry_injectivity_SUBMISSION.pdf)

## Abstract

Quantum circuits for the ECDLP spend roughly half their depth uncomputing intermediate carry bits. A natural optimization — measuring carries mid-circuit instead of uncomputing them — would halve oracle depth. We show that this optimization is blocked by a structural property of the carries themselves.

We prove that the extended carry vector (multiplication quotients + modular reduction flags) from scalar multiplication is **injective**: distinct scalars produce distinct carry sequences, with a unique algebraic exception characterized by y-coordinate matching (≤ 2 collisions per curve). Verified across **four arithmetic models** — affine, Jacobian projective, Montgomery ladder, and fixed-window — on 142 curve–model configurations (b = 4–15) with zero full-injectivity exceptions.

This injectivity creates a **depth–superposition trade-off**: measuring all carries collapses the superposition, destroying the QFT. We prove a scaling law: the critical measurement fraction satisfies f* ≥ 1 − 1/b (Proposition 11). At b = 256: f* = 99.6% — the trade-off **vanishes at cryptographic scale**. Applied to the 1,193-qubit oracle of Chevignard et al. (2026): ~31M Toffoli in ~31s vs. the baseline ~60M in ~60s — a **1.94× depth reduction**.

## Key Results

- **Carry Collision Characterization (Theorem 2):** A collision Cˢ(k) = Cˢ(k+1) with k ≥ 2 occurs iff (a) k is even and (b) all carries from [k]G + G are zero. Collision count ≤ 2 per curve, computable in polynomial time by solving the curve cubic.
- **Extended Carry Injectivity (Theorem 5):** Cᵉ(x) is injective on {2, …, n−1} with unique collision {0, 1}. Verified on 35 curves including all 13 simplified-model failures. Zero exceptions.
- **Depth–Superposition Trade-Off (Proposition 9):** Full carry measurement collapses the input to a single basis state. Depth halving and QFT recovery are mutually exclusive.
- **Scaling Law (Proposition 11):** Each informative carry contributes exactly 1 bit of conditional entropy. f* ≥ 1 − 1/b, so at b = 256 only ~16 carries need uncomputation out of ~4,000 total.
- **QFT Verification (Table 4):** Full state-vector QFT analysis confirms Pr[good] ≈ 0.78–0.82 ≫ 4/π² on projected states.
- **Persistence Bound (Proposition 8):** Conservative bound Pr[persistence failure] < 2⁻²³⁹ at b = 256, using only first-carry independence.

## Concrete Resource Estimates

| Configuration | Qubits | Toffoli | Runtime (1 MHz) | Speedup |
|---|---|---|---|---|
| Baseline (Chevignard et al.) | 1,193 | ~60M | ~60s | 1.00× |
| + carry-reuse f=90% | ~1,050 | ~33M | ~33s | 1.82× |
| + carry-reuse f=85% | ~1,080 | ~35M | ~35s | 1.71× |
| + carry-reuse f=100% | ~1,000 | ~30M | ~30s | N/A (QFT fails) |

## Injectivity Across Arithmetic Models

| Arithmetic model | Configs | b range | Full injectivity | Max collisions |
|---|---|---|---|---|
| Affine double-and-add | 35 | 4–15 | 35/35 | 0 |
| Jacobian projective | 29 | 4–13 | 29/29 | 0 |
| Montgomery ladder | 27 | 4–14 | 27/27 | 0 |
| Fixed-window (w=2,3,4) | 51 | 4–12 | 0/51 | ≤ 3 |
| **Total** | **142** | **4–15** | **91/142** | **≤ 3** |

## Simulation Scripts

Scripts validating related carry-reuse claims:

| Script | Validates | Runtime |
|--------|-----------|---------|
| `compound_carry_uniqueness.py` | Compound carry vector uniqueness | ~3s (p≤2000), ~60s (p≤4000) |
| `per_step_carry_analysis.py` | Per-step carry detection rate ≥ 0.90 | ~1s |
| `single_run_recovery.py` | Single-run d-recovery protocol | ~5s |
| `carry_information_content.py` | Carry entropy = b − 1.44 bits | <1s |
| `qft_quality_simulation.py` | QFT quality under carry measurement | ~10s |

## Quick Start

```bash
python3 compound_carry_uniqueness.py --max-prime 4000
python3 per_step_carry_analysis.py
python3 single_run_recovery.py
python3 carry_information_content.py
python3 qft_quality_simulation.py
```

## Requirements

- Python 3.8+
- No external dependencies (standard library only)

## Citation

```
Brad Merrill (2026). "Carry Injectivity Creates a Depth–Superposition
Trade-Off in Quantum ECDLP Circuits."
```

## License

MIT License. See [LICENSE](LICENSE) file.
