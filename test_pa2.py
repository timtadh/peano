from pa2 import *

def test_Print():
    zero = Constant(0)
    five = S(S(S(S(S(zero)))))
    assert int(five) == 5
    assert repr(five) == 'SSSSS0'
    assert repr(Not(Equal(zero, five))) == '(not, (equal, 0, SSSSS0))'
    assert repr(Not(Not(Equal(zero, five)))) == '(not, (not, (equal, 0, SSSSS0)))'

def test_S():
    zero = Variable('x')
    one = S(zero)
    two = S(S(zero))
    five = S(S(S(S(S(zero)))))
    assert repr(zero) == '<x>'
    assert repr(one) == 'S<x>'
    assert repr(two) == 'SS<x>'
    assert repr(five.value(x=five.value(x=Constant(0)))) == 'SSSSSSSSSS0'

def test_Equal():
    zero_x = Variable('x')
    one_x = S(zero_x)
    two_x = S(S(zero_x))
    zero_0 = Constant(0)
    one_0 = S(zero_0)
    two_0 = S(S(zero_0))
    assert Equal(one_x, two_x).value(x=Constant(0)) == False
    assert Equal(two_x, two_x).value(x=Constant(0)) == True
    assert Equal(two_0, two_x).value(x=two_0) == False
    assert Equal(two_0, two_0).value(x=Constant(0)) == True

def test_Not():
    zero = Constant(0)
    one = S(zero)
    two = S(S(zero))
    assert Not(Equal(one, two)).value() == True
    assert Not(Equal(two, two)).value() == False
    assert Not(Equal(two, one)).value() == True
    assert Not(Equal(one, one)).value() == False

def test_And():
    zero = Constant(0)
    one = S(zero)
    two = S(S(zero))
    true = Equal(one, one)
    false = Equal(one, two)
    assert And(true, true).value() == True
    assert And(true, false).value() == False
    assert And(false, true).value() == False
    assert And(false, false).value() == False

def test_Or():
    zero = Constant(0)
    one = S(zero)
    two = S(S(zero))
    true = Equal(one, one)
    false = Equal(one, two)
    assert Or(true, true).value() == True
    assert Or(true, false).value() == True
    assert Or(false, true).value() == True
    assert Or(false, false).value() == False

def test_Implies():
    zero = Constant(0)
    one = S(zero)
    two = S(S(zero))
    true = Equal(one, one)
    false = Equal(one, two)
    assert Implies(true, true).value() == True
    assert Implies(true, false).value() == False
    assert Implies(false, true).value() == True
    assert Implies(false, false).value() == True

def test_ForAll():
    zero = Constant(0)
    x = Variable('x')
    assert ForAll('x', Or(Not(Equal(zero, x)), Equal(x, x))).value() == True
    assert ForAll('x', Equal(Constant(0), Variable('x'))).value() == False

def test_ForSome():
    assert ForSome('x', Equal(Constant(0), Variable('x'))).value() == True
