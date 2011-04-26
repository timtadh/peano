

class Number(object):
    
    def __init__(self, value):
        self.o = value
        self.value = Number.coerce(value)
    
    @classmethod
    def coerce(cls, value):
        if hasattr(value, 'value'):
            return Number.coerce(value.value)
        assert value == 0 or isinstance(value, S)
        return value

    def __eq__(self, b):
        b = Number(b)
        if isinstance(b, S):
            return b.__eq__(self)
        return self.value == b.value

    def __ne__(self, b):
        return not self == b

    def __repr__(self):
        return repr(self.o)

    def __int__(self):
        return int(self.value)
    
    def __str__(self):
        return str(int(self))


class Boolean(object):
    
    def __init__(self, value):
        self.o = value
        self.value = Boolean.coerce(value)
    
    @classmethod
    def coerce(cls, value):
        if hasattr(value, 'value'):
            value = Boolean.coerce(value.value)
        assert value == True or value == False
        return value

    def __repr__(self):
        return repr(self.o)


class S(object):

    def __init__(self, x):
        self.x = Number(x)
    def __eq__(self, b):
        if b == None: return False
        if isinstance(b, S):
            return self.x == b.x
        return False
    def __ne__(self, b):
        return not self == b
    def __repr__(self):
        return 'S'+repr(self.x)
    def __int__(self):
        return 1+int(self.x)
    def __str__(self):
        return str(int(self))

class Not(object):

    def __init__(self, x):
        self.x = Boolean(x)
    @property
    def value(self):
        return not self.x.value

    def __repr__(self):
        return "(not, %s)" % repr(self.x.o)


class Equal(object):

    def __init__(self, x, y):
        self.x = Number(x)
        self.y = Number(y)
    @property
    def value(self):
        return self.x == self.y

    def __repr__(self):
        return "(equal, %s, %s)" % (repr(self.x), repr(self.y))

class And(object):

    def __init__(self, x, y):
        self.x = Boolean(x)
        self.y = Boolean(y)
    
    @property
    def value(self):
        return self.x.value and self.y.value

    def __repr__(self):
        return '(and, %s, %s)' % (repr(self.x), repr(self.y))


class Or(object):

    def __init__(self, x, y):
        self.x = Boolean(x)
        self.y = Boolean(y)
    
    @property
    def value(self):
        return self.x.value or self.y.value

    def __repr__(self):
        return '(or, %s, %s)' % (repr(self.x), repr(self.y))


class Implies(object):

    def __init__(self, x, y):
        self.x = Boolean(x)
        self.y = Boolean(y)
    
    @property
    def value(self):
        return (not self.x.value) or self.y.value

    def __repr__(self):
        return '(implies, %s, %s)' % (repr(self.x), repr(self.y))

class Add(object):
    
    def __init__(self, x, y):
        self.x = Number(x)
        self.y = Number(y)

    @property
    def value(self):
        x = self.x.value
        y = self.y.value
        while isinstance(y, S):
            x = S(x)
            y = y.x.value
        return x
    
    def __repr__(self):
        return '(add, %s, %s)' % (repr(self.x), repr(self.y))

