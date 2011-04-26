Peano Arithmetic
================

Peano Arithmetic is a small set of axioms which recursively define most of the truths of arithmetic.
They cannot define all of the truths do to G\:{o}del's Incompleteness Theorem, which states no
recursively axiomatized theory can settle all questions.

### To a settle a question.

To define what does it mean to settle a particular question. We first need to understand exactly
what a question is. This is a example question:

    :- 0 = s0
    or in more common notation
    :- 0 = 1

Clearly we would like any axoim system to settle this in the negative. That is we would like this
statement to be decided in the negative. To "decide" a question means to know whether or not it is
derivable. If it is derivable then it "true" and if it not derivable then it is false.

### Deciding all questions

For a theory to be complete it must be proven that it can decide all questions. That doesn't mean we
will have a computerized routine to decide any particular question (for instance 0 = s0) but we have
the assurance that indeed it can be decided. Unfortunately, Kurt G\:{o}del showed us the previous
century that if we finitely axiomitize our theory (that is only write down a finite set of
potentially recursive axoims) we will never decide all questions. 

Although Peano Arithmetic cannot decide all questions it can decide almost every interesting
question you might have. For instance it can decide whether a particular sentence is a theorem of
Peano Arithmetic. 

Purpose of this Repository
==========================

I am writing an evaluator for Peano Arithmetic to help me better understand the proof of the
Incompleteness theorem. In part I am doing this to prepare for an exam. However, on another level it
is just an interesting thing to do. The practical value is zero, but the educational value I hope to
be enormous.



