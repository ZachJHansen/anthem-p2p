input: living/1, father/2, mother/2.
output: orphan/1.
assume: forall X exists Y forall Z (father(Z,X) <-> Y=Z).
assume: forall X exists Y forall Z (mother(Z,X) <-> Y=Z).

spec: forall X1 (orphan(X1) <-> exists X2, X3, X4 (exists X5 (X5 = X2 and living(X5)) and exists X6, X7 (X6 = X3 and X7 = X2 and father(X6, X7)) and exists X8, X9 (X8 = X4 and X9 = X2 and mother(X8, X9)) and exists X10 (X10 = X3 and not living(X10)) and exists X11 (X11 = X4 and not living(X11)) and X1 = X2)).
