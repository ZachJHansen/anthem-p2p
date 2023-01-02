{ q_1(1..n,1..n) }.
:- q_1(X,Y1), q_1(X,Y2), Y1 != Y2.
:- q_1(X1,Y), q_1(X2,Y), X1 != X2.
diff_1(X1,X2,X3) :- X1 >= X2, X3 = X1-X2.
diff_1(X1,X2,X3) :- X2 >= X1, X3 = X2-X1.
:- q_1(X1,Y1), q_1(X2,Y2), X1 != X2, diff_1(X1,X2,X3X), diff_1(Y1,Y2,X3Y), X3X = X3Y.
q(X) :- q_1(X,Y).
:- not q(X), X = 1..n.
