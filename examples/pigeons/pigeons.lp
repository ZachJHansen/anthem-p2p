input_pidgeon(p).
input_hole(h).

pidgeon(J) :- input_pidgeon(N), J=1..N.
hole(I) :- input_hole(K), I=1..K.

{assign(J, I)} :- pidgeon(J), hole(I).
:- assign(J1,I), assign(J2,I), J1 != J2.
:- not assign(J, 1), not assign(J, 2), not assign(J, 3), pidgeon(J).

max_hole(I) :- hole(I), not hole(I+1).
max_pidgeon(J) :- pidgeon(J), not pidgeon(J+1).
 
next_pidgeon(J-1, J) :- max_pidgeon(N), J=1..N.

assignGEQ(J,I) :- assign(J,I).
assignGEQ(J,I-K) :- assign(J,I), K=1..I-1.

:- assignGEQ(J1,I), not assignGEQ(J2,I), next_pidgeon(J1,J2).
