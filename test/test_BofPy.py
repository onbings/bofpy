import sys
import os
# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import datetime

from bofpy.BofPy import (   
    DATA_TYPE,
    Bof_Init,
    Bof_Shutdown,
    Bof_GetVersion,
    Bof_ExitApp,
    Bof_IsInteger,
    Bof_MsSleep,
    Bof_UsSleep,
    Bof_NsSleep,
    Bof_GetMsTickCount,
    Bof_GetUsTickCount,
    Bof_GetNsTickCount,
    Bof_ElapsedMsTime,
    Bof_ElapsedUsTime,
    Bof_ElapsedNsTime,
    Bof_IsElapsedTimeInMs,
    Bof_IsElapsedTimeInUs,
    Bof_IsElapsedTimeInNs,
    Bof_EscapeAndSplit,
    Bof_Random,
    Bof_RandomHexa,
    Bof_Now,
    Bof_TicketGenerator,
    Bof_Serializer,
)

class TestBofPy(unittest.TestCase):
    SLEEP_TIME_IN_MS = 250
    
    def test_Bof_Init(self):
        config_dir, data_dir = Bof_Init("test_app")
        self.assertTrue(os.path.isdir(config_dir))
        self.assertTrue(os.path.isdir(data_dir))

    def test_Bof_Shutdown(self):
        # No specific behavior to test for Bof_Shutdown
        pass

    def test_Bof_GetVersion(self):
        self.assertEqual(Bof_GetVersion(), "0.1.1")
    
    def test_Bof_ExitApp(self):
        with self.assertRaises(SystemExit) as cm:
            Bof_ExitApp("Test exit message", 1)
        self.assertEqual(cm.exception.code, 1)

    def test_Bof_IsInteger_valid_integer(self):
        result = Bof_IsInteger("42", 0)
        self.assertEqual(result, (True, 42))
        
    def test_Bof_IsInteger_invalid_integer(self):
        result = Bof_IsInteger("not_an_integer", 0)
        self.assertEqual(result, (False, 0))

    def test_Bof_MsSleep(self):
        timer = Bof_GetMsTickCount()
        Bof_MsSleep(self.SLEEP_TIME_IN_MS)
        elapsed_time = Bof_ElapsedMsTime(timer)
        self.assertGreaterEqual(elapsed_time, (self.SLEEP_TIME_IN_MS * 0.90))
        self.assertLessEqual(elapsed_time, (self.SLEEP_TIME_IN_MS * 1.10))
    
    def test_Bof_UsSleep(self):
        timer = Bof_GetUsTickCount()
        Bof_UsSleep(self.SLEEP_TIME_IN_MS * 1000)
        elapsed_time = Bof_ElapsedUsTime(timer)
        self.assertGreaterEqual(elapsed_time, (self.SLEEP_TIME_IN_MS * 1000 * 0.90))
        self.assertLessEqual(elapsed_time, (self.SLEEP_TIME_IN_MS * 1000 * 1.10))
        
    def test_Bof_NsSleep(self):
        timer = Bof_GetNsTickCount()
        Bof_NsSleep(self.SLEEP_TIME_IN_MS * 1000 * 1000)
        elapsed_time = Bof_ElapsedNsTime(timer)
        self.assertGreaterEqual(elapsed_time, (self.SLEEP_TIME_IN_MS * 1000 * 1000  *0.90))
        self.assertLessEqual(elapsed_time, (self.SLEEP_TIME_IN_MS * 1000*1000*1.10))
                    
    def test_Bof_GetMsTickCount(self):
        # It's challenging to test the exact value, so we'll just check if it runs without errors
        result = Bof_GetMsTickCount()
        self.assertIsInstance(result, int)

    def test_Bof_GetUsTickCount(self):
        # It's challenging to test the exact value, so we'll just check if it runs without errors
        result = Bof_GetUsTickCount()
        self.assertIsInstance(result, int)
        
    def test_Bof_GetNsTickCount(self):
        # It's challenging to test the exact value, so we'll just check if it runs without errors
        result = Bof_GetNsTickCount()
        self.assertIsInstance(result, int)
                
    def test_Bof_IsElapsedTimeInMs(self):
       timer = Bof_GetMsTickCount()
       Bof_MsSleep(self.SLEEP_TIME_IN_MS)
       self.assertTrue(Bof_IsElapsedTimeInMs(timer, self.SLEEP_TIME_IN_MS * 0.5))
       self.assertFalse(Bof_IsElapsedTimeInMs(timer, self.SLEEP_TIME_IN_MS * 1.5))
      
    def test_Bof_IsElapsedTimeInUs(self):
       timer = Bof_GetUsTickCount()
       Bof_MsSleep(self.SLEEP_TIME_IN_MS)
       self.assertTrue(Bof_IsElapsedTimeInUs(timer, self.SLEEP_TIME_IN_MS * 1000 * 0.5))
       self.assertFalse(Bof_IsElapsedTimeInUs(timer, self.SLEEP_TIME_IN_MS * 1000 * 1.5))
              
    def test_Bof_IsElapsedTimeInNs(self):
       timer = Bof_GetNsTickCount()
       Bof_MsSleep(self.SLEEP_TIME_IN_MS)
       self.assertTrue(Bof_IsElapsedTimeInNs(timer, self.SLEEP_TIME_IN_MS * 1000 *1000 * 0.5))
       self.assertFalse(Bof_IsElapsedTimeInNs(timer, self.SLEEP_TIME_IN_MS * 1000 *1000 * 1.5))
                      
    def test_escape_and_split_basic(self):
        input_string = r'first\|second\|third'
        split_character = '|'
        result = Bof_EscapeAndSplit(input_string, split_character)
        # Check the result against the expected output
        expected_result = ['first|second|third']
        self.assertEqual(result, expected_result)

    def test_escape_and_split_with_backslashes(self):
        input_string = r'one\|two\|three\\\|four'
        split_character = '|'
        result = Bof_EscapeAndSplit(input_string, split_character)
        # Check the result against the expected output
        expected_result = ['one|two|three\\\\|four']
        self.assertEqual(result, expected_result)

    # collision with the other Bof_Random just below in test_bof_random_string
    # def test_bof_random(self):
    #     min_value = 1
    #     max_value = 10
    #     result = Bof_Random(min_value, max_value)
    #     self.assertGreaterEqual(result, min_value)
    #     self.assertLessEqual(result, max_value)

    def test_bof_random_string(self):
        length = 10
        min_char = 65  # ASCII value of 'A'
        max_char = 90  # ASCII value of 'Z'
        result =Bof_Random(length, min_char, max_char)
        self.assertEqual(len(result), length)
        for char in result:
            char_code = ord(char)
            self.assertGreaterEqual(char_code, min_char)
            self.assertLessEqual(char_code, max_char)

    def test_bof_random_hexa_uppercase(self):
        length = 8
        result = Bof_RandomHexa(length, upper_case=True)
        self.assertEqual(len(result), length)
        for char in result:
            self.assertIn(char, '0123456789ABCDEF')

    def test_bof_random_hexa_lowercase(self):
        length = 12
        result = Bof_RandomHexa(length, upper_case=False)
        self.assertEqual(len(result), length)
        for char in result:
            self.assertIn(char, '0123456789abcdef')
    
    def test_bof_now_default_format(self):
        result = Bof_Now()
        # Check if the result is a string
        self.assertIsInstance(result, str)
        # Attempt to parse the result as a datetime object
        try:
            datetime.datetime.strptime(result, "%d/%m/%Y %H:%M:%S.%f")
        except ValueError:
            self.fail("Failed to parse the result as a valid datetime string")

    def test_bof_now_custom_format(self):
        custom_format = "%Y-%m-%d %H:%M:%S"
        result = Bof_Now(format=custom_format)
        # Check if the result is a string
        self.assertIsInstance(result, str)

        # Attempt to parse the result as a datetime object using the custom format
        try:
            datetime.datetime.strptime(result, custom_format)
        except ValueError:
            self.fail("Failed to parse the result as a valid datetime string with the custom format")


    def test_Bof_TicketGenerator(self):
        ticket_gen = Bof_TicketGenerator(DATA_TYPE.DATA_TYPE_U8)
        self.assertEqual(ticket_gen.next(), 1)
        self.assertEqual(ticket_gen.next(), 2)
        ticket_gen.reset()
        self.assertEqual(ticket_gen.current(), 1)

    def test_Bof_SerializerLe(self):
        serializer = Bof_Serializer(little_endian=True)
        serializer.push(DATA_TYPE.DATA_TYPE_U8, 42)
        serialized_data = serializer.get_ser_buffer()
        popped_values = serializer.pop(DATA_TYPE.DATA_TYPE_U8, 1)
        self.assertEqual(popped_values, [42])
        self.assertEqual(serializer.get_ser_buffer_len(), 0)
        serializer.push(DATA_TYPE.DATA_TYPE_U8, 1)
        self.assertEqual(serializer.get_ser_buffer_len(), 1)
        serializer.push(DATA_TYPE.DATA_TYPE_U16, 2)
        self.assertEqual(serializer.get_ser_buffer_len(), 3)
        serializer.push(DATA_TYPE.DATA_TYPE_U32, 3)
        self.assertEqual(serializer.get_ser_buffer_len(), 7)
  
        popped_values = serializer.pop(DATA_TYPE.DATA_TYPE_U32, 1)
        self.assertEqual(popped_values, [3])
        self.assertEqual(serializer.get_ser_buffer_len(), 3)
        popped_values = serializer.pop(DATA_TYPE.DATA_TYPE_U16, 1)
        self.assertEqual(popped_values, [2])
        self.assertEqual(serializer.get_ser_buffer_len(), 1)
        popped_values = serializer.pop(DATA_TYPE.DATA_TYPE_U8, 1)
        self.assertEqual(popped_values, [1])
        self.assertEqual(serializer.get_ser_buffer_len(), 0)
    
        serializer.push(DATA_TYPE.DATA_TYPE_U8, 42)
        self.assertEqual(serializer.get_ser_buffer_len(), 1)
        serialized_data = serializer.reset()
        self.assertEqual(serializer.get_ser_buffer_len(), 0)
        with self.assertRaises(ValueError):
            popped_values = serializer.pop(DATA_TYPE.DATA_TYPE_U8, 1)
            
        for i in range(10):
            serializer.push(DATA_TYPE.DATA_TYPE_U16, (i*256)+i)    
        self.assertEqual(serializer.get_ser_buffer_len(), 10*2)
        popped_values=serializer.pop(DATA_TYPE.DATA_TYPE_U16, 3)    
        self.assertEqual(popped_values, [0x0909, 0x0808, 0x0707])   
        self.assertEqual(serializer.get_ser_buffer_len(), 7*2)
        popped_values=serializer.pop(DATA_TYPE.DATA_TYPE_U16, 3)   
        self.assertEqual(popped_values, [0x0606, 0x0505, 0x0404])   
        self.assertEqual(serializer.get_ser_buffer_len(), 4*2)
        popped_values=serializer.pop(DATA_TYPE.DATA_TYPE_U16, 3)   
        self.assertEqual(popped_values, [0x0303, 0x0202, 0x0101])   
        self.assertEqual(serializer.get_ser_buffer_len(), 1*2)
        with self.assertRaises(ValueError):
           popped_values=serializer.pop(DATA_TYPE.DATA_TYPE_U16, 2)   
        popped_values=serializer.pop(DATA_TYPE.DATA_TYPE_U16, 1)   
        self.assertEqual(serializer.get_ser_buffer_len(), 0)       

    def test_Bof_SerializerBe(self):
        serializer = Bof_Serializer(little_endian=False)
        serializer.push(DATA_TYPE.DATA_TYPE_U8, 42)
        serialized_data = serializer.get_ser_buffer()
        popped_values = serializer.pop(DATA_TYPE.DATA_TYPE_U8, 1)
        self.assertEqual(popped_values, [42])
        self.assertEqual(serializer.get_ser_buffer_len(), 0)
        serializer.push(DATA_TYPE.DATA_TYPE_U8, 1)
        self.assertEqual(serializer.get_ser_buffer_len(), 1)
        serializer.push(DATA_TYPE.DATA_TYPE_U16, 2)
        self.assertEqual(serializer.get_ser_buffer_len(), 3)
        serializer.push(DATA_TYPE.DATA_TYPE_U32, 3)
        self.assertEqual(serializer.get_ser_buffer_len(), 7)
  
        popped_values = serializer.pop(DATA_TYPE.DATA_TYPE_U32, 1)
        self.assertEqual(popped_values, [3])
        self.assertEqual(serializer.get_ser_buffer_len(), 3)
        popped_values = serializer.pop(DATA_TYPE.DATA_TYPE_U16, 1)
        self.assertEqual(popped_values, [2])
        self.assertEqual(serializer.get_ser_buffer_len(), 1)
        popped_values = serializer.pop(DATA_TYPE.DATA_TYPE_U8, 1)
        self.assertEqual(popped_values, [1])
        self.assertEqual(serializer.get_ser_buffer_len(), 0)
    
        serializer.push(DATA_TYPE.DATA_TYPE_U8, 42)
        self.assertEqual(serializer.get_ser_buffer_len(), 1)
        serialized_data = serializer.reset()
        self.assertEqual(serializer.get_ser_buffer_len(), 0)
        with self.assertRaises(ValueError):
            popped_values = serializer.pop(DATA_TYPE.DATA_TYPE_U8, 1)
            
        for i in range(10):
            serializer.push(DATA_TYPE.DATA_TYPE_U16, (i*256)+i)    
        self.assertEqual(serializer.get_ser_buffer_len(), 10*2)
        popped_values=serializer.pop(DATA_TYPE.DATA_TYPE_U16, 3)    
        self.assertEqual(popped_values, [0x0909, 0x0808, 0x0707])   
        self.assertEqual(serializer.get_ser_buffer_len(), 7*2)
        popped_values=serializer.pop(DATA_TYPE.DATA_TYPE_U16, 3)   
        self.assertEqual(popped_values, [0x0606, 0x0505, 0x0404])   
        self.assertEqual(serializer.get_ser_buffer_len(), 4*2)
        popped_values=serializer.pop(DATA_TYPE.DATA_TYPE_U16, 3)   
        self.assertEqual(popped_values, [0x0303, 0x0202, 0x0101])   
        self.assertEqual(serializer.get_ser_buffer_len(), 1*2)
        with self.assertRaises(ValueError):
           popped_values=serializer.pop(DATA_TYPE.DATA_TYPE_U16, 2)   
        popped_values=serializer.pop(DATA_TYPE.DATA_TYPE_U16, 1)   
        self.assertEqual(serializer.get_ser_buffer_len(), 0)       

if __name__ == '__main__':
    unittest.main()
