input: n -> integer.
assume: n > 1.
output: prime/1.
assume: forall X1 (composite_1(X1) <-> exists N1, N2 (exists X2, X3 (X2 = N1 and X3 = 1 and X2 > X3) and exists X4, X5 (X4 = N2 and X5 = 1 and X4 > X5) and exists N3, N4 (X1 = N3 * N4 and N3 = N1 and N4 = N2))).
input: composite_1/1.
spec: forall X1 (prime(X1) <-> exists N1 (exists X2, X3 (X2 = N1 and exists N2, N3, N4 (N2 = 2 and N3 = n and N2 <= N4 and N4 <= N3 and X3 = N4) and X2 = X3) and exists X4 (X4 = N1 and not composite_1(X4)) and X1 = N1)).
