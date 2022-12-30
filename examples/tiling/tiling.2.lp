index(1..8).
type(1..3).

% XT = 1: a 1x1 tile.
% XT = 2: a horizontal 3x1 tile which the leftmost tile is at (X,Y).
% XT = 3: a vertical 3x1 tile which the topmost tile is at (X,Y).

% We can place at most one type of tile at one location.
% Anthem: language feature not yet supported (aggregates with guards)
%{place(X,Y,XT) : type(XT)} 1 :- index(X), index(Y).

% replace with:
{place(X,Y,XT) : type(XT)} :- index(X), index(Y).
:- place(X,Y,XT1), place(X,Y,XT2), index(X), index(Y), type(XT1), type(XT2), XT1 != XT2.

% We should use exactly one 1x1 tile.
% Anthem: language feature not yet supported (aggregates with guards)
%:- 2 {place(X,Y,1) : index(X), index(Y)}.
%:- {place(X,Y,1) : index(X), index(Y)} 0.

% replace with:
:- place(X1,Y1,1), place(X2,Y2,1), X1 != X2.
:- place(X1,Y1,1), place(X2,Y2,1), Y1 != Y2.


% filled(X,Y) means (X,Y) is covered by one of the tiles.
filled(X,Y) :- place(X,Y,1), index(X), index(Y).
filled(X,Y) :- place(X,Y,2), index(X), index(Y).
filled(X+1,Y) :- place(X,Y,2), index(X), index(Y).
filled(X+2,Y) :- place(X,Y,2), index(X), index(Y).
filled(X,Y) :- place(X,Y,3), index(X), index(Y).
filled(X,Y+1) :- place(X,Y,3), index(X), index(Y).
filled(X,Y+2) :- place(X,Y,3), index(X), index(Y).

% The chessboard should be covered.
:- not filled(X,Y), index(X), index(Y).

% The tile should be in the chessboard.
:- place(X,Y,2), index(X), index(Y), X>6.
:- place(X,Y,3), index(X), index(Y), Y>6.

% Tiles can't be overlapped.
:- place(X,Y,2), place(X+1,Y,T), index(X), index(Y), type(T).
:- place(X,Y,2), place(X+2,Y,T), index(X), index(Y), type(T).
:- place(X,Y,2), place(X+1,Y-1,3), index(X), index(Y).
:- place(X,Y,2), place(X+2,Y-1,3), index(X), index(Y).
:- place(X,Y,2), place(X+1,Y-2,3), index(X), index(Y).
:- place(X,Y,2), place(X+2,Y-2,3), index(X), index(Y).
:- place(X,Y,3), place(X,Y+1,T), index(X), index(Y), type(T).
:- place(X,Y,3), place(X,Y+2,T), index(X), index(Y), type(T).
:- place(X,Y,3), place(X-1,Y+1,2), index(X), index(Y).
:- place(X,Y,3), place(X-1,Y+2,2), index(X), index(Y).
:- place(X,Y,3), place(X-2,Y+1,2), index(X), index(Y).
:- place(X,Y,3), place(X-2,Y+2,2), index(X), index(Y).


%h(X,Y) :- place(X,Y,2).
%v(X,Y) :- place(X,Y,3).

%#show h/2.
%#show v/2.

plc(X,Y,2) :- place(X,Y,2).
plc(X,Y,3) :- place(X,Y,3).

#show plc/3.



