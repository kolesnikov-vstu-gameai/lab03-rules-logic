% База знаний стражника (SWI-Prolog). Факты добавляются из игры через assertz/1.
:- dynamic sees/2, hears/2, alarm/0, state/2.

state(g1, patrol).
state(g2, patrol).

next_state(G, chase)       :- sees(G, player).
next_state(G, investigate) :- hears(G, noise), state(G, patrol), \+ sees(G, player).
next_state(G, search)      :- alarm, state(G, patrol), \+ sees(G, player).
next_state(G, S)           :- state(G, S), \+ sees(G, player), \+ hears(G, noise), \+ alarm.

raise_alarm :- sees(_, player), \+ alarm, assertz(alarm).
