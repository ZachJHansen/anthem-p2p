% Cover the 8-by-8 chessboard by twenty-one 3-by-1 tiles and
% one 1-by-1 tile.

% h(R,C) means that there is a tile at (R,C), (R,C+1), (R,C+2).
% v(R,C) means that there is a tile at (R,C), (R+1,C), (R+2,C).

% anthem: could not translate input program: language feature not yet supported (aggregates not containing exactly one element)
%{h(1..8,1..6); v(1..6,1..8)}. 

% replace with:
{h(1..8,1..6)}. 
{v(1..6,1..8)}. 

square(1..8,1..8).

covered(XR,XC) :- h(XR,XC).
covered(XR,XC+1) :- h(XR,XC).
covered(XR,XC+2) :- h(XR,XC).
covered(XR,XC) :- v(XR,XC).
covered(XR+1,XC) :- v(XR,XC).
covered(XR+2,XC) :- v(XR,XC).

% anthem: language feature not yet supported (elements other than terms in rule head)
%(XR1,XC1) = (XR2,XC2) :- square(XR1,XC1), square(XR2,XC2),
%                    not covered(XR1,XC1), not covered(XR2,XC2).

% replace with:
:- XR1 != XR2, square(XR1,XC1), square(XR2,XC2),
                    not covered(XR1,XC1), not covered(XR2,XC2).
:- XC1 != XC2, square(XR1,XC1), square(XR2,XC2),
                    not covered(XR1,XC1), not covered(XR2,XC2).


:- h(XR,XC), h(XR,XC+(1..2)).

:- v(XR,XC), v(XR+(1..2),XC).

:- h(XR,XC), v(XR-(0..2),XC+(0..2)).

%#show h/2.
%#show v/2.

plc(X,Y,2) :- h(X,Y).
plc(X,Y,3) :- v(X,Y).

#show plc/3.




