{ q_2(1..n,1..n) }.
:- q_2(X,Y1), q_2(X,Y2), Y1 != Y2.
:- q_2(X1,Y), q_2(X2,Y), X1 != X2.
diff_2(X1,X2,X3) :- X1 >= X2, X3 = X1-X2.
diff_2(X1,X2,X3) :- X2 >= X1, X3 = X2-X1.
:- q_2(X1,Y1), q_2(X2,Y2), X1 != X2, diff_2(X1,X2,XX), diff_2(Y1,Y2,XY), XX = XY.
q(X) :- q_2(X,Y).
:- not q(X), X = 1..n.
