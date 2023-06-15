import array


A1 = array.Array((4,), 1, -2, 3, -4)
A2 = array.Array((4,), 4.5, 3.5, 2.5, 1.5)


B = array.Array((3, 2), 1, -2, 3, -4, 5, -6)
B2 = array.Array((2, 3), 1, -2, 3, -4, 5, -6)
C = array.Array((2, 3, 2), 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12) 

def test_str():    
    assert A1.__str__() == "(1, -2, 3, -4)"
    assert B.__str__() == "((1, -2), (3, -4), (5, -6))"
    assert C.__str__() == "(((1, 2), (3, 4), (5, 6)), ((7, 8), (9, 10), (11, 12)))"


def test_add():
    #Test __add__ for 1D-arrays
    assert A1 + 10 == array.Array((4,), 11, 8, 13, 6)
    assert 10 + A1 == array.Array((4,), 11, 8, 13, 6)
    assert A1 + A2 == array.Array((4,), 5.5, 1.5, 5.5, -2.5)
    
    #Test __add__ for 2D-arrays
    assert B + 10 == array.Array((3,2), 11, 8, 13, 6, 15, 4)
    assert 10 + B == array.Array((3,2), 11, 8, 13, 6, 15, 4)
    assert B + B == array.Array((3,2), 2, -4, 6, -8, 10, -12)
    
    #Test __add__ for nD-arrays
    assert C + C == array.Array((2, 3, 2), 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24) 



def test_sub():
    #Test __sub__ for 1D-arrays
    assert A1 - 10 == array.Array((4,), -9, -12, -7, -14)
    assert 10 - A1 == array.Array((4,), -9, -12, -7, -14)
    assert A1 - A2 == array.Array((4,), -3.5, -5.5, 0.5, -5.5)
    
    #Test __sub__ for 2D-arrays
    assert B - 10 == array.Array((3,2), -9, -12, -7, -14, -5, -16)
    assert 10 - B == array.Array((3,2), -9, -12, -7, -14, -5, -16)
    assert B - B == array.Array((3,2), 0, 0, 0, 0, 0, 0)
    
    #Test __sub__ for nD-arrays
    assert C - C == array.Array((2, 3, 2), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) 



def test_mul():
    #Test __mul__ for 1D-arrays
    assert A1 * 10 == array.Array((4,), 10, -20, 30, -40)
    assert 10 * A1 == array.Array((4,), 10, -20, 30, -40)
    assert A1 * A2 == array.Array((4,), 4.5, -7.0, 7.5, -6.0)
    
    #Test __mul__ for 2D-arrays
    assert B * 10 == array.Array((3,2), 10, -20, 30, -40, 50, -60)
    assert 10 * B == array.Array((3,2), 10, -20, 30, -40, 50, -60)
    assert B * B == array.Array((3,2), 1, 4, 9, 16, 25, 36)
    
    #Test __mul__ for nD-arrays
    assert C * C == array.Array((2, 3, 2), 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144) 



def test_eq(): 
    #Test __eq__ 
    assert (A1 == array.Array((4,), 1, -2, 3, -4)) == True 
    assert (A1 * 10 == 10 * A1) == True
    assert (B == B) == True 
    assert (C == C) == True
    assert (A1 == B) == False
    assert (B == B2) == False
    assert (B == 4) == False 
    

def test_is_equal():
    #Test is_equal
    assert A1.is_equal(A2) == array.Array((4,), False, False, False, False)
    assert A1.is_equal(-2) == array.Array((4,), False, True, False, False)
    assert B.is_equal(B) == array.Array((3, 2), True, True, True, True, True, True)
    assert B2.is_equal(1) == array.Array((2, 3), True, False, False, False, False, False)
    
def test_min_element():
    #Test min_element
    assert A1.min_element() == -4
    assert A2.min_element() == 1.5
    assert B.min_element() == -6
    assert B2.min_element() == -6
    assert C.min_element() == 1
    
    
def test_get_item():
    #Test get_item 
    assert A1[0] == 1
    assert B[1] == (3, -4)
    assert B[1][0] == 3
    assert B2[1] == (-4, 5, -6)
    assert B2[1][0] == -4
    assert C[1][2][1] == 12 

    
