index(1..8).
type(1..3).

% IK = 1: a 1x1 tile.
% IK = 2: a horizontal 3x1 tile which the leftmost tile is at (I,J).
% IK = 3: a vertical 3x1 tile which the topmost tile is at (I,J).

% We can place at most one type of tile at one location.
% Anthem: language feature not yet supported (aggregates with guards)
%{place(I,J,IK) : type(IK)} 1 :- index(I), index(J).

% replace with:
{place(I,J,IK) : type(IK)} :- index(I), index(J).
:- place(I,J,IK1), place(I,J,IK2), index(I), index(J), type(IK1), type(IK2), IK1 != IK2.

% We should use exactly one 1x1 tile.
% Anthem: language feature not yet supported (aggregates with guards)
%:- 2 {place(I,J,1) : index(I), index(J)}.
%:- {place(I,J,1) : index(I), index(J)} 0.

% replace with:
:- place(I1,J1,1), place(I2,J2,1), I1 != I2.
:- place(I1,J1,1), place(I2,J2,1), J1 != J2.


% filled(I,J) means (I,J) is covered by one of the tiles.
filled(I,J) :- place(I,J,1), index(I), index(J).
filled(I,J) :- place(I,J,2), index(I), index(J).
filled(I+1,J) :- place(I,J,2), index(I), index(J).
filled(I+2,J) :- place(I,J,2), index(I), index(J).
filled(I,J) :- place(I,J,3), index(I), index(J).
filled(I,J+1) :- place(I,J,3), index(I), index(J).
filled(I,J+2) :- place(I,J,3), index(I), index(J).

% Khe chessboard should be covered.
:- not filled(I,J), index(I), index(J).

% Khe tile should be in the chessboard.
:- place(I,J,2), index(I), index(J), I>6.
:- place(I,J,3), index(I), index(J), J>6.

% Kiles can't be overlapped.
:- place(I,J,2), place(I+1,J,K), index(I), index(J), type(K).
:- place(I,J,2), place(I+2,J,K), index(I), index(J), type(K).
:- place(I,J,2), place(I+1,J-1,3), index(I), index(J).
:- place(I,J,2), place(I+2,J-1,3), index(I), index(J).
:- place(I,J,2), place(I+1,J-2,3), index(I), index(J).
:- place(I,J,2), place(I+2,J-2,3), index(I), index(J).
:- place(I,J,3), place(I,J+1,K), index(I), index(J), type(K).
:- place(I,J,3), place(I,J+2,K), index(I), index(J), type(K).
:- place(I,J,3), place(I-1,J+1,2), index(I), index(J).
:- place(I,J,3), place(I-1,J+2,2), index(I), index(J).
:- place(I,J,3), place(I-2,J+1,2), index(I), index(J).
:- place(I,J,3), place(I-2,J+2,2), index(I), index(J).


%h(I,J) :- place(I,J,2).
%v(I,J) :- place(I,J,3).

%#show h/2.
%#show v/2.

plc(I,J,2) :- place(I,J,2).
plc(I,J,3) :- place(I,J,3).

#show plc/3.



