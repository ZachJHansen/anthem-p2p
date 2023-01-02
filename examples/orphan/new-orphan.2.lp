parent_living_1(X) :- father(Y,X), living(Y).
parent_living_1(X) :- mother(Y,X), living(Y).
orphan(X) :- living(X), not parent_living_1(X).
