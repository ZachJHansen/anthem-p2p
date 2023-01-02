output: q/1.

assume: forall X (pp_1(X) <-> X = a).
input: pp_1/1.
spec: forall X1 (q(X1) <-> exists X2 (exists X3 (X3 = X2 and pp_1(X3)) and X1 = X2)).
