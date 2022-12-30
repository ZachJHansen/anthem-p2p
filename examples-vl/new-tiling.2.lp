index_2(1..8).
type_2(1..3).
{place_2(X,Y,XT) : type_2(XT)} :- index_2(X), index_2(Y).
:- place_2(X,Y,XT1), place_2(X,Y,XT2), index_2(X), index_2(Y), type_2(XT1), type_2(XT2), XT1 != XT2.
:- place_2(X1,Y1,1), place_2(X2,Y2,1), X1 != X2.
:- place_2(X1,Y1,1), place_2(X2,Y2,1), Y1 != Y2.
filled_2(X,Y) :- place_2(X,Y,1), index_2(X), index_2(Y).
filled_2(X,Y) :- place_2(X,Y,2), index_2(X), index_2(Y).
filled_2(X+1,Y) :- place_2(X,Y,2), index_2(X), index_2(Y).
filled_2(X+2,Y) :- place_2(X,Y,2), index_2(X), index_2(Y).
filled_2(X,Y) :- place_2(X,Y,3), index_2(X), index_2(Y).
filled_2(X,Y+1) :- place_2(X,Y,3), index_2(X), index_2(Y).
filled_2(X,Y+2) :- place_2(X,Y,3), index_2(X), index_2(Y).
:- not filled_2(X,Y), index_2(X), index_2(Y).
:- place_2(X,Y,2), index_2(X), index_2(Y), X>6.
:- place_2(X,Y,3), index_2(X), index_2(Y), Y>6.
:- place_2(X,Y,2), place_2(X+1,Y,T), index_2(X), index_2(Y), type_2(T).
:- place_2(X,Y,2), place_2(X+2,Y,T), index_2(X), index_2(Y), type_2(T).
:- place_2(X,Y,2), place_2(X+1,Y-1,3), index_2(X), index_2(Y).
:- place_2(X,Y,2), place_2(X+2,Y-1,3), index_2(X), index_2(Y).
:- place_2(X,Y,2), place_2(X+1,Y-2,3), index_2(X), index_2(Y).
:- place_2(X,Y,2), place_2(X+2,Y-2,3), index_2(X), index_2(Y).
:- place_2(X,Y,3), place_2(X,Y+1,T), index_2(X), index_2(Y), type_2(T).
:- place_2(X,Y,3), place_2(X,Y+2,T), index_2(X), index_2(Y), type_2(T).
:- place_2(X,Y,3), place_2(X-1,Y+1,2), index_2(X), index_2(Y).
:- place_2(X,Y,3), place_2(X-1,Y+2,2), index_2(X), index_2(Y).
:- place_2(X,Y,3), place_2(X-2,Y+1,2), index_2(X), index_2(Y).
:- place_2(X,Y,3), place_2(X-2,Y+2,2), index_2(X), index_2(Y).
plc(X,Y,2) :- place_2(X,Y,2).
plc(X,Y,3) :- place_2(X,Y,3).
