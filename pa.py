

class Number(object):
    
    def __init__(self, value):
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
        return repr(self.value)

    def __int__(self):
        return int(self.value)
    
    def __str__(self):
        return str(int(self))


class Boolean(object):
    
    def __init__(self, value):
        self.value = Boolean.coerce(value)
    
    @classmethod
    def coerce(cls, value):
        if hasattr(value, 'value'):
            value = Boolean.coerce(value.value)
        assert value == True or value == False
        return value


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
        self.x = Boolean.coerce(x)
    @property
    def value(self):
        return not self.x        


class Equal(object):

    def __init__(self, x, y):
        self.x = Number.coerce(x)
        self.y = Number.coerce(y)
    @property
    def value(self):
        return self.x == self.y

