#!/usr/bin/env python3
"""
compound_carry_uniqueness.py — Theorem 4 Verification
======================================================
Verifies that the compound modular arithmetic carry vector from [x]G
computation determines x uniquely for all x >= 2, with the sole
exception {0, 1}.

Tidoshi (2026) — Carry-Reuse v4.2
Contact: satoshirising420@gmail.com

Usage:
    python3 compound_carry_uniqueness.py                  # default: p <= 2000
    python3 compound_carry_uniqueness.py --max-prime 4000  # extended
    python3 compound_carry_uniqueness.py --verbose
"""

import math, time, argparse
from collections import defaultdict


# ── Elliptic Curve Arithmetic ────────────────────────────────────

def ec_add(P, Q, a, p):
    """Affine point addition on y^2 = x^3 + ax + b over F_p."""
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P; x2, y2 = Q
    if x1 == x2:
        if (y1 + y2) % p == 0: return None
        lam = (3 * x1 * x1 + a) * pow(2 * y1, -1, p) % p
    else:
        lam = (y2 - y1) * pow(x2 - x1, -1, p) % p
    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3)


# ── Carry Extraction ─────────────────────────────────────────────

def extract_carries(x, G, a, p, b):
    """
    Compute [x]G via MSB-first double-and-add, extracting ALL modular
    arithmetic carry values (quotients floor(a*b/p)) from each field
    multiplication.

    Returns: tuple of carry values (hashable for equivalence-class counting)
    """
    bits = [(x >> (b - 1 - i)) & 1 for i in range(b)]
    R = None
    carries = []

    for i in range(b):
        # Doubling: R <- 2R
        if R is not None:
            rx, ry = R
            if (2 * ry) % p == 0:
                carries.append(-1)
                R = None
                if bits[i] == 1:
                    R = G
                continue

            v1 = 3 * rx * rx + a
            carries.append(v1 // p)
            lam = (v1 % p) * pow(2 * ry, -1, p) % p

            v2 = lam * lam
            carries.append(v2 // p)
            x3 = (v2 - 2 * rx) % p

            v3 = lam * ((rx - x3) % p)
            carries.append(v3 // p)
            R = (x3, (v3 % p - ry) % p)

        # Conditional addition: R <- R + G (if bit is 1)
        if bits[i] == 1:
            if R is None:
                R = G
            else:
                rx, ry = R; gx, gy = G
                if rx == gx:
                    if (ry + gy) % p == 0:
                        R = None
                    else:
                        R = ec_add(R, R, a, p)
                else:
                    lam = (gy - ry) * pow((gx - rx) % p, -1, p) % p
                    v4 = lam * lam
                    carries.append(v4 // p)
                    x3 = (v4 - rx - gx) % p
                    v5 = lam * ((rx - x3) % p)
                    carries.append(v5 // p)
                    R = (x3, (v5 % p - ry) % p)

    return tuple(carries)


# ── Curve Utilities ──────────────────────────────────────────────

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True


def count_curve_order(a, b, p):
    """Count #E(F_p) by Legendre symbol enumeration."""
    count = 1
    for x in range(p):
        rhs = (x * x * x + a * x + b) % p
        if rhs == 0:
            count += 1
        elif pow(rhs, (p - 1) // 2, p) == 1:
            count += 2
    return count


def find_point(a, b, p):
    """Find any affine point on y^2 = x^3 + ax + b (mod p)."""
    for x in range(p):
        rhs = (x * x * x + a * x + b) % p
        if rhs == 0:
            return (x, 0)
        if pow(rhs, (p - 1) // 2, p) == 1:
            if p % 4 == 3:
                y = pow(rhs, (p + 1) // 4, p)
            else:
                # Tonelli-Shanks
                q, s = p - 1, 0
                while q % 2 == 0: q //= 2; s += 1
                z = 2
                while pow(z, (p - 1) // 2, p) != p - 1: z += 1
                m, c = s, pow(z, q, p)
                t, r = pow(rhs, q, p), pow(rhs, (q + 1) // 2, p)
                while t != 1:
                    i = 1; tmp = t * t % p
                    while tmp != 1: tmp = tmp * tmp % p; i += 1
                    bb = pow(c, 1 << (m - i - 1), p)
                    m, c, t, r = i, bb * bb % p, t * bb * bb % p, r * bb % p
                y = r
            if (y * y) % p == rhs:
                return (x, y)
    return None


# ── Main Verification ────────────────────────────────────────────

def verify_carry_uniqueness(max_prime=2000, verbose=False):
    results = []
    anomalies = []
    t0 = time.time()

    for p in range(13, max_prime + 1):
        if not is_prime(p): continue

        for a_val, b_val in [(1, 1), (2, 1), (1, 3), (3, 7), (5, 2), (7, 1)]:
            if (4 * a_val ** 3 + 27 * b_val ** 2) % p == 0: continue

            n = count_curve_order(a_val, b_val, p)
            if not is_prime(n) or n < 13: continue

            G = find_point(a_val, b_val, p)
            if G is None: continue

            b_width = math.ceil(math.log2(n))

            sig_map = defaultdict(list)
            for x in range(n):
                sig = extract_carries(x, G, a_val, p, b_width)
                sig_map[sig].append(x)

            num_classes = len(sig_map)
            max_size = max(len(v) for v in sig_map.values())

            collisions = {k: v for k, v in sig_map.items() if len(v) > 1}
            is_perfect = (num_classes == n - 1 and
                          len(collisions) == 1 and
                          all(sorted(v) == [0, 1] for v in collisions.values()))

            if not is_perfect:
                anomalies.append({
                    'p': p, 'a': a_val, 'b': b_val, 'n': n,
                    'classes': num_classes, 'collisions': collisions
                })

            results.append({
                'p': p, 'a': a_val, 'b': b_val, 'n': n, 'b_width': b_width,
                'classes': num_classes, 'max_size': max_size, 'perfect': is_perfect
            })

            if verbose and p % 200 < 5:
                print(f"  p={p:>5}, n={n:>5}, b={b_width:>2}: "
                      f"classes={num_classes:>5} ({'OK' if is_perfect else 'ANOMALY'})")
            break

    elapsed = time.time() - t0
    return results, anomalies, elapsed


def main():
    parser = argparse.ArgumentParser(
        description="Verify Compound Carry Uniqueness Theorem (Theorem 4)")
    parser.add_argument('--max-prime', type=int, default=2000,
                        help='Test all primes up to this value (default: 2000)')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    print("=" * 68)
    print("COMPOUND CARRY UNIQUENESS — THEOREM 4 VERIFICATION")
    print("Tidoshi (2026) — Carry-Reuse v4.2")
    print("=" * 68)

    results, anomalies, elapsed = verify_carry_uniqueness(
        args.max_prime, args.verbose)

    n_perfect = sum(1 for r in results if r['perfect'])

    print(f"\nResults:")
    print(f"  Curves tested:    {len(results)}")
    print(f"  Perfect (n-1):    {n_perfect}")
    print(f"  Anomalies:        {len(anomalies)}")
    print(f"  Success rate:     {n_perfect / len(results):.6f}")
    print(f"  Time:             {elapsed:.2f}s")

    if anomalies:
        print(f"\nANOMALIES FOUND:")
        for a in anomalies:
            print(f"  p={a['p']}, n={a['n']}: {a['classes']} classes")
    else:
        print(f"\n  *** ALL {len(results)} CURVES: classes = n-1 ***")
        print(f"  *** SOLE COLLISION: {{0, 1}} IN EVERY CASE ***")

    by_b = defaultdict(list)
    for r in results: by_b[r['b_width']].append(r)

    print(f"\nScaling by bit width:")
    print(f"  {'b':>3} {'curves':>7} {'min_n':>7} {'max_n':>7} {'all_ok':>8}")
    for b in sorted(by_b.keys()):
        rs = by_b[b]
        print(f"  {b:>3} {len(rs):>7} {min(r['n'] for r in rs):>7} "
              f"{max(r['n'] for r in rs):>7} "
              f"{'YES' if all(r['perfect'] for r in rs) else 'NO':>8}")

    print(f"\nTheorem 4: {'VERIFIED' if not anomalies else 'COUNTEREXAMPLE FOUND'}")


if __name__ == '__main__':
    main()
