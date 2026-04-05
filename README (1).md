# Carry-Reuse: Breaking Elliptic Curve Cryptography with Fewer Qubits

**Simulation and verification code for the paper by Tidoshi (2026)**

Version 4.2 — 520-Qubit Single-Run Architecture

## Overview

This repository contains all simulation code supporting the claims in "Carry-Reuse: Breaking Elliptic Curve Cryptography with Fewer Qubits." The paper introduces carry-reuse, a quantum circuit architecture that replaces standard uncomputation with mid-circuit measurement and reset, reducing the logical qubit count for ECDLP from 1,193 to 780 (unconditional, all curves) or 520 (conditional, Montgomery-compatible curves).

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

## Key Results

- **Theorem 4:** Compound carry vector produces exactly n−1 equivalence classes on 180/180 tested curves (zero exceptions)
- **Lemma 2:** Per-step carry detection rate = 0.904 (≥ 7/8 = 0.875, confirmed). Persistence after first detection = 1.000
- **Single-run:** 280/280 = 100% success across 14 prime-order curves
- **Theorem 1:** Zero discrepancy between analytical formula and exact enumeration across 500 test cases per bit width
- **Theorem 2:** QFT quality ratio 0.947–1.061 with no degradation trend

## Citation

```
Tidoshi (2026). "Carry-Reuse: Breaking Elliptic Curve Cryptography
with Fewer Qubits." Version 4.2.
Contact: satoshirising420@gmail.com
```

## License

MIT License. See LICENSE file.
