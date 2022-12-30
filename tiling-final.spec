output: plc/3.

assume: forall X1, X2 (covered_1(X1, X2) <-> exists X3, X4 (exists X5, X6 (X5 = X3 and X6 = X4 and h_1(X5, X6)) and X1 = X3 and X2 = X4) or exists X7, X8 (exists X9, X10 (X9 = X7 and X10 = X8 and h_1(X9, X10)) and X1 = X7 and exists N1, N2 (X2 = N1 + N2 and N1 = X8 and N2 = 1)) or exists X11, X12 (exists X13, X14 (X13 = X11 and X14 = X12 and h_1(X13, X14)) and X1 = X11 and exists N3, N4 (X2 = N3 + N4 and N3 = X12 and N4 = 2)) or exists X15, X16 (exists X17, X18 (X17 = X15 and X18 = X16 and v_1(X17, X18)) and X1 = X15 and X2 = X16) or exists X19, X20 (exists X21, X22 (X21 = X19 and X22 = X20 and v_1(X21, X22)) and exists N5, N6 (X1 = N5 + N6 and N5 = X19 and N6 = 1) and X2 = X20) or exists X23, X24 (exists X25, X26 (X25 = X23 and X26 = X24 and v_1(X25, X26)) and exists N7, N8 (X1 = N7 + N8 and N7 = X23 and N8 = 2) and X2 = X24)).
input: covered_1/2.
assume: forall X1, X2 (h_1(X1, X2) <-> h_1(X1, X2) and exists N1, N2, N3 (N1 = 1 and N2 = 8 and N1 <= N3 and N3 <= N2 and X1 = N3) and exists N4, N5, N6 (N4 = 1 and N5 = 6 and N4 <= N6 and N6 <= N5 and X2 = N6)).
input: h_1/2.
spec: forall X1, X2, X3 (plc(X1, X2, X3) <-> exists X4, X5 (exists X6, X7 (X6 = X4 and X7 = X5 and h_1(X6, X7)) and X1 = X4 and X2 = X5 and X3 = 2) or exists X8, X9 (exists X10, X11 (X10 = X8 and X11 = X9 and v_1(X10, X11)) and X1 = X8 and X2 = X9 and X3 = 3)).
assume: forall X1, X2 (square_1(X1, X2) <-> exists N1, N2, N3 (N1 = 1 and N2 = 8 and N1 <= N3 and N3 <= N2 and X1 = N3) and exists N4, N5, N6 (N4 = 1 and N5 = 8 and N4 <= N6 and N6 <= N5 and X2 = N6)).
input: square_1/2.
assume: forall X1, X2 (v_1(X1, X2) <-> v_1(X1, X2) and exists N1, N2, N3 (N1 = 1 and N2 = 6 and N1 <= N3 and N3 <= N2 and X1 = N3) and exists N4, N5, N6 (N4 = 1 and N5 = 8 and N4 <= N6 and N6 <= N5 and X2 = N6)).
input: v_1/2.
spec: forall X1, X2, X3, X4 not (exists X5, X6 (X5 = X1 and X6 = X2 and X5 != X6) and exists X7, X8 (X7 = X1 and X8 = X3 and square_1(X7, X8)) and exists X9, X10 (X9 = X2 and X10 = X4 and square_1(X9, X10)) and exists X11, X12 (X11 = X1 and X12 = X3 and not covered_1(X11, X12)) and exists X13, X14 (X13 = X2 and X14 = X4 and not covered_1(X13, X14))).
spec: forall X1, X2, X3, X4 not (exists X5, X6 (X5 = X1 and X6 = X2 and X5 != X6) and exists X7, X8 (X7 = X3 and X8 = X1 and square_1(X7, X8)) and exists X9, X10 (X9 = X4 and X10 = X2 and square_1(X9, X10)) and exists X11, X12 (X11 = X3 and X12 = X1 and not covered_1(X11, X12)) and exists X13, X14 (X13 = X4 and X14 = X2 and not covered_1(X13, X14))).
spec: forall X1, X2 not (exists X3, X4 (X3 = X1 and X4 = X2 and h_1(X3, X4)) and exists X5, X6 (X5 = X1 and exists N1, N2 (X6 = N1 + N2 and N1 = X2 and exists N3, N4, N5 (N3 = 1 and N4 = 2 and N3 <= N5 and N5 <= N4 and N2 = N5)) and h_1(X5, X6))).
spec: forall X1, X2 not (exists X3, X4 (X3 = X1 and X4 = X2 and v_1(X3, X4)) and exists X5, X6 (exists N1, N2 (X5 = N1 + N2 and N1 = X1 and exists N3, N4, N5 (N3 = 1 and N4 = 2 and N3 <= N5 and N5 <= N4 and N2 = N5)) and X6 = X2 and v_1(X5, X6))).
spec: forall X1, X2 not (exists X3, X4 (X3 = X1 and X4 = X2 and h_1(X3, X4)) and exists X5, X6 (exists N1, N2 (X5 = N1 - N2 and N1 = X1 and exists N3, N4, N5 (N3 = 0 and N4 = 2 and N3 <= N5 and N5 <= N4 and N2 = N5)) and exists N6, N7 (X6 = N6 + N7 and N6 = X2 and exists N8, N9, N10 (N8 = 0 and N9 = 2 and N8 <= N10 and N10 <= N9 and N7 = N10)) and v_1(X5, X6))).