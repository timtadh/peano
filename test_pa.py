from pa import *

def test_S():
    zero = 0
    one = S(zero)
    two = S(S(zero))
    five = S(S(S(S(S(zero)))))
    assert one == S(0)
    assert two == S(S(0))
    assert five == S(S(S(S(S(0)))))
    assert five != S(0)

def test_Equal():
    zero = 0
    one = S(zero)
    two = S(S(zero))

    print Equal(one, two).value
    assert Equal(one, two).value == False
    assert Equal(one, two.x).value == True

def test_Not():
    zero = Number(0)
    one = S(zero)

    assert Not(Equal(one, zero)).value
    assert Not(Equal(one, one)).value == False
    assert Not(False)

def test_PrintNumber():
    zero = Number(0)
    five = S(S(S(S(S(zero)))))
    assert int(five) == 5
    assert repr(five) == 'SSSSS0'
    assert str(five) == '5'

    assert repr(Not(Equal(zero, five))) == '(not, (equal, 0, SSSSS0))'
    assert repr(Not(Not(Equal(zero, five)))) == '(not, (not, (equal, 0, SSSSS0)))'
    assert repr(And(Not(Equal(zero, five)), Equal(zero, zero))) == (
      '(and, (not, (equal, 0, SSSSS0)), (equal, 0, 0))'
    )
    assert repr(Or(Not(Equal(zero, five)), Equal(zero, zero))) == (
      '(or, (not, (equal, 0, SSSSS0)), (equal, 0, 0))'
    )
    assert repr(Implies(Not(Equal(zero, five)), Equal(zero, zero))) == (
      '(implies, (not, (equal, 0, SSSSS0)), (equal, 0, 0))'
    )

def test_And():
    zero = Number(0)
    one = S(zero)

    assert And(Not(Equal(one, zero)), Equal(zero, zero)).value == True
    assert And(Equal(one, zero), Equal(zero, zero)).value == False
    assert And(Equal(one, one), Equal(one, zero)).value == False
    assert And(Equal(one, zero), Equal(one, zero)).value == False

def test_Or():
    zero = Number(0)
    one = S(zero)

    assert Or(Not(Equal(one, zero)), Equal(zero, zero)).value == True
    assert Or(Equal(one, zero), Equal(zero, zero)).value == True
    assert Or(Equal(one, one), Equal(one, zero)).value == True
    assert Or(Equal(one, zero), Equal(one, zero)).value == False

def test_Implies():
    zero = Number(0)
    one = S(zero)

    assert Implies(Not(Equal(one, zero)), Equal(zero, zero)).value == True
    assert Implies(Equal(one, zero), Equal(zero, zero)).value == True
    assert Implies(Equal(one, one), Equal(one, zero)).value == False
    assert Implies(Equal(one, zero), Equal(one, zero)).value == True

