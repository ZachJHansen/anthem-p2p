{h_1(1..8,1..6)}. 
{v_1(1..6,1..8)}. 
square_1(1..8,1..8).
covered_1(XR,XC) :- h_1(XR,XC).
covered_1(XR,XC+1) :- h_1(XR,XC).
covered_1(XR,XC+2) :- h_1(XR,XC).
covered_1(XR,XC) :- v_1(XR,XC).
covered_1(XR+1,XC) :- v_1(XR,XC).
covered_1(XR+2,XC) :- v_1(XR,XC).
:- XR1 != XR2, square_1(XR1,XC1), square_1(XR2,XC2),
                    not covered_1(XR1,XC1), not covered_1(XR2,XC2).
:- XC1 != XC2, square_1(XR1,XC1), square_1(XR2,XC2),
                    not covered_1(XR1,XC1), not covered_1(XR2,XC2).
:- h_1(XR,XC), h_1(XR,XC+(1..2)).
:- v_1(XR,XC), v_1(XR+(1..2),XC).
:- h_1(XR,XC), v_1(XR-(0..2),XC+(0..2)).
plc(X,Y,2) :- h_1(X,Y).
plc(X,Y,3) :- v_1(X,Y).
