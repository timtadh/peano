
MAX = 100

class Type(object): pass
class Number(Type): pass
class Boolean(Type): pass
class NumericFunction(Number):
    def __init__(self, *inn):
        self.params = inn
class BooleanFunction(Boolean):
    def __init__(self, *inn):
        self.params = inn

class Value(object):
    def __init__(self, val, type):
        self.val  = val
        self.type = type
    def value(self, **objs):
        return self.val

class NumericValue(Value): pass
class BooleanValue(Value): pass
class NumericBinaryFunction(NumericValue):
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        super(NumericBinaryFunction, self).__init__(None, type)
class BooleanBinaryFunction(BooleanValue):
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        super(BooleanBinaryFunction, self).__init__(None, type)

class Constant(NumericValue):
    def __init__(self, val):
        assert val == 0
        super(Constant, self).__init__(val, Number())
    def __repr__(self):
        return repr(self.val)
    def __int__(self):
        return 0
    def value(self, **objs):
        return self

class S(NumericValue):
    def __init__(self, val):
        assert isinstance(val, NumericValue)
        super(S, self).__init__(val, NumericFunction(Number()))
    def __repr__(self):
        return 'S'+repr(self.val)
    def __int__(self):
        return 1+int(self.val)
    def value(self, **objs):
        return S(self.val.value(**objs))

class Variable(NumericValue):
    def __init__(self, name):
        assert isinstance(name, basestring)
        super(Variable, self).__init__(name, Number())
    def __repr__(self):
        return '<%s>' % self.val
    def value(self, **objs):
        return objs[self.val]

class Add(NumericBinaryFunction):
    def __init__(self, x, y):
        assert isinstance(x, NumericValue)
        assert isinstance(y, NumericValue)
        super(Add, self).__init__(x, y, NumericFunction(Number(),Number()))
    def __repr__(self):
        return '(add, %s, %s)' % (repr(self.x), repr(self.y))
    def value(self, **objs):
        r = Constant(0)
        x = self.x.value(**objs)
        y = self.y.value(**objs)
        while isinstance(x, S):
            r = S(r)
            x = x.val
        while isinstance(y, S):
            r = S(r)
            y = y.val
        return r

class Mul(NumericBinaryFunction):
    def __init__(self, x, y):
        assert isinstance(x, NumericValue)
        assert isinstance(y, NumericValue)
        super(Mul, self).__init__(x, y, NumericFunction(Number(),Number()))
    def __repr__(self):
        return '(mul, %s, %s)' % (repr(self.x), repr(self.y))
    def value(self, **objs):
        r = Constant(0)
        x = self.x.value(**objs)
        y = self.y.value(**objs)
        while isinstance(y, S):
            r = Add(r, x).value()
            y = y.val
        return r

class Exp(NumericBinaryFunction):
    def __init__(self, x, y):
        assert isinstance(x, NumericValue)
        assert isinstance(y, NumericValue)
        super(Exp, self).__init__(x, y, NumericFunction(Number(),Number()))
    def __repr__(self):
        return '(exp, %s, %s)' % (repr(self.x), repr(self.y))
    def value(self, **objs):
        r = S(Constant(0))
        x = self.x.value(**objs)
        y = self.y.value(**objs)
        while isinstance(y, S):
            r = Mul(r, x).value()
            y = y.val
        return r

class Equal(BooleanBinaryFunction):
    def __init__(self, x, y):
        assert isinstance(x, NumericValue)
        assert isinstance(y, NumericValue)
        super(Equal, self).__init__(x, y, BooleanFunction(Number(), Number()))
    def __repr__(self):
        return '(equal, %s, %s)' % (repr(self.x), repr(self.y))
    def value(self, **objs):
        x = self.x.value(**objs)
        y = self.y.value(**objs)
        while isinstance(x, S) and isinstance(y, S):
            x = x.val
            y = y.val
        if (not isinstance(x, S)) and (not isinstance(y, S)):
            if isinstance(x, Constant) and isinstance(y, Constant):
                return x.val == y.val
            elif isinstance(x, Variable) and isinstance(y, Variable):
                return x.val == y.val
        return False

class Not(BooleanValue):
    def __init__(self, val):
        assert isinstance(val, BooleanValue)
        super(Not, self).__init__(val, Boolean())
    def __repr__(self):
        return '(not, %s)' % (repr(self.val))
    def value(self, **objs):
        return not self.val.value(**objs)

class And(BooleanBinaryFunction):
    def __init__(self, x, y):
        assert isinstance(x, BooleanValue)
        assert isinstance(y, BooleanValue)
        super(And, self).__init__(x, y, BooleanFunction(Boolean(), Boolean()))
    def __repr__(self):
        return '(and, %s, %s)' % (repr(self.x), repr(self.y))
    def value(self, **objs):
        return self.x.value(**objs) and self.y.value(**objs)

class Or(BooleanBinaryFunction):
    def __init__(self, x, y):
        assert isinstance(x, BooleanValue)
        assert isinstance(y, BooleanValue)
        super(Or, self).__init__(x, y, BooleanFunction(Boolean(), Boolean()))
    def __repr__(self):
        return '(or, %s, %s)' % (repr(self.x), repr(self.y))
    def value(self, **objs):
        return self.x.value(**objs) or self.y.value(**objs)

class Implies(BooleanBinaryFunction):
    def __init__(self, x, y):
        assert isinstance(x, BooleanValue)
        assert isinstance(y, BooleanValue)
        super(Implies, self).__init__(x, y, BooleanFunction(Boolean(), Boolean()))
    def __repr__(self):
        return '(implies, %s, %s)' % (repr(self.x), repr(self.y))
    def value(self, **objs):
        return (not self.x.value(**objs)) or self.y.value(**objs)

class ForAll(BooleanValue):
    def __init__(self, var, formula):
        assert isinstance(var, basestring)
        assert isinstance(formula, BooleanValue)
        self.var = var
        self.formula = formula
        super(ForAll, self).__init__(None, BooleanFunction(Boolean()))
    def __repr__(self):
        return '(for all, %s, %s)' % (repr(self.var), repr(self.formula))
    def value(self, **objs):
        cur = Constant(0)
        for x in xrange(0, MAX):
            if not self.formula.value(**{self.var:cur}): return False
            cur = S(cur)
        return True

class ForSome(BooleanValue):
    def __init__(self, var, formula):
        assert isinstance(var, basestring)
        assert isinstance(formula, BooleanValue)
        self.var = var
        self.formula = formula
        super(ForSome, self).__init__(None, BooleanFunction(Boolean()))
    def __repr__(self):
        return '(for some, %s, %s)' % (repr(self.var), repr(self.formula))
    def value(self, **objs):
        cur = Constant(0)
        for x in xrange(0, MAX):
            if self.formula.value(**{self.var:cur}): return True
            cur = S(cur)
        return False
