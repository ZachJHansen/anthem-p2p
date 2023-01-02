input: living/1, father/2, mother/2.
output: orphan/1.
assume: forall X exists Y forall Z (father(Z,X) <-> Y=Z).
assume: forall X exists Y forall Z (mother(Z,X) <-> Y=Z).

spec: forall X1 (orphan(X1) <-> exists X2 (exists X3 (X3 = X2 and living(X3)) and exists X4 (X4 = X2 and not parent_living_1(X4)) and X1 = X2)).
assume: forall X1 (parent_living_1(X1) <-> exists X2, X3 (exists X4, X5 (X4 = X2 and X5 = X3 and father(X4, X5)) and exists X6 (X6 = X2 and living(X6)) and X1 = X3) or exists X7, X8 (exists X9, X10 (X9 = X7 and X10 = X8 and mother(X9, X10)) and exists X11 (X11 = X7 and living(X11)) and X1 = X8)).
input: parent_living_1/1.
