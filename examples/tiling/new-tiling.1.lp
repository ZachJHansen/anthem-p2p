{h_1(1..8,1..6)}. 
{v_1(1..6,1..8)}. 
square_1(1..8,1..8).
covered_1(IR,IC) :- h_1(IR,IC).
covered_1(IR,IC+1) :- h_1(IR,IC).
covered_1(IR,IC+2) :- h_1(IR,IC).
covered_1(IR,IC) :- v_1(IR,IC).
covered_1(IR+1,IC) :- v_1(IR,IC).
covered_1(IR+2,IC) :- v_1(IR,IC).
:- IR1 != IR2, square_1(IR1,IC1), square_1(IR2,IC2),
                    not covered_1(IR1,IC1), not covered_1(IR2,IC2).
:- IC1 != IC2, square_1(IR1,IC1), square_1(IR2,IC2),
                    not covered_1(IR1,IC1), not covered_1(IR2,IC2).
:- h_1(IR,IC), h_1(IR,IC+(1..2)).
:- v_1(IR,IC), v_1(IR+(1..2),IC).
:- h_1(IR,IC), v_1(IR-(0..2),IC+(0..2)).
plc(X,Y,2) :- h_1(X,Y).
plc(X,Y,3) :- v_1(X,Y).
