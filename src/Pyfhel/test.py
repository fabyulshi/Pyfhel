
# Global modules
import unittest
import time
import sys
import numpy as np

# Local module
from Pyfhel import Pyfhel
from PyCtxt import PyCtxt
from PyPtxt import PyPtxt

from util import ENCODING_t

# Value of p for batching: p=1964769281

class PyfhelTestCase(unittest.TestCase):
    
    def setUp(self):
        self.t0 = time.time()

    def tearDown(self):
        sys.stderr.write('({}s) ...'.format(
            round(time.time() - self.t0 , 3)))
    def TEST_PyPtxt_PyCtxt(self):
        pass
    def test_PyPtxt_creation_deletion(self):    
        try:
            self.ptxt = PyPtxt()
        except Exception as err:
            self.fail("PyPtxt() creation failed unexpectedly: ", err)
        self.assertEqual(self.ptxt._encoding, ENCODING_t.UNDEFINED)
        self.ptxt._encoding=ENCODING_t.INTEGER
        self.assertEqual(self.ptxt._encoding, ENCODING_t.INTEGER)
        del(self.ptxt._encoding)
        self.assertEqual(self.ptxt._encoding, ENCODING_t.UNDEFINED)
        try:
            del(self.ptxt)
        except Exception as err:
            self.fail("PyPtxt() deletion failed unexpectedly: ", err)
        
    def test_PyCtxt_creation_deletion(self):    
        try:
            self.ctxt = PyCtxt()
        except Exception as err:
            self.fail("PyCtxt() creation failed unexpectedly: ", err)
        self.assertEqual(self.ctxt.size(), 2)
        self.assertEqual(self.ctxt._encoding, ENCODING_t.UNDEFINED)
        self.ctxt._encoding=ENCODING_t.FRACTIONAL
        self.assertEqual(self.ctxt._encoding, ENCODING_t.FRACTIONAL)
        del(self.ctxt._encoding)
        self.assertEqual(self.ctxt._encoding, ENCODING_t.UNDEFINED)
        self.assertEqual(self.ctxt.size(), 2)    
        try:
            del(self.ctxt)
        except Exception as err:
            self.fail("PyCtxt() deletion failed unexpectedly: ", err)
        
    def test_Pyfhel_1_GENERATION(self):
        pass
    def test_Pyfhel_1a_creation_deletion(self):    
        try:
            self.pyfhel = Pyfhel()
        except Exception as err:
            self.fail("Pyfhel() creation failed unexpectedly: ", err)
        try:
            del(self.pyfhel)
        except Exception as err:
            self.fail("Pyfhel() deletion failed unexpectedly: ", err)
            
    def test_Pyfhel_1b_context_n_key_generation(self):  
        self.pyfhel = Pyfhel()
        self.pyfhel.ContextGen(65537)
        self.pyfhel.KeyGen() 
        
    def test_Pyfhel_1c_rotate_key_generation(self):  
        self.pyfhel = Pyfhel()
        self.pyfhel.ContextGen(65537)
        self.pyfhel.KeyGen() 
        self.pyfhel.rotateKeyGen(30)
        self.pyfhel.rotateKeyGen(1)  
        self.pyfhel.rotateKeyGen(60) 
        self.assertRaises(SystemError, lambda: self.pyfhel.rotateKeyGen(61))
        self.assertRaises(SystemError, lambda: self.pyfhel.rotateKeyGen(0))
        
    def test_Pyfhel_1d_relin_key_generation(self):  
        self.pyfhel = Pyfhel()
        self.pyfhel.ContextGen(65537)
        self.pyfhel.KeyGen() 
        self.pyfhel.relinKeyGen(30)
        self.pyfhel.relinKeyGen(1)  
        self.pyfhel.relinKeyGen(60) 
        self.assertRaises(SystemError, lambda: self.pyfhel.relinKeyGen(61))
        self.assertRaises(SystemError, lambda: self.pyfhel.relinKeyGen(0))
        
    def test_Pyfhel_2_ENCODING(self):
        pass
    
    def test_Pyfhel_2a_encode_decode_int(self):
        self.pyfhel = Pyfhel()
        self.pyfhel.ContextGen(p=65537)
        self.pyfhel.KeyGen() 
        self.ptxt = self.pyfhel.encodeInt(127)
        self.assertEqual(self.ptxt.to_string(), b'1x^6 + 1x^5 + 1x^4 + 1x^3 + 1x^2 + 1x^1 + 1')
        self.assertEqual(self.pyfhel.decodeInt(self.ptxt), 127)
        self.pyfhel.encodeInt(-2, self.ptxt)
        self.assertEqual(self.ptxt.to_string(),  b'10000x^1')
        self.assertEqual(self.pyfhel.decodeInt(self.ptxt), -2)
                        
    def test_Pyfhel_2b_encode_decode_float(self):
        self.pyfhel = Pyfhel()
        self.pyfhel.ContextGen(p=65537, m=8192, base=2, intDigits = 80, fracDigits = 20)
        self.pyfhel.KeyGen() 
        self.ptxt = self.pyfhel.encodeFrac(19.30)
        self.assertTrue(self.ptxt.to_string(), b'9x^8190 + 1x^4 + 1x^1 + 1')
        self.assertEqual(round(self.pyfhel.decodeFrac(self.ptxt), 2), 19.30)
        self.pyfhel.encodeFrac(-2.25, self.ptxt)
        self.assertEqual(self.ptxt.to_string(),  b'1x^8190 + 10000x^1')
        self.assertEqual(round(self.pyfhel.decodeFrac(self.ptxt), 2), -2.25)
    
            
    def test_Pyfhel_2c_encode_decode_batch(self):
        self.pyfhel = Pyfhel()
        self.pyfhel.ContextGen(p=1964769281, m=8192, base=2, sec=192, flagBatching=True)
        self.pyfhel.KeyGen() 
        self.assertTrue(self.pyfhel.batchEnabled())
        self.ptxt = self.pyfhel.encodeBatch([1, 2, 3, 4, 5, 6])
        self.assertEqual(self.pyfhel.getnSlots(), 8192)
        self.assertEqual(self.pyfhel.decodeBatch(self.ptxt)[:6], [1, 2, 3, 4, 5, 6])
        
        #print(self.ptxt.to_string())
        
    def test_Pyfhel_2d_encode_decode_array(self):
        self.pyfhel = Pyfhel()
        self.pyfhel.ContextGen(p=1964769281, m=8192, base=2, sec=192, flagBatching=True)
        self.pyfhel.KeyGen() 
        self.assertTrue(self.pyfhel.batchEnabled())
        self.ptxt = self.pyfhel.encodeArray(np.array([1, 2, 3, 4, 5, 6]))
        self.assertEqual(self.pyfhel.getnSlots(), 8192)
        self.assertTrue(np.alltrue(self.pyfhel.decodeArray(self.ptxt)[:6] == np.array([1, 2, 3, 4, 5, 6])))
            
    def test_Pyfhel_3_ENCRYPTING(self):
        pass
    
    def test_Pyfhel_3a_encrypt_decrypt_int(self):
        self.pyfhel = Pyfhel()
        self.pyfhel.ContextGen(p=65537)
        self.pyfhel.KeyGen() 
        self.ctxt = self.pyfhel.encryptInt(127)
        self.assertEqual(self.pyfhel.decryptInt(self.ctxt), 127)
        self.pyfhel.encryptInt(-2, self.ctxt)
        self.assertEqual(self.pyfhel.decryptInt(self.ctxt), -2)
                        
    def test_Pyfhel_3b_encrypt_decrypt_float(self):
        self.pyfhel = Pyfhel()
        self.pyfhel.ContextGen(p=65537, m=8192, base=2, intDigits = 80, fracDigits = 20)
        self.pyfhel.KeyGen() 
        self.ptxt = self.pyfhel.encodeFrac(19.30)
        self.assertTrue(self.ptxt.to_string(), b'9x^8190 + 1x^4 + 1x^1 + 1')
        self.assertEqual(round(self.pyfhel.decodeFrac(self.ptxt), 2), 19.30)
        self.pyfhel.encodeFrac(-2.25, self.ptxt)
        self.assertEqual(self.ptxt.to_string(),  b'1x^8190 + 10000x^1')
        self.assertEqual(round(self.pyfhel.decodeFrac(self.ptxt), 2), -2.25)
    
            
    def test_Pyfhel_3c_encrypt_decrypt_batch(self):
        self.pyfhel = Pyfhel()
        self.pyfhel.ContextGen(p=1964769281, m=8192, base=2, sec=192, flagBatching=True)
        self.pyfhel.KeyGen() 
        self.assertTrue(self.pyfhel.batchEnabled())
        self.ptxt = self.pyfhel.encodeBatch([1, 2, 3, 4, 5, 6])
        self.assertEqual(self.pyfhel.getnSlots(), 8192)
        self.assertEqual(self.pyfhel.decodeBatch(self.ptxt)[:6], [1, 2, 3, 4, 5, 6])
        
        #print(self.ptxt.to_string())
        
    def test_Pyfhel_3d_encrypt_decrypt_array(self):
        self.pyfhel = Pyfhel()
        self.pyfhel.ContextGen(p=1964769281, m=8192, base=2, sec=192, flagBatching=True)
        self.pyfhel.KeyGen() 
        self.assertTrue(self.pyfhel.batchEnabled())
        self.ptxt = self.pyfhel.encodeArray(np.array([1, 2, 3, 4, 5, 6]))
        self.assertEqual(self.pyfhel.getnSlots(), 8192)
        self.assertTrue(np.alltrue(self.pyfhel.decodeArray(self.ptxt)[:6] == np.array([1, 2, 3, 4, 5, 6])))
if __name__ == '__main__':
    unittest.main(verbosity=2)