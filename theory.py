from pa import *
import sys
sys.setrecursionlimit(10000)

Z = Constant(0)

x = Variable('x')
y = Variable('y')
z = Variable('z')
has_pred = ForAll(x, Or(Equal(x, Z), ForSome(y, Equal(x, S(y)))))
print has_pred.value(), has_pred

r = Variable('r')
lt = Abbrv(ForSome(r, And(Not(Equal(r, Z)), Equal(Add(r, x), y)))) ## x < y
le = Abbrv(Or(Equal(x, y), lt()))
print lt()

gt_one = Abbrv(LessThan(S(Z), y))

print
print gt_one(y=x)
print gt_one(y=x).value(x=N(3))

prime = Abbrv(
    And(gt_one(y=x),
        Not(
            ForSome(y,
                ForSome(z,
                    And(
                        Equal(x, Mul(y, z)),
                        And(
                            gt_one(y=y),
                            gt_one(y=z)
                        )
                    )
                )
            )
        )
    )
)
print
print prime()
print
for x in xrange(0, MAX):
    print x, prime(x=N(x)).value()