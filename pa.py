
MAX = 8

class Type(object): pass
class Number(Type): pass
class Boolean(Type): pass
class NumericFunction(Number):
    def __init__(self, *inn):
        self.params = inn
class BooleanFunction(Boolean):
    def __init__(self, *inn):
        self.params = inn


class TypedObject(object):
    def __init__(self, type):
        self.type = type

class Value(TypedObject):
    def __init__(self, val, type):
        self.val  = val
        super(Value, self).__init__(type)
    def value(self, **objs):
        return self.val

class NumericValue(Value): pass
class BooleanValue(Value): pass
class SubValue(NumericValue, BooleanValue): pass

class BinaryFunction(TypedObject):
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        TypedObject.__init__(self, type)
        #super(BinaryFunction, self).__init__(type)

class NumericBinaryFunction(BinaryFunction, NumericValue):
    def __init__(self, x, y, type):
        super(NumericBinaryFunction, self).__init__(x,y,type)
class BooleanBinaryFunction(BinaryFunction, BooleanValue):
    def __init__(self, x, y, type):
        super(BooleanBinaryFunction, self).__init__(x,y,type)

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
    def __str__(self):
        return 'S'+str(self.val)
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
    def __str__(self):
        return self.val
    def value(self, **objs):
        return objs[self.val]

class Add(NumericBinaryFunction):
    def __init__(self, x, y):
        assert isinstance(x, NumericValue)
        assert isinstance(y, NumericValue)
        super(Add, self).__init__(x, y, NumericFunction(Number(),Number()))
    def __repr__(self):
        return '(add, %s, %s)' % (repr(self.x), repr(self.y))
    def __str__(self):
        return '(%s + %s)' % (str(self.x), str(self.y))
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
    def __str__(self):
        return '(%s * %s)' % (str(self.x), str(self.y))
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
    def __str__(self):
        return '(%s^%s)' % (str(self.x), str(self.y))
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
    def __str__(self):
        return '(%s = %s)' % (str(self.x), str(self.y))
    def value(self, **objs):
        #print self.x, self.y
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


class Divides(BooleanBinaryFunction):
    def __init__(self, x, y):
        assert isinstance(x, NumericValue)
        assert isinstance(y, NumericValue)
        super(Divides, self).__init__(x, y, BooleanFunction(Number(), Number()))
    def __repr__(self):
        return '(divies, %s, %s)' % (repr(self.x), repr(self.y))
    def __str__(self):
        return '(%s|%s)' % (str(self.x), str(self.y))
    def value(self, **objs):
        #print self.x, self.y
        x = self.x.value(**objs)
        X = 0
        y = self.y.value(**objs)
        Y = 0
        while isinstance(x, S):
            X += 1
            x = x.val
        while isinstance(y, S):
            Y += 1
            y = y.val
        return Y%X == 0

class LessThan(BooleanBinaryFunction):
    def __init__(self, x, y):
        assert isinstance(x, NumericValue)
        assert isinstance(y, NumericValue)
        super(LessThan, self).__init__(x, y, BooleanFunction(Number(), Number()))
    def __repr__(self):
        return '(less than, %s, %s)' % (repr(self.x), repr(self.y))
    def __str__(self):
        return '(%s < %s)' % (str(self.x), str(self.y))
    def value(self, **objs):
        #print self.x, self.y
        x = self.x.value(**objs)
        y = self.y.value(**objs)
        while isinstance(x, S) and isinstance(y, S):
            x = x.val
            y = y.val
        if (not isinstance(x, S)) and (isinstance(y, S)):
            if isinstance(x, Constant):
                return True
        return False

class Not(BooleanValue):
    def __init__(self, val):
        assert isinstance(val, BooleanValue)
        super(Not, self).__init__(val, Boolean())
    def __repr__(self):
        return '(not, %s)' % (repr(self.val))
    def __str__(self):
        return '!%s'  % (str(self.val))
    def value(self, **objs):
        return not self.val.value(**objs)

class And(BooleanBinaryFunction):
    def __init__(self, x, y):
        assert isinstance(x, BooleanValue)
        assert isinstance(y, BooleanValue)
        super(And, self).__init__(x, y, BooleanFunction(Boolean(), Boolean()))
    def __repr__(self):
        return '(and, %s, %s)' % (repr(self.x), repr(self.y))
    def __str__(self):
        return '(%s and %s)' % (str(self.x), str(self.y))
    def value(self, **objs):
        return self.x.value(**objs) and self.y.value(**objs)

class Or(BooleanBinaryFunction):
    def __init__(self, x, y):
        assert isinstance(x, BooleanValue)
        assert isinstance(y, BooleanValue)
        super(Or, self).__init__(x, y, BooleanFunction(Boolean(), Boolean()))
    def __repr__(self):
        return '(or, %s, %s)' % (repr(self.x), repr(self.y))
    def __str__(self):
        return '(%s or %s)' % (str(self.x), str(self.y))
    def value(self, **objs):
        return self.x.value(**objs) or self.y.value(**objs)

class Implies(BooleanBinaryFunction):
    def __init__(self, x, y):
        assert isinstance(x, BooleanValue)
        assert isinstance(y, BooleanValue)
        super(Implies, self).__init__(x, y, BooleanFunction(Boolean(), Boolean()))
    def __repr__(self):
        return '(implies, %s, %s)' % (repr(self.x), repr(self.y))
    def __str__(self):
        return '(%s --> %s)' % (str(self.x), str(self.y))
    def value(self, **objs):
        x = self.x.value(**objs)
        y = "don't care"
        if x == True: y = self.y.value(**objs)
        #print '------ implies ------'
        #print objs
        #print 'X', x
        #print 'Y', y
        #print (not x) or y
        #print '------ implies ------'
        return (not x) or y

class Bijection(BooleanBinaryFunction):
    def __init__(self, x, y):
        assert isinstance(x, BooleanValue)
        assert isinstance(y, BooleanValue)
        super(Bijection, self).__init__(x, y, BooleanFunction(Boolean(), Boolean()))
    def __repr__(self):
        return '(bijection, %s, %s)' % (repr(self.x), repr(self.y))
    def __str__(self):
        return '(%s <--> %s)' % (str(self.x), str(self.y))
    def value(self, **objs):
        x = self.x.value(**objs)
        y = self.y.value(**objs)
        return (x and y) or ((not x) and (not y))

class ForAll(BooleanBinaryFunction):
    def __init__(self, var, formula):
        assert isinstance(var, Variable)
        assert isinstance(formula, BooleanValue)
        super(ForAll, self).__init__(var, formula, BooleanFunction(Boolean()))
    def __repr__(self):
        return '(for all, %s, %s)' % (repr(self.x), repr(self.y))
    def __str__(self):
        return '[All{%s} %s]' % (str(self.x), str(self.y))
    def value(self, **objs):
        var = self.x
        formula = self.y
        cur = Constant(0)
        for x in xrange(0, MAX):
            cobjs = dict(objs)
            cobjs.update({var.val:cur})
            if not formula.value(**cobjs): return False
            cur = S(cur)
        return True

class ForSome(BooleanBinaryFunction):
    def __init__(self, var, formula):
        assert isinstance(var, Variable)
        assert isinstance(formula, BooleanValue)
        super(ForSome, self).__init__(var, formula, BooleanFunction(Boolean()))
    def __repr__(self):
        return '(for some, %s, %s)' % (repr(self.x), repr(self.y))
    def __str__(self):
        return '[Some{%s} %s]' % (str(self.x), str(self.y))
    def value(self, **objs):
        var = self.x
        formula = self.y
        cur = Constant(0)
        for x in xrange(0, MAX):
            cobjs = dict(objs)
            cobjs.update({var.val:cur})
            if formula.value(**cobjs): return True
            cur = S(cur)
        return False

class Sub(SubValue):
    def __init__(self, x, y, formula):
        assert isinstance(x, Variable)
        assert isinstance(y, Value)
        assert isinstance(formula, Value)
        self.x = x
        self.y = y
        self.formula = formula
        super(Sub, self).__init__(None, Type)
    def __repr__(self):
        return '(sub, %s, %s, %s)' % (repr(self.x), repr(self.y), repr(self.formula))
    def __str__(self):
        return '{%s}(%s/%s)' % (str(self.formula), str(self.x), str(self.y))

    def replace(self, f):
        if isinstance(f, Constant): return f
        if isinstance(f, Variable):
            #print repr(f), repr(self.x)
            if f.val == self.x.val:
                #print repr(f), '<-->', repr(self.y)
                return self.y
            #print f.__class__, f
            return f
        elif isinstance(f, BinaryFunction):
            f = f.__class__(self.replace(f.x), self.replace(f.y))
            #print f.__class__, f
            return f
        elif isinstance(f, SubValue):
            #print 'a new', f
            f = f.replace(f.formula)
            #print 'got it', f
            f = self.replace(f)
            #print f.__class__, f
            #print
            return f
        elif isinstance(f, Value):
            #print f.__class__
            f = f.__class__(self.replace(f.val))
            #print f.__class__, f
            #print
            return f
        raise Exception, f.__class__


    def value(self, **objs):
        #print '<-------', self
        f = self.replace(self.formula)
        #print '------->', f
        r = f.value(**objs)
        #print 'val', r
        return r

def Abbrv(formula):
    def abbrv(**subs):
        f = formula
        for k, v in subs.iteritems():
            f = Sub(Variable(k), v, f)
        return f
    return abbrv

def N(n):
    #assert n < MAX
    cur = Constant(0)
    for x in xrange(0, n):
        cur = S(cur)
    return cur
