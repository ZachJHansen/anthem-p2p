index(1..8).
type(1..3).
place(X,Y,Z) :- index(X), index(Y), type(Z).
:- place(X,Y,2), place(X+2,Y,A), index(X), index(Y), type(A).
