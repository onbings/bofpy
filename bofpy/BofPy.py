import time
import datetime
import sys
import os
import re
import random
import struct
from typing import Tuple, List
from enum import auto,Enum

class DATA_TYPE(Enum):
    DATA_TYPE_U8 = 8
    DATA_TYPE_U16 = 16
    DATA_TYPE_U32 = 32
    DATA_TYPE_U64= 64
    
def Bof_Init(app_name:str)->Tuple[str,str]:
    if hasattr(sys, "_MEIPASS"):
        DataDir = os.path.join(sys._MEIPASS, "data")
        print(f"Running from the packaged version (data in {DataDir}).")
    else:
        DataDir = os.path.join(os.getcwd(), "data")
        print(f"Running from the non-packaged version (data in {DataDir}).")
    if not os.path.isdir(DataDir):
        os.makedirs(DataDir)
        
    ConfigDir = os.path.join(os.path.expanduser("~"), f".{app_name}")
    if not os.path.isdir(ConfigDir):
        os.makedirs(ConfigDir)
    print(f"Config in {ConfigDir}.")
    return ConfigDir,DataDir
    
def Bof_Shutdown():
    pass

def Bof_ExitApp(msg, exit_code):
    print(f"{msg}")
    print(f"exit_app with code {exit_code}")
    sys.exit(exit_code)

def Bof_IsInteger(num:str, val_if_not_int:int)->Tuple[bool,int]:
    try:
        val=int(num)
        return True,val
    except ValueError:
        return False,val_if_not_int
    
def Bof_MsSleep(ms:int):
    time.sleep(ms / 1000)
   
def Bof_UsSleep(us:int):
    time.sleep(us / 1000/1000)
    
def Bof_NsSleep(ns:int):
    time.sleep(ns / 1000/1000/1000)
            
def Bof_GetMsTickCount()->int:
    return (int)(time.perf_counter_ns()/1000000)

def Bof_GetUsTickCount()->int:
    return (int)(time.perf_counter_ns()/1000)

def Bof_GetNsTickCount()->int:
    return (int)(time.perf_counter_ns())

def Bof_ElapsedMsTime(start_in_ms:int)->int:
    return Bof_GetMsTickCount() - start_in_ms

def Bof_ElapsedUsTime(start_in_us:int)->int:
    return Bof_GetUsTickCount() - start_in_us

def Bof_ElapsedNsTime(start_in_ns:int)->int:
    return Bof_GetNsTickCount() - start_in_ns

def Bof_IsElapsedTimeInMs(start_in_ms:int, timeout_in_ms:int)->bool:
    return Bof_ElapsedMsTime(start_in_ms) >= timeout_in_ms

def Bof_IsElapsedTimeInUs(start_in_us:int, timeout_in_us:int)->bool:
    return Bof_ElapsedUsTime(start_in_us) >= timeout_in_us

def Bof_IsElapsedTimeInNs(start_in_ns:int, timeout_in_ns:int)->bool:
    return Bof_ElapsedNsTime(start_in_ns) >= timeout_in_ns

def Bof_EscapeAndSplit(input_string:str, split_character:str)->str:
    # Use re.split with a regular expression to split the string, preserving the escaped character
    split_pattern = r'(?<!\\)' + re.escape(split_character)
    result = re.split(split_pattern, input_string)

    # Remove escape characters from the result
    return [item.replace('\\' + split_character, split_character) for item in result]

def Bof_Random(min_value:int, max_value:int)->int:
    return random.randint(min_value, max_value)
    
def Bof_Random(length: int, min_char: int, max_char: int)->str:
    rts=""
    for i in range(length):
        random_char = random.randint(min_char, max_char)
        rts += chr(random_char)
    return rts
 
def Bof_RandomHexa(length: int, upper_case: bool)->str:
    hex_digits = "0123456789abcdef"
    if upper_case:
        hex_digits = hex_digits.upper()

    random_string = ""
    for i in range(length):
        random_char = random.choice(hex_digits)
        random_string += random_char
    return random_string

def Bof_Now(format: str = "%d/%m/%Y %H:%M:%S.%f")->str:
    current_time = datetime.datetime.now()
    return current_time.strftime(format)

class Bof_TicketGenerator:
    def __init__(self, data_type:DATA_TYPE)->None:    
        self.num_bits = data_type.value
        self.max_value = (1 << self.num_bits) - 1  # Calculate the maximum value based on the number of bits
        self.ticket_num = 0
        
    def next(self)->int:
        self.ticket_num = (self.ticket_num + 1) & self.max_value  # Ensure the ticket number stays within bounds
        if self.ticket_num == 0:
            self.ticket_num = 1
        return self.ticket_num
    
    def current(self)->int:
        return self.ticket_num if self.ticket_num!=0 else 1
    
    def reset(self)->None:
        self.ticket_num = 0
        
class Bof_Serializer:
    def __init__(self, little_endian)->None:    
        self.little_endian = little_endian
        self.byte_buffer = bytearray()

    def push(self, data_type: DATA_TYPE, *values):
        if  self.little_endian:
            for value in values:
                if data_type == DATA_TYPE.DATA_TYPE_U8:
                    self.byte_buffer.extend(struct.pack('<B', value))
                elif data_type == DATA_TYPE.DATA_TYPE_U16:
                    self.byte_buffer.extend(struct.pack('<H', value))
                elif data_type == DATA_TYPE.DATA_TYPE_U32:
                    self.byte_buffer.extend(struct.pack('<I', value))
                elif data_type == DATA_TYPE.DATA_TYPE_U64:
                    self.byte_buffer.extend(struct.pack('<Q', value))     
        else:
            for value in values:
                if data_type == DATA_TYPE.DATA_TYPE_U8:
                    self.byte_buffer.extend(struct.pack('>B', value))
                elif data_type == DATA_TYPE.DATA_TYPE_U16:
                    self.byte_buffer.extend(struct.pack('>H', value))
                elif data_type == DATA_TYPE.DATA_TYPE_U32:
                    self.byte_buffer.extend(struct.pack('>I', value))
                elif data_type == DATA_TYPE.DATA_TYPE_U64:
                    self.byte_buffer.extend(struct.pack('>Q', value))                
                else:
                    raise ValueError("Unsupported data_type")
                
    def pop(self, data_type: DATA_TYPE, count: int):
        popped_value_collection = []
        if data_type == DATA_TYPE.DATA_TYPE_U8:
            size = 1
            format_str = '<B' if self.little_endian else '>B'
        elif data_type == DATA_TYPE.DATA_TYPE_U16:
            size = 2
            format_str = '<H' if self.little_endian else '>H'
        elif data_type == DATA_TYPE.DATA_TYPE_U32:
            size = 4
            format_str = '<I' if self.little_endian else '>I'
        elif data_type == DATA_TYPE.DATA_TYPE_U64:
            size = 8
            format_str = '<Q' if self.little_endian else '>Q'
        else:
            raise ValueError("Unsupported data_type")
        if len(self.byte_buffer) >= (size*count):
            start_index = len(self.byte_buffer) - size
            for _ in range(count):
                value = struct.unpack(format_str, self.byte_buffer[start_index:start_index+size])[0]
                popped_value_collection.append(value)
                if start_index!= 0:  #last elem
                    start_index -= size
            self.byte_buffer = self.byte_buffer[:-(count * size)]
        else:
            raise ValueError("Not enough bytes in the byte_buffer")
        return popped_value_collection 
        
    def reset(self):
        self.byte_buffer = bytearray()           
   
    def set_ser_buffer(self, data:bytearray):
        self.byte_buffer = data    
                
    def get_ser_buffer(self)->bytearray:
        return  self.byte_buffer
    
    def get_ser_buffer_len(self)->int:
        return len(self.byte_buffer) 
    
