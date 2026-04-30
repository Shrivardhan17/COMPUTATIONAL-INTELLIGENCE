likes(ravi, X) :- food(X).
food(chicken).
food(apple).
food(X) :- eats(X, Y), \+ killed(Y).
eats(peanut, ajay).
alive(ajay).
eats(X, rita) :- eats(X, ajay).
killed(X) :- \+ alive(X).
alive(X) :- \+ killed(X).

102 ?- likes(ravi,peanut).
true .

103 ?- likes(ravi,X).
X = chicken ;
X = apple ;
X = peanut ;
run :-
write('--- Calculator Menu ---'), nl,
write('1. ADD'), nl,
write('2. SUB'), nl,
write('3. MUL'), nl,
write('4. DIV'), nl,
write('5. MOD'), nl,
write('6. EXIT'), nl,
loop.

loop :-
nl,write('Enter choice (e.g. 1.): '),
read(Ch),
choice(Ch).

choice(1) :- do_calc('+').
choice(2) :- do_calc('-').
choice(3) :- do_calc('*').
choice(4) :- do_calc('/').
choice(5) :- do_calc('mod').
choice(6) :- write('Exit'),nl,halt.
choice(_) :- write('Invalid choice!'),nl,loop.

do_calc(Op) :-
write('Enter first number: '),read(A),
write('Enter second number: '),read(B),
calculate(Op,A,B,Res),
write('Result:'),nl,
write(A),write(Op),write(B),write('='),write(Res),nl,
loop.

calculate('+',A,B,Res) :- Res is A+B.
calculate('-',A,B,Res) :- Res is A-B.
calculate('*',A,B,Res) :- Res is A*B.
calculate('/',A,B,Res) :- B\==0 -> Res is A/B ; write('Error: Div by zero'),Res=0.
calculate('mod',A,B,Res) :- B\==0 -> Res is A mod B ; write('Error: Div by zero'),Res=0.
101 ?- consult(['z:/PROLOG/calc.pl']).
true.

102 ?- run.
--- Calculator Menu ---
1. ADD
2. SUB
3. MUL
4. DIV
5. MOD
6. EXIT

Enter choice (e.g. 1.): 1.
Enter first number: |: 1.
Enter second number: |: 2.
Result:
1+2=3

Enter choice (e.g. 1.): |: 2.
Enter first number: |: 2.
Enter second number: |: 1.
Result:
2-1=1

Enter choice (e.g. 1.): |: 3.
Enter first number: |: 3.
Enter second number: |: 2.
Result:
3*2=6

Enter choice (e.g. 1.): |: 4.
Enter first number: |: 4.
Enter second number: |: 2.
Result:
4/2=2

Enter choice (e.g. 1.): |: 4.
Enter first number: |: 4.
Enter second number: |: 0.
Error: Div by zeroResult:
4/0=0

Enter choice (e.g. 1.): |: 5.
Enter first number: |: 5.
Enter second number: |: 2.
Result:
5mod2=1

Enter choice (e.g. 1.): |:
male(motilal_nehru).
male(jawaharlal_nehru).
male(feroze_gandhi).
male(rajiv_gandhi).
male(sanjay_gandhi).
male(rahul_gandhi).
male(varun_gandhi).
male(robert_vadra).
male(raihan_vadra).

female(swarup_rani_nehru).
female(kamala_nehru).
female(indira_gandhi).
female(sonia_gandhi).
female(maneka_gandhi).
female(priyanka_gandhi).
female(miraya_vadra).

married(motilal_nehru, swarup_rani_nehru).
married(jawaharlal_nehru, kamala_nehru).
married(feroze_gandhi, indira_gandhi).
married(rajiv_gandhi, sonia_gandhi).
married(sanjay_gandhi, maneka_gandhi).
married(robert_vadra, priyanka_gandhi).

parent(motilal_nehru, jawaharlal_nehru).
parent(swarup_rani_nehru, jawaharlal_nehru).

parent(jawaharlal_nehru, indira_gandhi).
parent(kamala_nehru, indira_gandhi).

parent(indira_gandhi, rajiv_gandhi).
parent(feroze_gandhi, rajiv_gandhi).

parent(indira_gandhi, sanjay_gandhi).
parent(feroze_gandhi, sanjay_gandhi).

parent(rajiv_gandhi, rahul_gandhi).
parent(sonia_gandhi, rahul_gandhi).

parent(rajiv_gandhi, priyanka_gandhi).
parent(sonia_gandhi, priyanka_gandhi).

parent(sanjay_gandhi, varun_gandhi).
parent(maneka_gandhi, varun_gandhi).

parent(priyanka_gandhi, raihan_vadra).
parent(robert_vadra, raihan_vadra).

parent(priyanka_gandhi, miraya_vadra).
parent(robert_vadra, miraya_vadra).

spouse(X, Y) :- married(X, Y).
spouse(X, Y) :- married(Y, X).

father(F, C) :- parent(F, C), male(F).
mother(M, C) :- parent(M, C), female(M).

sibling(X, Y) :-
    parent(P, X),
    parent(P, Y),
    X \= Y.

brother(B, X) :- sibling(B, X), male(B).
sister(S, X) :- sibling(S, X), female(S).

uncle(U, C) :-
    parent(P, C),
    brother(U, P).

aunt(A, C) :-
    parent(P, C),
    sister(A, P).

grandparent(GP, C) :-
    parent(GP, P),
    parent(P, C).

grandfather(GF, C) :- grandparent(GF, C), male(GF).
grandmother(GM, C) :- grandparent(GM, C), female(GM).

nephew(X, Y) :-
    male(X),
    parent(P, X),
    sibling(P, Y).

niece(X, Y) :-
    female(X),
    parent(P, X),
    sibling(P, Y).

cousin(X, Y) :-
    parent(P1, X),
    parent(P2, Y),
    sibling(P1, P2),
    X \= Y.

wife(X, Y) :- spouse(X, Y), female(X).
husband(X, Y) :- spouse(X, Y), male(X).

son(X, Y) :- parent(Y, X), male(X).
daughter(X, Y) :- parent(Y, X), female(X).
child(X, Y) :- parent(Y, X).

relation(X, Y) :-
    father(X, Y), !,
    write(X), write(' is father of '), write(Y).

relation(X, Y) :-
    mother(X, Y), !,
    write(X), write(' is mother of '), write(Y).

relation(X, Y) :-
    brother(X, Y), !,
    write(X), write(' is brother of '), write(Y).

relation(X, Y) :-
    sister(X, Y), !,
    write(X), write(' is sister of '), write(Y).

relation(X, Y) :-
    husband(X, Y), !,
    write(X), write(' is husband of '), write(Y).

relation(X, Y) :-
    wife(X, Y), !,
    write(X), write(' is wife of '), write(Y).

relation(X, Y) :-
    son(X, Y), !,
    write(X), write(' is son of '), write(Y).

relation(X, Y) :-
    daughter(X, Y), !,
    write(X), write(' is daughter of '), write(Y).

relation(X, Y) :-
    uncle(X, Y), !,
    write(X), write(' is uncle of '), write(Y).

relation(X, Y) :-
    aunt(X, Y), !,
    write(X), write(' is aunt of '), write(Y).

relation(X, Y) :-
    grandfather(X, Y), !,
    write(X), write(' is grandfather of '), write(Y).

relation(X, Y) :-
    grandmother(X, Y), !,
    write(X), write(' is grandmother of '), write(Y).

relation(X, Y) :-
    cousin(X, Y), !,
    write(X), write(' is cousin of '), write(Y).

relation(X, Y) :-
    write('No direct relation found').

103 ?- grandfather(X,varun_gandhi).
X = feroze_gandhi .

104 ?- nephew(X,sanjay_gandhi).
X = rahul_gandhi .

105 ?- relation(indira_gandhi,priyanka).
No direct relation found
true.

106 ?- relation(indira_gandhi,priyanka_gandhi).
indira_gandhi is grandmother of priyanka_gandhi
true.

107 ?- wife(X,rajiv_gandhi).
X = sonia_gandhi.

108 ?- child(X,indira_gandhi).
X = rajiv_gandhi ;
X = sanjay_gandhi.

109 ?-

% ---------- BASIC OPERATIONS ----------

mymember(X, [X|_]).
mymember(X, [_|T]) :- mymember(X, T).

subset([], _).
subset([H|T], Set) :-
    mymember(H, Set),
    subset(T, Set).

union([], L, L).
union([H|T], L, R) :-
    mymember(H, L),
    union(T, L, R).
union([H|T], L, [H|R]) :-
    \+ mymember(H, L),
    union(T, L, R).

intersection([], _, []).
intersection([H|T], L, [H|R]) :-
    mymember(H, L),
    intersection(T, L, R).
intersection([H|T], L, R) :-
    \+ mymember(H, L),
    intersection(T, L, R).

difference([], _, []).
difference([H|T], L, R) :-
    mymember(H, L),
    difference(T, L, R).
difference([H|T], L, [H|R]) :-
    \+ mymember(H, L),
    difference(T, L, R).

equivalent(A, B) :-
    subset(A, B),
    subset(B, A).

% ---------- CARDINALITY ----------

cardinality([], 0).
cardinality([_|T], N) :-
    cardinality(T, N1),
    N is N1 + 1.

% ---------- MENU ----------

menu :-
    nl,
    write('----- SET OPERATIONS MENU -----'), nl,
    write('1. Member'), nl,
    write('2. Subset'), nl,
    write('3. Union'), nl,
    write('4. Intersection'), nl,
    write('5. Difference'), nl,
    write('6. Equivalent'), nl,
    write('7. Cardinality'), nl,
    write('8. Exit'), nl,
    loop.

% ---------- LOOP ----------

loop :-
    write('Enter your choice: '),
    read(Choice),
    process(Choice).

% ---------- PROCESS OPTIONS ----------

process(1) :-
    write('--- Member Check ---'), nl,
    write('Enter element: '), read(X),
    write('Enter list: '), read(L),
    (mymember(X, L) ->
        write('Element is a member')
    ;
        write('Element is NOT a member')
    ),
    nl, loop.

process(2) :-
    write('--- Subset Check ---'), nl,
    write('Enter subset list: '), read(A),
    write('Enter main list: '), read(B),
    (subset(A, B) ->
        write('It is a subset')
    ;
        write('Not a subset')
    ),
    nl, loop.

process(3) :-
    write('--- Union ---'), nl,
    write('Enter first list: '), read(A),
    write('Enter second list: '), read(B),
    union(A, B, R),
    write('Union = '), write(R), nl,
    loop.

process(4) :-
    write('--- Intersection ---'), nl,
    write('Enter first list: '), read(A),
    write('Enter second list: '), read(B),
    intersection(A, B, R),
    write('Intersection = '), write(R), nl,
    loop.

process(5) :-
    write('--- Difference ---'), nl,
    write('Enter first list: '), read(A),
    write('Enter second list: '), read(B),
    difference(A, B, R),
    write('Difference = '), write(R), nl,
    loop.

process(6) :-
    write('--- Equivalence Check ---'), nl,
    write('Enter first list: '), read(A),
    write('Enter second list: '), read(B),
    (equivalent(A, B) ->
        write('Sets are equivalent')
    ;
        write('Sets are NOT equivalent')
    ),
    nl, loop.

process(7) :-
    write('--- Cardinality ---'), nl,
    write('Enter list: '), read(L),
    cardinality(L, N),
    write('Cardinality = '), write(N), nl,
    loop.

process(8) :-
    write('Exiting program...'), nl.

process(_) :-
    write('Invalid choice! Try again.'), nl,
    loop.

----- SET OPERATIONS MENU -----
1. Member
2. Subset
3. Union
4. Intersection
5. Difference
6. Equivalent
7. Cardinality
8. Exit
Enter your choice: 1.
--- Member Check ---
Enter element: |: 2.
Enter lis]. |: [1,2,3
Element is a member
Enter your choice: |: 2.
--- Subset Check ---
Enter s].set list: |: [1,2
Enter main ].st: |: [1,2,3,4
It is a subset
Enter your choice: |: 3.
--- Union ---
Enter fir]. list: |: [1,2,3
Enter sec].d list: |: [3,4,5
Union = [1,2,3,4,5]
Enter your choice: |: 4.
--- Intersection ---
Enter first].ist: |: [1,4,5,6
Enter sec].d list: |: [1,4,5
Intersection = [1,4,5]
Enter your choice: |: 5.
--- Difference ---
Enter first].ist: |: [1,4,5,6
Enter sec].d list: |: [1,4,5
Difference = [6]
Enter your choice: |: 6.
--- Equivalence Check ---
Enter fir]. list: |: [1,2,3
Enter sec].d list: |: [1,2,3
Sets are equivalent
Enter your choice: |: 7.
--- Cardinality ---
Enter lis]. |: [1,4,5
Cardinality = 3
Enter your choice: |: 3.
--- Union ---
Enter first list: |:
[23bcs057@mepcolinux ex6]$exit
exit
