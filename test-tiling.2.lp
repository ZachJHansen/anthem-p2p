index(1..8).
type(1..3).
{place(X,Y,XT) : type(XT)} :- index(X), index(Y).
