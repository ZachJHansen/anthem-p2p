index_2(1..8).
type_2(1..3).
{place_2(I,J,IK) : type(IK)} :- index_2(I), index_2(J).
:- place_2(I,J,IK1), place_2(I,J,IK2), index_2(I), index_2(J), type_2(IK1), type_2(IK2), IK1 != IK2.
:- place_2(I1,J1,1), place_2(I2,J2,1), I1 != I2.
:- place_2(I1,J1,1), place_2(I2,J2,1), J1 != J2.
filled_2(I,J) :- place_2(I,J,1), index_2(I), index_2(J).
filled_2(I,J) :- place_2(I,J,2), index_2(I), index_2(J).
filled_2(I+1,J) :- place_2(I,J,2), index_2(I), index_2(J).
filled_2(I+2,J) :- place_2(I,J,2), index_2(I), index_2(J).
filled_2(I,J) :- place_2(I,J,3), index_2(I), index_2(J).
filled_2(I,J+1) :- place_2(I,J,3), index_2(I), index_2(J).
filled_2(I,J+2) :- place_2(I,J,3), index_2(I), index_2(J).
:- not filled_2(I,J), index_2(I), index_2(J).
:- place_2(I,J,2), index_2(I), index_2(J), I>6.
:- place_2(I,J,3), index_2(I), index_2(J), J>6.
:- place_2(I,J,2), place_2(I+1,J,K), index_2(I), index_2(J), type_2(K).
:- place_2(I,J,2), place_2(I+2,J,K), index_2(I), index_2(J), type_2(K).
:- place_2(I,J,2), place_2(I+1,J-1,3), index_2(I), index_2(J).
:- place_2(I,J,2), place_2(I+2,J-1,3), index_2(I), index_2(J).
:- place_2(I,J,2), place_2(I+1,J-2,3), index_2(I), index_2(J).
:- place_2(I,J,2), place_2(I+2,J-2,3), index_2(I), index_2(J).
:- place_2(I,J,3), place_2(I,J+1,K), index_2(I), index_2(J), type_2(K).
:- place_2(I,J,3), place_2(I,J+2,K), index_2(I), index_2(J), type_2(K).
:- place_2(I,J,3), place_2(I-1,J+1,2), index_2(I), index_2(J).
:- place_2(I,J,3), place_2(I-1,J+2,2), index_2(I), index_2(J).
:- place_2(I,J,3), place_2(I-2,J+1,2), index_2(I), index_2(J).
:- place_2(I,J,3), place_2(I-2,J+2,2), index_2(I), index_2(J).
plc(I,J,2) :- place_2(I,J,2).
plc(I,J,3) :- place_2(I,J,3).
