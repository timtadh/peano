from pa import *
import sys
sys.setrecursionlimit(10000)

Z = Constant(0)

a = Variable('a')
b = Variable('b')
c = Variable('c')
d = Variable('d')
e = Variable('e')
f = Variable('f')
g = Variable('g')
p = Variable('p')
q = Variable('q')
x = Variable('x')
y = Variable('y')
z = Variable('z')
has_pred = ForAll(x, Or(Equal(x, Z), ForSome(y, Equal(x, S(y)))))
print has_pred.value(), has_pred

r = Variable('r')
lt = Abbrv(ForSome(r, And(Not(Equal(r, Z)), Equal(Add(r, x), y)))) ## x < y
le = Abbrv(Or(Equal(x, y), lt()))
print lt()

gt_one = Abbrv(LessThan(S(Z), a))

print
print gt_one(a=x)
print gt_one(a=x).value(x=N(3))
print
print

prime = Abbrv(
    And(gt_one(a=x),
        Not(
            ForSome(b,
                ForSome(c,
                    And(
                        Equal(x, Mul(b, c)),
                        And(
                            gt_one(a=b),
                            gt_one(a=c)
                        )
                    )
                )
            )
        )
    )
)

#print prime(x=N(5)).replace(prime(x=N(5)))

nextprime = Abbrv(
    And(
        And(prime(), prime(x=y)),
        And(
            LessThan(x, y),
            ForAll(z,
                Implies(
                    prime(x=z),
                    Or(
                        Or(Equal(z, x), LessThan(z, x)),
                        Or(Equal(y, z), LessThan(y, z))
                    )
                )
            )
        )
    )
)

#print nextprime()
#print nextprime().value(x=N(13), y=N(17))

seq = Abbrv(
    And(
        LessThan(S(Z), c),
        ForAll(q,
            ForAll(p,
                Implies(
                    And(
                        And(prime(x=p), prime(x=q)),
                        And(
                            LessThan(p, q),
                            Divides(q, c)
                        )
                    ),
                    Divides(p, c)
                )
            )
        )
    )
)

#print seq()
#for x in xrange(0, 10):
    #print x, seq().value(c=N(x))


products = Abbrv(
    And(
        And(
            And(Divides(N(2),d), Not(Divides(N(4),d))),
            seq(c=d),
        ),
        ForAll(e,
            ForAll(f,
                ForAll(g,
                    Implies(
                        And(nextprime(x=f, y=g), Divides(g, d)),
                        Bijection(
                            Divides(Exp(f, e), d),
                            Divides(Exp(g, S(e)), d),
                        ),
                    )
                )
            )
        )
    )
)

print products()
for x in xrange(0, MAX):
    print x, products().value(d=N(x))


