#!/usr/bin/env python3
"""Exact small algebra checks used by the p=2 completion argument.

Standard library only; no point counting, numerical fitting, or local
monodromy theorem is implemented.  Polynomial identities and matrices
are calculated over Q and Q(i), respectively.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from math import comb
import argparse
import json


class P:
    """Q[v,eta]/(eta^3-4(v^3+1)); canonical eta degree <3."""
    def __init__(self, a=0):
        if isinstance(a, P): self.a = dict(a.a)
        elif isinstance(a, dict): self.a = {k:F(v) for k,v in a.items() if v}
        else: self.a = {(0,0):F(a)} if a else {}
    def __add__(self, b):
        b=P(b); d=dict(self.a)
        for k,v in b.a.items(): d[k]=d.get(k,F(0))+v
        return P(d)
    __radd__=__add__
    def __neg__(self): return P({k:-v for k,v in self.a.items()})
    def __sub__(self,b): return self+-P(b)
    def __rsub__(self,b): return P(b)+-self
    def __mul__(self,b):
        b=P(b); d={}
        for (v,e),a in self.a.items():
            for (w,f),b0 in b.a.items():
                q,r=divmod(e+f,3)
                for j in range(q+1):
                    k=(v+w+3*j,r)
                    d[k]=d.get(k,F(0))+a*b0*4**q*comb(q,j)
        return P(d)
    __rmul__=__mul__
    def __pow__(self,n):
        assert n>=0
        a=P(1)
        for _ in range(n): a=a*self
        return a
    def __eq__(self,b): return self.a==P(b).a


class G:
    """Exact Gaussian rationals."""
    def __init__(self,a=0,b=0):
        if isinstance(a,G): self.a,self.b=a.a,a.b
        else: self.a,self.b=F(a),F(b)
    def __add__(self,x):
        x=G(x); return G(self.a+x.a,self.b+x.b)
    __radd__=__add__
    def __neg__(self): return G(-self.a,-self.b)
    def __sub__(self,x): return self+-G(x)
    def __rsub__(self,x): return G(x)+-self
    def __mul__(self,x):
        x=G(x); return G(self.a*x.a-self.b*x.b,self.a*x.b+self.b*x.a)
    __rmul__=__mul__
    def __truediv__(self,x):
        x=G(x); q=x.a*x.a+x.b*x.b
        return G((self.a*x.a+self.b*x.b)/q,(self.b*x.a-self.a*x.b)/q)
    def __pow__(self,n):
        a=G(1)
        for _ in range(n): a=a*self
        return a
    def __eq__(self,x):
        x=G(x); return self.a==x.a and self.b==x.b
    def __bool__(self): return bool(self.a or self.b)


def eye(n): return [[G(int(i==j)) for j in range(n)] for i in range(n)]
def zero(n): return [[G() for _ in range(n)] for _ in range(n)]
def ma(A,B): return [[a+b for a,b in zip(x,y)] for x,y in zip(A,B)]
def ms(A,c): return [[a*c for a in x] for x in A]
def mm(A,B):
    return [[sum((a*b for a,b in zip(row,col)),G())
             for col in zip(*B)] for row in A]
def trace(A): return sum((A[i][i] for i in range(len(A))),G())
def power(A,n):
    B=eye(len(A))
    for _ in range(n): B=mm(B,A)
    return B
def rank(A):
    A=[list(r) for r in A]; m=len(A); n=len(A[0]); r=0
    for c in range(n):
        p=next((i for i in range(r,m) if A[i][c]),None)
        if p is None: continue
        A[r],A[p]=A[p],A[r]; t=A[r][c]
        A[r]=[x/t for x in A[r]]
        for i in range(m):
            if i!=r:
                t=A[i][c]; A[i]=[x-t*y for x,y in zip(A[i],A[r])]
        r+=1
        if r==m: break
    return r
def sym4(A):
    # Columns act on e^(4-j)f^j, with Ae=a*e+c*f, Af=b*e+d*f.
    a,b=A[0]; c,d=A[1]; S=zero(5)
    for j in range(5):
        for k in range(5-j):
            for t in range(j+1):
                S[k+t][j]+=comb(4-j,k)*comb(j,t)*a**(4-j-k)*c**k*b**(j-t)*d**t
    return S


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,default=Path(__file__).with_suffix('.json'))
    args=ap.parse_args(); results=[]
    def check(name, a, b, detail=''):
        passed=a==b; results.append(dict(name=name,passed=passed,detail=detail))
        if not passed: raise AssertionError(name)

    v=P({(1,0):1}); eta=P({(0,1):1}); h=v**3; D=2*h+1; zn=v*(h+2)
    check('closure_equation',eta**3,4*(h+1))
    check('quartic_known_root_cleared',D*v**4-2*zn*v**3+2*D*v-zn,0)
    a=v-F(1,2)*eta**2-v**2*eta
    check('quartic_other_root_cleared',a**4-2*zn*a**3+2*a*D**3-zn*D**3,0,
          'The other two roots follow by eta -> zeta*eta.')
    check('cubic_other_root_cleared',a**3-3*v*a**2-3*v**2*a*D+(h+2)*D**2,0)
    check('branch_factorization',zn**3-D**3,(h-1)**3*(h+1))
    # Disc(X^4+bX^3+dX+e), c=0, applied b=-2z,d=2,e=-z.
    # The polynomial variable v is reused as an indeterminate z here.
    z=v; b=-2*z; d=P(2); e=-z
    disc=256*e**3-192*b*d*e**2-27*d**4-6*b**2*d**2*e-27*b**4*e**2-4*b**3*d**3
    check('quartic_discriminant',disc,-432*(z**3-1)**2)
    check('Fermat_Weierstrass_identity',81*(1-v)**2*(v+1),27*eta**3-27*(v+1)**3)

    ii=G(0,1); E=eye(2)
    I=[[ii,G()],[G(),-ii]]
    J=[[G(),G(1)],[G(-1),G()]]
    K=mm(I,J)
    C=ms(ma(ma(ms(E,-1),I),ma(J,K)),F(1,2))
    check('quaternion_I_square',mm(I,I),ms(E,-1))
    check('quaternion_J_square',mm(J,J),ms(E,-1))
    check('quaternion_anticommutation',mm(J,I),ms(K,-1))
    check('binary_tetrahedral_C_order3',power(C,3),E)
    # This convention cycles I -> K -> J -> I.
    check('binary_tetrahedral_normalizes_Q8',mm(mm(C,I),power(C,2)),K)
    SI,SJ,SK,SC=map(sym4,(I,J,K,C)); E5=eye(5)
    Pq=ms(ma(ma(E5,SI),ma(SJ,SK)),F(1,4))
    check('Q8_projector_idempotent',mm(Pq,Pq),Pq)
    check('Q8_Sym4_invariant_dimension',rank(Pq),2)
    check('C3_commutes_Q8_projector',mm(SC,Pq),mm(Pq,SC))
    check('C3_trace_on_Q8_invariants',trace(mm(Pq,SC)),G(-1))
    check('C3_character_relation_on_Q8_invariants',mm(Pq,ma(ma(E5,SC),power(SC,2))),zero(5))
    check('binary_tetrahedral_Sym4_invariants',
          rank(mm(Pq,ms(ma(ma(E5,SC),power(SC,2)),F(1,3)))),0)
    check('Sym4_order4_trace',trace(SI),G(1))
    check('Sym4_order3_trace',trace(SC),G(-1))

    out=dict(checks=results,all_passed=all(x['passed'] for x in results),
             scope='Exact algebra only; geometric descent, nearby cycles, and tail vanishing require separate proofs.')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(f"{len(results)} exact checks passed; wrote {args.output}")


if __name__=='__main__': main()
