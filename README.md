# Carry-Reuse in Quantum ECDLP Circuits

Research on carry-reuse optimization for quantum circuits solving the elliptic curve discrete logarithm problem (ECDLP).

## Papers

### Carry Injectivity Creates a Depth–Superposition Trade-Off in Quantum ECDLP Circuits
**Author:** Brad Merrill | [`carry_injectivity_SUBMISSION.pdf`](carry_injectivity_SUBMISSION.pdf)

Formal submission proving that the extended carry vector (multiplication quotients + modular reduction flags) from EC scalar multiplication is **injective**: distinct scalars produce distinct carry sequences. Verified across **four arithmetic models** — affine, Jacobian projective, Montgomery ladder, and fixed-window — on 142 curve–model configurations (b = 4–15) with zero full-injectivity exceptions.

**Key findings:**
- **Carry Collision Characterization (Theorem 2):** Collisions occur iff (a) k is even and (b) all carries from [k]G + G are zero. At most ≤ 2 collisions per curve, characterized by y-coordinate matching.
- **Extended Carry Injectivity (Theorem 5):** Cᵉ(x) is injective on {2, …, n−1} with unique collision {0, 1}. Verified on 35 curves including all 13 simplified-model failures. Zero exceptions.
- **Depth–Superposition Trade-Off (Proposition 9):** Measuring all carries collapses the superposition to a single basis state, destroying QFT periodicity. Depth halving and QFT recovery are mutually exclusive.
- **Resolution via Partial Measurement (§5.1):** Measuring fraction f ≈ 1 − 1/b of carries preserves W ≥ 2 equivalence classes. At b = 256: f* = 99.6%, achieving **1.94× depth reduction** (~31M vs ~60M Toffoli) while maintaining Pr[good] ≈ 0.78–0.82 ≫ 4/π².
- **Scaling Law (Proposition 11):** Each informative carry entry contributes exactly 1 bit of conditional entropy. The critical fraction f* ≥ 1 − 1/b, so the trade-off vanishes at cryptographic scale.

| Configuration | Qubits | Toffoli | Runtime (1 MHz) | Speedup |
|---|---|---|---|---|
| Baseline [Chevignard et al.] | 1,193 | ~60M | ~60s | 1.00× |
| + carry-reuse f=90% | ~1,050 | ~33M | ~33s | 1.82× |
| + carry-reuse f=85% | ~1,080 | ~35M | ~35s | 1.71× |

### Carry-Reuse: Breaking Elliptic Curve Cryptography with Fewer Qubits
**Author:** Tidoshi | **Version 4.2** | [`Carry_Reuse_v4_2_Tidoshi.pdf`](Carry_Reuse_v4_2_Tidoshi.pdf)

The original carry-reuse architecture paper proposing measurement-based ancilla reset to reduce logical qubit counts for ECDLP.

**Key results:**
- **520 logical qubits** for 256-bit Montgomery curves (2.29× reduction from 1,193) using Beauregard in-place arithmetic + Montgomery ladder
- **780-qubit fallback** for non-Montgomery curves (1.53× reduction)
- **Single-run key recovery:** 280/280 = 100% simulation success across 14 prime-order curves
- **Carry information content:** b − 1.44 bits per operand (Theorem 1)
- **QFT preservation:** Pr[success] ≥ 4/π² ≈ 0.405 (Theorem 2)
- **Compound carry uniqueness:** P(collision) ≤ 2⁻²⁵⁶ on 180 curves (Theorem 4)
- **Error detection:** 1,032:1 redundancy ratio, 100% detection of corrupted runs (~10× speedup at 10% error rate)
- **Physical qubits:** ~15,600 under QLDPC 30:1 (projected)

## Simulation Scripts

Scripts validating claims from the Tidoshi v4.2 paper:

| Script | Validates | Runtime |
|--------|-----------|---------|
| `compound_carry_uniqueness.py` | Theorem 4 (carry vector determines k uniquely) | ~3s (p≤2000), ~60s (p≤4000) |
| `per_step_carry_analysis.py` | Lemma 2 (per-step detection rate ≥ 0.90) | ~1s |
| `single_run_recovery.py` | §7.5 (single-run d-recovery protocol) | ~5s |
| `carry_information_content.py` | Theorem 1 (carry entropy = b − 1.44 bits) | <1s |
| `qft_quality_simulation.py` | Theorem 2 (QFT quality under carry measurement) | ~10s |

## Quick Start

```bash
# Verify compound carry uniqueness (180 curves, 0 exceptions)
python3 compound_carry_uniqueness.py --max-prime 4000

# Per-step carry detection rate
python3 per_step_carry_analysis.py

# End-to-end single-run key recovery (280/280 success)
python3 single_run_recovery.py

# Carry information content verification
python3 carry_information_content.py

# Full QFT quality simulation at b = 4–8
python3 qft_quality_simulation.py
```

## Requirements

- Python 3.8+
- No external dependencies (standard library only)

## Simulation Results

- **Theorem 4:** n−1 equivalence classes on 180/180 tested curves (zero exceptions)
- **Lemma 2:** Per-step detection rate = 0.904 (≥ 0.875 confirmed). Persistence = 1.000
- **Single-run:** 280/280 = 100% across 14 prime-order curves
- **Theorem 1:** Zero discrepancy across 500 test cases per bit width
- **Theorem 2:** QFT quality ratio 0.947–1.061, no degradation trend

## Citation

```
Brad Merrill (2026). "Carry Injectivity Creates a Depth–Superposition
Trade-Off in Quantum ECDLP Circuits."

Tidoshi (2026). "Carry-Reuse: Breaking Elliptic Curve Cryptography
with Fewer Qubits." Version 4.2. Contact: satoshirising420@gmail.com
```

## License

MIT License. See [LICENSE](LICENSE) file.
