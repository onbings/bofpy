import socket
import ftplib
import BofPy  
import BofSocket
from typing import Tuple, List
from enum import auto,Enum

class Bof_Ip_Address:
    def __init__(self, endpoint)->None:    
        self.parse_ip_endpoint(endpoint)
 
    def get_ip_endpoint_param(self)->Tuple[bool,str,str,int]:
        return self.valid, self.protocol, self.ip, int(self.port)
    
    def parse_ip_endpoint(self, endpoint: str)->Tuple[bool,str,str,int]:
        self.valid = True
        self.protocol= ""
        self.ip = ""
        self.port = "0"
        try:
            if "://" in endpoint:
                self.protocol, address = endpoint.split("://", 1)
            else:
                self.protocol =""
                address=endpoint
            if ":" in address:            
                self.ip, self.port = address.split(":", 1)
            else:
                self.ip=address
                self.port=0
            if address=="":
                self.valid=False
        except:
            self.valid = False
        return self.valid, self.protocol, self.ip, int(self.port)

    def build_ip_endpoint(self, protocol:str, ip:str, port:int)->Tuple[bool,str,str,int]:
        if protocol!="":
            endpoint = protocol + "://" + ip
        else:
            endpoint = ip
        if port!=0:
           endpoint = endpoint + ":" + str(port)
        return self.parse_ip_endpoint(endpoint)
        #return protocol + "://" + ip + ":" + str(port)
    
    def to_string(self)->str:
        if self.protocol!="":
            rts = self.protocol + "://" + self.ip
        else:
            rts = self.ip
        if self.port!=0:
           rts = rts + ":" + str(self.port)        
        return rts
    
class Bof_Ftp_Socket:
    def __init__(self)->None:    
        self.connected = False
        self.tcp=False
        self.sock = None
        
    def connect(self, endpoint:str)->bool:
        if not self.connected:
            ip_address = Bof_Ip_Address(endpoint)
            sts, protocol, ip, port = ip_address.get_ip_endpoint_param()
            if sts:
                self.tcp = (protocol!="udp")
                if self.tcp:
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        self.sock.connect((ip, port))
                        print(f"Connection to {ip}:{port} successful.")
                        self.connected = True
                    except socket.error as e:
                        print(f"[!EXCPT!] Connection to {ip}:{port} failed. Error: {e}")
                else:
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind the UDP socket to the target host and port
                    try:
                        self.sock.bind(ip, port)
                        print(f"Bind to {ip}:{port} successful")
                        self.connected = True
                    except socket.error as e:
                        print(f"[!EXCPT!] Bind to {ip}:{port} failed. Error: {e}")
        return self.connected
    
    def read_string(self,timeout_ms:int)->Tuple[bool,str]:
        rts = False
        received_data = b""
        if self.connected:     
            self.sock.settimeout(timeout_ms / 1000)  # Set the socket timeout in seconds
            while True:
                try:
                    chunk = self.sock.recv(1)  # Read one byte at a time
                    if not chunk:  # If no more data is received, break the loop
                        break
                    received_data += chunk
                    if received_data.endswith(b"\r\n"):  # Check if the received data ends with \r\n
                        rts = True
                        break
                except Exception as e:
                    print(f"[!EXCPT!] Error occurred during string read: '{str(e)}'")
        return rts,received_data.decode().rstrip("\r\n")

    def read_binary(self, timeout_ms: int, buffer_size: int) ->Tuple[bool,bytes]:
        rts = False
        received_data = b""
        if self.connected:        
            try:
                self.sock.settimeout(timeout_ms / 1000)  # Set the socket timeout in seconds
                received_data = b""
                if buffer_size >= 0:
                    exit_when_data = False
                else:
                    exit_when_data = True
                    buffer_size=-buffer_size
                while True:
                    data_chunk = self.sock.recv(buffer_size)
                    received_data += data_chunk
                    if exit_when_data or (len(received_data)==buffer_size):
                        rts = True
                        break          
                    buffer_size = buffer_size - len(data_chunk)

            except Exception as e:
                print(f"[!EXCPT!] Error occurred during binary read: '{str(e)}'")
        return rts,received_data

    def write_string(self,timeout_ms:int, message:str)->bool:
        rts = False
        if self.connected:
            try:
                self.sock.settimeout(timeout_ms / 1000)  # Set the socket timeout in seconds
                message_bytes = message.encode()
                self.sock.sendall(message_bytes)  # + b"\r\n")
                rts = True
            except Exception as e:
                print(f"[!EXCPT!] Error occurred during string write: '{str(e)}'")
        return rts
    
    def write_binary(self, timeout_ms: int, binary_data: bytes) -> bool:
        rts = False
        if self.connected:
            try:
                self.sock.settimeout(timeout_ms / 1000)  # Set the socket timeout in seconds
                self.sock.sendall(binary_data)
                rts = True
            except Exception as e:
                print(f"[!EXCPT!] Error occurred during binary write: '{str(e)}'")
        return rts    
    
    def disconnect(self)->bool:
        rts = False
        if self.connected:
            self.connected = False
            try:        
                self.sock.close()
                rts = True
            except Exception as e:
                print(f"[!EXCPT!] Error occurred during close: '{str(e)}'")                
        return rts   
    
class Bof_Ftp_Client:
    def __init__(self)->None:    
        self.ftp = ftplib.FTP()  #host="")
        self.ftp.set_debuglevel(1)     
        self.connected = False
        
    def connect(self, timeout_ms:int, endpoint:str, user:str, pw:str,  passive:bool)->Tuple[bool,int,str]:
        ip_address = Bof_Ip_Address(endpoint)
        rts, protocol, ip, port = ip_address.get_ip_endpoint_param()
        if rts:
            try:
                resp = self.ftp.connect(ip, port, timeout_ms/1000)  #welcome msg
                resp = self.ftp.login(user, pw) 
                self.ftp.set_pasv(passive)
                self.connected = True
            except Exception as e:
                rts=False
                resp = str(e)   
                self.connected = False
                print(f"[!EXCPT!] connect: {resp}")     
            sts, code = bofpy.BofPy.Bof_IsInteger(resp[:3],-1)   
        return rts,code,resp[4:]
    
    def is_connected(self)->bool: 
        return self.connected
    
    def quit(self)->Tuple[bool, int]:
        rts=True
        try:
            self.ftp.quit()
            resp=self.ftp.lastresp
        except Exception as e:
            rts=False
            resp = str(e)   
            print(f"[!EXCPT!] quit: {resp}")    
        sts, code = bofpy.BofPy.Bof_IsInteger(resp[:3],-1)   
        return rts,code,resp[4:]  
    
    def send_command(self, ftp_cmd:str)->Tuple[bool, int,str]:
        rts=True
        code=-1
        resp = "-1 "
        try:
            resp =  self.ftp.sendcmd(ftp_cmd)
        except Exception as e:
            rts=False
            resp=str(e)   
            print(f"[!EXCPT!] send_command: {resp}") 
        sts, code = bofpy.BofPy.Bof_IsInteger(resp[:3],-1)   
        return rts,code,resp[4:]
    
    def retr(self, ftp_cmd:str, callback, block_size_in_byte:int, data_storage)->Tuple[bool, int,str]:
        rts=True
        try:
            if data_storage==None:
                resp = self.ftp.retrbinary(ftp_cmd, callback, block_size_in_byte)
            else:
                resp = self.ftp.retrbinary(ftp_cmd, lambda data: (data_storage.write(data), callback(data)), block_size_in_byte)
        #except ftplib.error_proto as e:
        except Exception as e:
            rts=False
            resp = str(e)
            print(f"[!EXCPT!] retr: {resp}")   
        sts, code = bofpy.BofPy.Bof_IsInteger(resp[:3],-1)     
        return rts,code,resp[4:]
      
    def store(self, ftp_cmd:str, callback, block_size_in_byte:int, data_provider)->Tuple[bool, int,str]:
        rts=True
        try:
            resp = self.ftp.storbinary(ftp_cmd,data_provider,block_size_in_byte, callback)
        except Exception as e:
            rts=False
            resp = str(e)
            print(f"[!EXCPT!] store: {resp}")  
        sts, code = bofpy.BofPy.Bof_IsInteger(resp[:3],-1)   
        return rts,code,resp[4:]
     
    def list(self, dir)->Tuple[bool, int,str, List[str]]:
        rts=True
        list_line_collection = []
        try:
            self.ftp.retrlines("LIST " + dir , lambda line: list_line_collection.append(line))
            resp=self.ftp.lastresp
        except Exception as e:
            rts=False
            resp=str(e)   
            print(f"[!EXCPT!] list: {resp}")   
        sts, code = bofpy.BofPy.Bof_IsInteger(resp[:3],-1)           
        resp = f"    {len(list_line_collection)} entries"
        return rts,code,resp,list_line_collection
  