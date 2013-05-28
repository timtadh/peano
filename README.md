Peano Arithmetic
================

Peano Arithmetic is a small set of axioms which recursively define most of the truths of arithmetic.
They cannot define all of the truths due to Gödel's Incompleteness Theorem, which states no
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

### Deciding all questions.

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

The Language
============

Constants

    0

Functions

    The Unary Function
      S(x)   abbr Sx
        semantically it interpreted as +1 or successor
      Not(x) abbr !x

    The Binary Functions
      Add(x, y)     abbr x + y
      Mul(x, y)     abbr x * y
      Exp(x, y)     abbr x^y
      Implies(x, y) abbr x --> y
      And(x, y)     abbr x & y
      Or(x, y)      abbr x | y

Relations

    Equal(x, y)    abbrv x = y
    NotEqual(x, y) abbrv x != y

The Peano Axioms
================

    PA 1 - Sx != 0
    PA 2 - Sx = Sy --> x = y
    PA 3 - x + 0 = x
    PA 4 - x + Sy = S(x + y)
    PA 5 - x * 0 = 0
    PA 6 - x * Sy = (x * y) + x
    PA 7 - x^0 = S0
    PA 8 - x^Sy = x^y * x

Now for the Rest:

    For any formula F with free variable x there is a formula:
        (F(0) & ForAll{x}[F(x) --> F(Sx)]) --> ForAll{x}[F(x)]

Status
======

You can define and evaluate PA in a limited way. Unquantified PA works fine, but quantifiers cause
some issues. This is to be expected as they are saying very general things and a computer can really
only say specific things. There may be more clever ways to implement quantifiers but for now they
are slow, and only marginally useful. However, we can still encode interesting things like:

    prime = Abbrv(
        And(
            LessThan(S(0), x),
            Not(
                ForSome(b,
                    ForSome(c,
                        And(
                            Equal(x, Mul(b, c)),
                            And(
                                LessThan(S(0), b),
                                LessThan(S(0), c)
                            )
                        )
                    )
                )
            )
        )
    )

Just note that formulas such as this one may take a very, very long time to evaluate in the general
case.

The "Peano on Python" one day experiment was a success, but not a particularly useful one. It was
however very educational and helped me understand the Incompleteness Theorem more fully.

