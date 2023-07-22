in(XP,XR,0) :- in0(XP,XR).
in(XP,XR,XT+1) :- goto(XP,XR,XT).
go(XP,XT) :- goto(XP,XR,XT).
in(XP,XR,XT+1) :- in(XP,XR,XT), not go(XP,XT), XT = 0..h-1.
:- in(XP,XR1,XT), in(XP,XR2,XT), XR1 != XR2.
in_building(XP,XT) :- in(XP,XR,XT).
:- not in_building(XP,XT), person(XP), XT = 0..h.
