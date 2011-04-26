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
   

