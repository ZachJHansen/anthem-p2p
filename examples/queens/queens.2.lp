% place a set of queens on the chess board
{ q(1..n,1..n) }.

% at most one queen per row/column
:- q(X,Y1), q(X,Y2), Y1 != Y2.
:- q(X1,Y), q(X2,Y), X1 != X2.

% Absolute value replacement
diff(X1,X2,X3) :- X1 >= X2, X3 = X1-X2.
diff(X1,X2,X3) :- X2 >= X1, X3 = X2-X1.

% at most one queen per diagonal
:- q(X1,Y1), q(X2,Y2), X1 != X2, diff(X1,X2,XX), diff(Y1,Y2,XY), XX = XY.

% a queen in every column
q(X) :- q(X,Y).
:- not q(X), X = 1..n.

#show q/2.

