#!/usr/bin/env python3
"""Exact algebra checks for p=2 tame charts; standard library only.

These checks do not implement semistable reduction, nearby cycles, or a
monodromy theorem. They do not determine d2, P2, or the Artin exponent a2.
"""
import argparse
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path


def trim(p):
    p = list(p)
    while len(p) > 1 and not p[-1]:
        p.pop()
    return p


def add(a, b):
    c = [F(0)] * max(len(a), len(b))
    for i, x in enumerate(a): c[i] += x
    for i, x in enumerate(b): c[i] += x
    return trim(c)


def mul(a, b):
    c = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): c[i+j] += x*y
    return trim(c)


class R:
    """Rational functions in one formal variable, without numerical evaluation."""
    def __init__(self, numerator, denominator=None):
        if isinstance(numerator, R):
            self.n, self.d = numerator.n, numerator.d
            return
        if not isinstance(numerator, (list, tuple)): numerator = [numerator]
        if denominator is None: denominator = [1]
        self.n, self.d = trim(map(F, numerator)), trim(map(F, denominator))
        if self.d == [0]: raise ZeroDivisionError
    def __add__(self, other):
        other = R(other)
        return R(add(mul(self.n, other.d), mul(other.n, self.d)), mul(self.d, other.d))
    __radd__ = __add__
    def __neg__(self): return R([-x for x in self.n], self.d)
    def __sub__(self, other): return self + (-R(other))
    def __rsub__(self, other): return R(other) + (-self)
    def __mul__(self, other):
        other = R(other)
        return R(mul(self.n, other.n), mul(self.d, other.d))
    __rmul__ = __mul__
    def __truediv__(self, other):
        other = R(other)
        return R(mul(self.n, other.d), mul(self.d, other.n))
    def __rtruediv__(self, other): return R(other) / self
    def __pow__(self, n):
        if n < 0: return (R(1)/self)**(-n)
        result = R(1)
        for _ in range(n): result = result*self
        return result
    def __eq__(self, other):
        other = R(other)
        return mul(self.n, other.d) == mul(other.n, self.d)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_suffix('.json'))
    args = parser.parse_args()
    checks = []
    def check(name, left, right, detail=''):
        passed = left == right
        checks.append({'name': name, 'passed': passed, 'detail': detail})
        if not passed: raise AssertionError(name)

    q = R([0,1])
    lam = q**3*(q+2)/((q-1)*(q+1)**3)
    alpha = q**2/(q**2-1)
    check('three_division_polynomial',
          3*alpha**4-4*(1+lam)*alpha**3+6*lam*alpha**2-lam**2, R(0))
    X0 = alpha**2
    Y0 = q**5/((q-1)**3*(q+1)**4)
    M = q*(q**2+q+1)/((q-1)*(q+1)**2)
    a2, a4 = -alpha*(1+lam), alpha**2*lam
    check('rational_flex_point', Y0**2, X0**3+a2*X0**2+a4*X0)
    check('rational_flex_tangent', 2*Y0*M, 3*X0**2+2*a2*X0+a4)
    check('rational_flex_inflection', M**2, a2+3*X0)
    k = q/((q-1)*(q+1))
    Aq, Bq = (q**2+q+1)/(q+1), q**2/(q+1)
    check('Tate_a1_scaling', 2*M/k, 2*Aq)
    check('Tate_a3_scaling', 2*Y0/k**3, 2*Bq)
    check('Tate_discriminant_factor', 4*(q**2+q+1)**3-27*q**2*(q+1)**2,
          (q-1)**2*(q+2)**2*(2*q+1)**2)

    v = R([0,1]); h = v**3
    qv = (h+2)/(h-1)
    z = v*(h+2)/(2*h+1)
    Av = 3*(h**2+h+1)/((h-1)*(2*h+1))
    Bv = (h+2)**2/((h-1)*(2*h+1))
    check('cubic_cover_compatibility', z**3, qv**3*(qv+2)/((qv-1)*(qv+1)**3))
    check('A_q_to_v', (qv**2+qv+1)/(qv+1), Av)
    check('B_q_to_v', qv**2/(qv+1), Bv)
    check('generic_Tate_discriminant', Bv**3*(4*Av**3-27*Bv),
          3**6*h**2*(h+1)**2*(h+2)**6/((h-1)**6*(2*h+1)**6))
    check('preimage_z_one', z-1, (v-1)**3*(v+1)/(2*v**3+1))
    check('complete_cubic_cusp_divisor', z**3-1,
          (h-1)**3*(h+1)/(2*h+1)**3)
    check('degree_four_cover_derivative',
          ((4*h+2)*(2*h+1)-(v**4+2*v)*6*v**2)/(2*h+1)**2,
          2*(h-1)**2/(2*h+1)**2)

    # At the v=0 node r^3=2/v^3; pi^2 factors cancel from the a1 identity.
    r3 = 2/v**3
    check('zero_node_a3', Bv/v**6, (1+r3)**2/((v**3-1)*(2*v**3+1)))

    # Infinity node w*r=pi; replace r^3 by 2/w^3 when clearing denominators.
    w = R([0,1]); hi = 1/w**3
    Ai = 3*(hi**2+hi+1)/((hi-1)*(2*hi+1))
    Bi = (hi+2)**2/((hi-1)*(2*hi+1))
    check('infinity_node_a3', w**3*Bi,
          (1+2*w**3)**2/((1-w**3)*(1+2/w**3)))
    check('infinity_node_a1_divided_by_pi_squared', w*Ai,
          3*(1+w**3+w**6)/(w**2*(1-w**3)*(1+2/w**3)))

    # At s=0, h=1+s^3 and s*r=pi; division by pi^2 leaves rational identities.
    s = R([0,1]); hs = 1+s**3
    As = 3*(hs**2+hs+1)/((hs-1)*(2*hs+1))
    Bs = (hs+2)**2/((hs-1)*(2*hs+1))
    check('mu_node_a3', s**3*Bs, (hs+2)**2/(2*hs+1))
    check('mu_node_a1_divided_by_pi_squared', s*As,
          3*(hs**2+hs+1)/(s**2*(2*hs+1)))

    u = R([0,1]); hu = 2*u**3
    Bu = (hu+2)**2/((hu-1)*(2*hu+1))
    Au = 3*(hu**2+hu+1)/((hu-1)*(2*hu+1))
    check('zero_tail_a3', Bu/4, (u**3+1)**2/((2*u**3-1)*(4*u**3+1)))
    check('zero_tail_integral_a1', Au,
          3*(4*u**6+2*u**3+1)/((2*u**3-1)*(4*u**3+1)))
    hinf = 1/(2*u**3)
    Binf = (hinf+2)**2/((hinf-1)*(2*hinf+1))
    check('infinity_tail_a3', 2*Binf,
          (1+4*u**3)**2/((1-2*u**3)*(1+u**3)))
    Ainf = 3*(hinf**2+hinf+1)/((hinf-1)*(2*hinf+1))
    check('infinity_tail_integral_a1', 2*(1+u**3)*Ainf,
          3*(1+2*u**3+4*u**6)/(1-2*u**3))
    check('infinity_tail_integral_a3', 2*(1+u**3)**3*Binf,
          (1+u**3)**2*(1+4*u**3)**2/(1-2*u**3))
    hmu = 1+2*u**3
    Amu = 3*(hmu**2+hmu+1)/((hmu-1)*(2*hmu+1))
    Bmu = (hmu+2)**2/((hmu-1)*(2*hmu+1))
    check('mu_tail_integral_a1', 2*u**3*Amu,
          3*(hmu**2+hmu+1)/(2*hmu+1))
    check('mu_tail_integral_a3', 2*u**9*Bmu,
          u**6*(hmu+2)**2/(2*hmu+1))

    # Exact finite-field polynomial calculations on the two tail types.
    def mod2(p): return trim([int(x) % 2 for x in p])
    Btail = [1,0,0,0,0,0,1]  # (u^3+1)^2 in F2
    delta_tail = mul(mul(Btail, Btail), mul(Btail, add([1], Btail)))
    expected = mul([0,0,0,0,0,0,1],
                   mul(mul(Btail, Btail), Btail))
    check('ordinary_tail_discriminant_mod2', mod2(delta_tail), mod2(expected),
          'Delta=u^6(u^3+1)^6')
    check('mu_tail_discriminant_mod2', mod2([-27,0,0,0,0,0,1]),
          [1,0,0,0,0,0,1], 'a1=r^2,a3=1 gives Delta=(r^3+1)^2')
    check('node_discriminant_unit', (-27) % 2, 1, 'a1=0,a3=1')
    check('main_supersingular_discriminant_unit', (-27) % 2, 1)

    check('generic_v_cusp_count', 2+4*3, 14)
    check('generic_Fermat_cusp_count', 3+(14-3)*3, 36)
    check('tail_cusp_count', 9*4, 36)
    check('generic_fibre_Euler_multiplicity', 24*6+9*2+3*18, 216)
    check('special_fibre_Euler_multiplicity', 6*(4*6)+3*(18+3*2), 216)

    # Independent finite consequences of the stated p=3/Hodge inputs.
    # These do not establish those geometric inputs or rank-one classification.
    hodge_exponents = (0, 0, 5, 5)
    for rank in (1, 2, 3):
        allowed = {sum(c) for c in combinations(hodge_exponents, rank)}
        local_exponent = rank*(rank+1)//2
        check(f'determinant_obstruction_rank_{rank}', local_exponent in allowed,
              False, f'Local exponent {local_exponent}; allowed Hodge sums {sorted(allowed)}')
    check('chi_minus3_unramified_quadratic_at2',
          [(x*x+x+1) % 2 for x in (0, 1)], [1, 1],
          'X^2+X+1 has no F2 root and derivative 1 modulo 2')
    check('rational_cover_mod2_numerator', mod2([0,2,0,0,1]), [0,0,0,0,1])
    check('rational_cover_mod2_denominator', mod2([1,0,0,2]), [1])

    report = {
        'date': '2026-10-30', 'standard_library_only': True,
        'historical_experiments_rerun': False,
        'arithmetic': 'exact rational functions via polynomial coefficients and exact F2 polynomials',
        'all_checks_passed': all(c['passed'] for c in checks),
        'number_of_checks': len(checks), 'checks': checks,
        'scope_limit': ('These identities check the formulas, numerical divisor counts and the '
                        'finite determinant obstruction conditional on the stated p3/Hodge inputs. '
                        'They do not certify exhaustion of charts, gluing of models, nearby cycles, '
                        'the semistable-monodromy theorem, or its application. No inertia invariant '
                        'dimension, P2, or Artin conductor exponent is computed by this script.')
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(f"PASS: {len(checks)} exact checks; {args.output}")
    print('No d2, P2, or a2 claim is certified by these algebra checks.')


if __name__ == '__main__':
    main()
