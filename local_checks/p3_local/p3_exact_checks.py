#!/usr/bin/env python3
"""Exact algebra and CONDITIONAL Weil--Deligne checks for the p=3 note.

Standard library only. No archived numerical experiments are rerun.
The matrix portion verifies consequences of an ASSUMED geometric
identification; it does not certify nearby cycles or that identification.
Run: python p3_exact_checks.py --output p3_exact_checks.json
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import json
from pathlib import Path


# Univariate polynomials are coefficient lists in ascending degree.
def trim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def add(a, b):
    c = [0] * max(len(a), len(b))
    for i, x in enumerate(a):
        c[i] += x
    for i, x in enumerate(b):
        c[i] += x
    return trim(c)


def scale(a, scalar):
    return trim([scalar * x for x in a])


def sub(a, b):
    return add(a, scale(b, -1))


def mul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return trim(c)


def power(a, n):
    c = [1]
    for _ in range(n):
        c = mul(c, a)
    return c


def compose(a, b):
    c = [0]
    for coefficient in reversed(a):
        c = add(mul(c, b), [coefficient])
    return c


def ident(n):
    return [[Q(int(i == j)) for j in range(n)] for i in range(n)]


def zeros(n):
    return [[Q(0) for _ in range(n)] for _ in range(n)]


def mmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def madd(a, b):
    return [[x + y for x, y in zip(row_a, row_b)]
            for row_a, row_b in zip(a, b)]


def mscale(a, scalar):
    return [[scalar * x for x in row] for row in a]


def transpose(a):
    return [list(row) for row in zip(*a)]


def rank(a):
    a = [[Q(x) for x in row] for row in a]
    r = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        denominator = a[r][col]
        a[r] = [x / denominator for x in a[r]]
        for i in range(len(a)):
            if i != r:
                coefficient = a[i][col]
                a[i] = [x - coefficient * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def determinant(a):
    a = [[Q(x) for x in row] for row in a]
    result = Q(1)
    for col in range(len(a)):
        pivot = next((i for i in range(col, len(a)) if a[i][col]), None)
        if pivot is None:
            return Q(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            result = -result
        p = a[col][col]
        result *= p
        for i in range(col + 1, len(a)):
            c = a[i][col] / p
            a[i] = [x - c * y for x, y in zip(a[i], a[col])]
    return result


def serial_matrix(a):
    return [[int(x) if x.denominator == 1 else str(x) for x in row]
            for row in a]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_suffix(".json"))
    args = parser.parse_args()
    checks = []

    def check(name, obtained, expected, category, explanation=""):
        passed = obtained == expected
        checks.append({"name": name, "category": category, "passed": passed,
                       "explanation": explanation})
        if not passed:
            raise AssertionError(f"{name}: {obtained!r} != {expected!r}")

    def polycheck(name, lhs, rhs, explanation=""):
        check(name, sub(lhs, rhs), [0], "exact_polynomial_identity", explanation)

    t = [0, 1]
    a = mul([-1, 1], [2, 1])
    b = [2, 1]
    c4 = scale(sub(power(a, 2), scale(b, 3)), 16)
    delta = scale(mul(power(b, 2), sub(power(a, 2), scale(b, 4))), 16)
    polycheck("quotient_u_plus_2", mul(power([-1, 1], 2), [2, 1]),
              [2, -3, 0, 1], "(t-1)^2(t+2)=t^3-3t+2")
    polycheck("quotient_c4", c4, scale(mul([2, 1], [-1, -3, 0, 1]), 16))
    polycheck("quotient_discriminant", delta,
              scale(mul(power([2, 1], 3), mul([-2, 1], power([1, 1], 2))), 16))

    # t=(z^2+1)/z. Clear denominators explicitly.
    z = [0, 1]
    t_num, t_den = [1, 0, 1], z
    a_num = mul(sub(t_num, t_den), add(t_num, scale(t_den, 2)))
    a_den = power(z, 2)
    b_num, b_den = add(t_num, scale(t_den, 2)), z
    d_num, d_den = [0, 0, -1], [1, 1]
    polycheck("twist_a_cleared", mul(d_num, a_num),
              mul([-1, 0, 0, -1], mul(d_den, a_den)),
              "d*a(t(z))=-(1+z^3), d=-z^2/(z+1)")
    polycheck("twist_b_cleared", mul(power(d_num, 2), b_num),
              mul(power(z, 3), mul(power(d_den, 2), b_den)),
              "d^2*b(t(z))=z^3")
    # d(1/z)=-1/[z(z+1)], d(z)/z^3=-z^2/[(z+1)z^3].
    polycheck("inversion_twist_cleared",
              mul([-1], mul(d_den, power(z, 3))),
              mul(d_num, mul(z, [1, 1])),
              "d(1/z)=d(z)/z^3; this checks the scalar identity, not sheaf descent")

    # h=t+2=v^4, x=v^2*X, y=v^3*Y.
    v = [0, 1]
    v4 = power(v, 4)
    tame_a = mul(power(v, 2), add(v4, [-3]))
    tame_b = [1]
    tame_delta = scale(sub(power(tame_a, 2), [4]), 16)
    polycheck("tame_chart_a", compose(a, add(v4, [-2])),
              mul(power(v, 2), tame_a))
    polycheck("tame_chart_b", compose(b, add(v4, [-2])),
              mul(power(v, 4), tame_b))
    polycheck("tame_chart_discriminant", tame_delta,
              scale(mul(add(v4, [-4]), power(add(v4, [-1]), 2)), 16))
    polycheck("tame_chart_scaling_discriminant", compose(delta, add(v4, [-2])),
              mul(power(v, 12), tame_delta))
    check("tame_chart_good_reduction_at_v_zero", tame_delta[0] % 3 != 0,
          True, "exact_residue_arithmetic", "Delta(v=0)=-64, a 3-adic unit")

    special_cubic = [0, 1, 1, 1]  # x^3+x^2+x over F3
    node_factor = mul(t, power([-1, 1], 2))
    check("split_special_node_factorization",
          [x % 3 for x in special_cubic], [x % 3 for x in node_factor],
          "exact_finite_field_polynomial", "x^3+x^2+x=x(x-1)^2 over F3")
    shifted = compose(special_cubic, [1, 1])
    check("split_special_node_tangent_cone", shifted[2] % 3, 1,
          "exact_residue_arithmetic", "At x=1+X, tangent cone is y^2=X^2")
    check("parabolic_rank_formula", (4 - 2) * 5 - (1 + 1 + 3 + 1), 4,
          "conditional_dimension_arithmetic",
          "Assumes the stated local invariant dimensions and no global/dual invariants")

    # CONDITIONAL model: geometric Frob, Tate character Q_l(-1) has value 3.
    n = 4
    eye = ident(n)
    F = [[Q(3 ** (i + 1) if i == j else 0) for j in range(n)] for i in range(n)]
    N = [[Q(1 if j == i + 1 else 0) for j in range(n)] for i in range(n)]
    omega = [[Q((1 if i % 2 == 0 else -1) if j == n - 1 - i else 0)
              for j in range(n)] for i in range(n)]
    check("WD_geometric_Frobenius_relation", mmul(F, N),
          mscale(mmul(N, F), Q(1, 3)), "conditional_WD_matrix", "F*N=N*F/3")
    check("alternating_pairing", transpose(omega), mscale(omega, -1),
          "conditional_WD_matrix")
    check("nondegenerate_pairing", rank(omega), n, "conditional_WD_matrix")
    check("Frobenius_similitude", mmul(mmul(transpose(F), omega), F),
          mscale(omega, 3 ** 5), "conditional_WD_matrix", "F^t*Omega*F=3^5*Omega")
    check("monodromy_infinitesimal_pairing",
          madd(mmul(transpose(N), omega), mmul(omega, N)), zeros(n),
          "conditional_WD_matrix")
    powers = [eye]
    for _ in range(4):
        powers.append(mmul(powers[-1], N))
    n_ranks = [rank(x) for x in powers[1:]]
    check("nilpotent_power_ranks", n_ranks, [3, 2, 1, 0], "conditional_WD_matrix")
    U = madd(madd(eye, N), madd(mscale(powers[2], Q(1, 2)),
                               mscale(powers[3], Q(1, 6))))
    d_plus = n - rank(madd(U, mscale(eye, -1)))
    d_minus = n - rank(madd(mscale(U, -1), mscale(eye, -1)))
    check("unipotent_model_invariants", d_plus, 1, "conditional_WD_matrix")
    check("ramified_quadratic_twist_model_invariants", d_minus, 0,
          "conditional_WD_matrix")
    check("minus_inertia_has_no_one_eigenvalue",
          determinant(madd(mscale(U, -1), mscale(eye, -1))), Q(16),
          "conditional_WD_matrix")
    e1 = [[Q(1)], [Q(0)], [Q(0)], [Q(0)]]
    check("kernel_generator", mmul(N, e1), [[Q(0)] for _ in range(n)],
          "conditional_WD_matrix")
    check("invariant_line_Frobenius", mmul(F, e1), mscale(e1, 3),
          "conditional_WD_matrix")
    swan = 0  # An ASSUMPTION supplied by the proposed tame geometric model.
    a_plus, a_minus = n - d_plus + swan, n - d_minus + swan
    check("conditional_conductor_exponents", [a_plus, a_minus], [3, 4],
          "conditional_conductor_arithmetic", "a=dim(V)-dim(V^I)+Swan; assumes Swan=0")

    report = {
        "schema_version": 1,
        "date": "2026-10-30",
        "method": "standard-library exact integer polynomial and rational matrix arithmetic",
        "historical_experiments_rerun": False,
        "all_checks_passed": all(c["passed"] for c in checks),
        "number_of_checks": len(checks),
        "checks": checks,
        "polynomial_coefficient_order": "ascending degree",
        "conditional_WD_model": {
            "F": serial_matrix(F), "N": serial_matrix(N),
            "Omega": serial_matrix(omega), "U_exp_N": serial_matrix(U),
            "N_power_ranks": n_ranks,
            "plus_inertia_invariant_dimension": d_plus,
            "minus_inertia_invariant_dimension": d_minus,
            "assumed_swan_plus_and_minus": swan,
            "plus_P3_coefficients": [1, -3],
            "minus_P3_coefficients": [1],
            "plus_conductor_exponent": a_plus,
            "minus_conductor_exponent": a_minus,
        },
        "scope_limit": (
            "The polynomial identities are exact. The matrix/conductor results are "
            "conditional on the proposed geometric identification of W4+ with this "
            "tame Weil--Deligne model and W4- with its chi_-3 twist. This program "
            "does not certify nearby-cycle theorems, their hypotheses, the arithmetic "
            "sheaf identification, or that the matrix model is the actual local "
            "representation. Those require a separate written proof."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: {len(checks)} exact checks; report written to {args.output}")
    print("WD and conductor conclusions are CONDITIONAL; nearby cycles are not certified.")


if __name__ == "__main__":
    main()
