from pa import *

Z = Constant(0)

x = Variable('x')
y = Variable('y')
has_pred = ForAll(x, Or(Equal(x, Z), ForSome(y, Equal(x, S(y)))))
print has_pred.value(), has_pred
