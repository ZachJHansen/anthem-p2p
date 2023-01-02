{h(1..8,1..6)}. 
{v(1..6,1..8)}. 
square(1..8,1..8).

covered(IR,IC) :- h(IR,IC).
covered(IR,IC+1) :- h(IR,IC).
covered(IR,IC+2) :- h(IR,IC).
covered(IR,IC) :- v(IR,IC).
covered(IR+1,IC) :- v(IR,IC).
covered(IR+2,IC) :- v(IR,IC).

% anthem: language feature not yet supported (elements other than terms in rule head)
%(IR1,IC1) = (IR2,IC2) :- square(IR1,IC1), square(IR2,IC2),
%                    not covered(IR1,IC1), not covered(IR2,IC2).

% replace with:
:- IR1 != IR2, square(IR1,IC1), square(IR2,IC2),
                    not covered(IR1,IC1), not covered(IR2,IC2).
:- IC1 != IC2, square(IR1,IC1), square(IR2,IC2),
                    not covered(IR1,IC1), not covered(IR2,IC2).


:- h(IR,IC), h(IR,IC+(1..2)).

:- v(IR,IC), v(IR+(1..2),IC).

:- h(IR,IC), v(IR-(0..2),IC+(0..2)).

%#show h/2.
%#show v/2.

plc(X,Y,2) :- h(X,Y).
plc(X,Y,3) :- v(X,Y).

#show plc/3.




