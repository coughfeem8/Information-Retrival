'''
assertEqual(a, b) 	 a == b 	 
assertNotEqual(a, b) 	 a != b 	 
assertTrue(x) 	         bool(x) is True 	 
assertFalse(x) 	         bool(x) is False 	 
assertIs(a, b) 	         a is b 	
assertIsNot(a, b) 	 a is not b 	
assertIsNone(x) 	 x is None 	
assertIsNotNone(x) 	 x is not None 	
assertIn(a, b) 	         a in b 	
assertNotIn(a, b) 	 a not in b 	
assertIsInstance(a, b)   isinstance(a, b)       
assertNotIsInstance(a, b)not isinstance(a, b)
'''
import unittest,sys, random
sys.path.append('../src')
from  part1  import prime_index, area_based_avg, sur_real_pix, r_val_indx

class TestLab3(unittest.TestCase):

    #before each method
    def setUp(self):
        pass

    #after each method
    def teardown():
        pass
    #before the first test
    def setUpclass():
        pass

    #after last test
    def teardownClass():
        pass
    
    def test_prime_index(self):
        self.assertEqual(round(prime_index(10.0),2),0.00)
        self.assertEqual(prime_index(0.5),0.5)
        self.assertEqual(round(prime_index(15.65),2),0.65)
                         
if __name__ == '__main__':
    unittest.main()
