parent_living(X) :- father(Y,X), living(Y).
parent_living(X) :- mother(Y,X), living(Y).
orphan(X) :- living(X), not parent_living(X), not neg_orphan(X).
:- orphan(X), neg_orphan(X).

