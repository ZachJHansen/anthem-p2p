input: n -> integer.
assume: n >= 1.
output: q/1.


assume: forall X1, X2, X3 (diff_1(X1, X2, X3) <-> exists X4, X5, X6 (exists X7, X8 (X7 = X4 and X8 = X5 and X7 >= X8) and exists X9, X10 (X9 = X6 and exists N1, N2 (X10 = N1 - N2 and N1 = X4 and N2 = X5) and X9 = X10) and X1 = X4 and X2 = X5 and X3 = X6) or exists X11, X12, X13 (exists X14, X15 (X14 = X11 and X15 = X12 and X14 >= X15) and exists X16, X17 (X16 = X13 and exists N3, N4 (X17 = N3 - N4 and N3 = X11 and N4 = X12) and X16 = X17) and X1 = X12 and X2 = X11 and X3 = X13)).
input: diff_1/3.
spec: forall X1 (q(X1) <-> exists X2, X3 (exists X4, X5 (X4 = X2 and X5 = X3 and q_1(X4, X5)) and X1 = X2)).
assume: forall X1, X2 (q_1(X1, X2) <-> q_1(X1, X2) and exists N1, N2, N3 (N1 = 1 and N2 = n and N1 <= N3 and N3 <= N2 and X1 = N3) and exists N4, N5, N6 (N4 = 1 and N5 = n and N4 <= N6 and N6 <= N5 and X2 = N6)).
input: q_1/2.
spec: forall X1, X2, X3 not (exists X4, X5 (X4 = X1 and X5 = X2 and q_1(X4, X5)) and exists X6, X7 (X6 = X1 and X7 = X3 and q_1(X6, X7)) and exists X8, X9 (X8 = X2 and X9 = X3 and X8 != X9)).
spec: forall X1, X2, X3 not (exists X4, X5 (X4 = X1 and X5 = X2 and q_1(X4, X5)) and exists X6, X7 (X6 = X3 and X7 = X2 and q_1(X6, X7)) and exists X8, X9 (X8 = X1 and X9 = X3 and X8 != X9)).
spec: forall X1, X2, X3, X4, X5, X6 not (exists X7, X8 (X7 = X1 and X8 = X2 and q_1(X7, X8)) and exists X9, X10 (X9 = X3 and X10 = X4 and q_1(X9, X10)) and exists X11, X12 (X11 = X1 and X12 = X3 and X11 != X12) and exists X13, X14, X15 (X13 = X1 and X14 = X3 and X15 = X5 and diff_1(X13, X14, X15)) and exists X16, X17, X18 (X16 = X2 and X17 = X4 and X18 = X6 and diff_1(X16, X17, X18)) and exists X19, X20 (X19 = X5 and X20 = X6 and X19 = X20)).
spec: forall X1 not (exists X2 (X2 = X1 and not q(X2)) and exists X3, X4 (X3 = X1 and exists N1, N2, N3 (N1 = 1 and N2 = n and N1 <= N3 and N3 <= N2 and X4 = N3) and X3 = X4)).
