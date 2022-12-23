orphan(X) :- living(X), father(Z,X), mother(Y,X),
             not living(Z), not living(Y),
	     not neg_orphan(X).
:- orphan(X), neg_orphan(X).	     
