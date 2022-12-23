input: p/1.
output: r/1.

assume: forall X1 (q_1(X1) <-> exists X2 (exists X3 (X3 = X2 and r(X3)) and X1 = X2)).
input: q_1/1.
spec: forall X1 (r(X1) <-> exists X2 (exists X3 (X3 = X2 and p(X3)) and X1 = X2)).
