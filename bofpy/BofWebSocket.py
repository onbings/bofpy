import websocket
import threading
import time 
import json
import BofStd

from enum import Enum
from typing import Tuple
from urllib.parse import urlparse, parse_qs

class WebSocketClientState(Enum):
    INIT = 1
    OPEN  = 2
    ERROR = 3
    CLOSE = 4
    
class WebSocketClient():
    s_seq_id = 1  # This is a static variable
    
    def __init__(self, verbose, cb_open, cb_rx, cb_close, cb_error):
        self.url = None
        self.ws = None
        self.state= WebSocketClientState.INIT
        #websocket.enableTrace(verbose)
        self.cb_open=cb_open
        self.cb_rx=cb_rx
        self.cb_close=cb_close
        self.cb_error=cb_error
        self.wait_for_cmd_reply = False
        self.reply=None
        self.reply_id = 0
        self.client_thread = None
        self.connected = False
        
    def get_client_state(self):
        return self.state

    def send_message(self, message):
        print(f"Sending message: {message} if state {self.state} is equel to {WebSocketClientState.OPEN} and {self.wait_for_cmd_reply} is False")
        if self.state == WebSocketClientState.OPEN and  not self.wait_for_cmd_reply:
            self.ws.send(message)
            return True
        return False

    def send_command(self, timeout_in_ms:int, cmd:str)->Tuple[bool,str]:
        if self.state == WebSocketClientState.OPEN:
            start_time_in_ms = BofStd.Bof_GetMsTickCount()
            self.reply=None
            self.wait_for_cmd_reply = True
            self.reply_id = self.s_seq_id
            self.s_seq_id += 1 
            if self.s_seq_id == 0x100000000:
                self.s_seq_id = 1 
            if "?" in cmd:
                cmd += "&seq=" + str(self.reply_id)
            else:
                cmd += "?seq=" + str(self.reply_id) 
            #print(f"Send seq '{self.reply_id}' cmd '{cmd}'.")   
            self.ws.send(cmd)
            while self.state == WebSocketClientState.OPEN and self.wait_for_cmd_reply:
                if BofStd.Bof_ElapsedMsTime(start_time_in_ms) >= timeout_in_ms:
                    return False,None
                BofStd.Bof_MsSleep(1)      
            #print(f"Final check: state '{self.state}' wait '{self.wait_for_cmd_reply}' reply '{self.reply}'.")         
            if self.state == WebSocketClientState.OPEN and not self.wait_for_cmd_reply:
                try:
                    json_data = json.loads(self.reply)
                    if "protocolInfo" in json_data:
                        protocol_info = json_data["protocolInfo"]
                        #if cmd == protocol_info:
                        # Parse the URL
                        parsed_http_request = urlparse(protocol_info)
                        #Extract components
                        #scheme = parsed_http_request.scheme
                        #netloc = parsed_http_request.netloc
                        #path = parsed_http_request.path
                        query = parsed_http_request.query           
                        #Parse the query string into a dictionary
                        query_param = parse_qs(query)
                        # Get the value of the 'seq' parameter
                        seq_value = int(query_param.get("seq", [None])[0])
                        if self.reply_id==seq_value:
                            return True,self.reply
                        else:
                            print(f"ProtocolInfo seq of '{protocol_info}' ({seq_value}) is not equal to seq of '{cmd}' ({self.reply_id})")                           
                    else:
                        print(f"No 'protocolInfo' field found in the JSON data.")     
                except json.JSONDecodeError:
                    print(f"send_command: Invalid JSON format.")
                except Exception as e:
                    print(f"send_command: An error occurred: '{e}'")
        else:
           print(f"State '{self.state}' is not correct.")   
                
        self.wait_for_cmd_reply = False
        return False,None
            
    def _do_connect(self, url:str):
        # url = "ws://192.168.0.41:8080"  # Replace with your server's URL
        print(f"Thread starts")
        self.ws = websocket.WebSocketApp(url,
                                on_message=self.on_message,
                                on_error=self.on_error,
                                on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()
        print(f"Thread leaves")
        
    def ws_url(self)->str:
        return self.url
    
    def is_connected(self)->bool:
        return self.connected
    
    def connect(self, timeout_in_ms, url):
        # url = "ws://192.168.0.41:8080"  # Replace with your server's URL
        self.url = url
        self.client_thread = threading.Thread(target=self._do_connect, args=(url,))
        #self.client_thread = threading.Thread(target=self._do_connect, args=("ws://127.0.0.1:8080",))
        self.client_thread.start()
        start_time_in_ms = BofStd.Bof_GetMsTickCount()
        while self.state != WebSocketClientState.OPEN:
            if BofStd.Bof_ElapsedMsTime(start_time_in_ms) >= timeout_in_ms:
              return False
            BofStd.Bof_MsSleep(100)
        return True
    
    def disconnect(self):
        if self.ws:
            self.ws.close()
            self.ws = None
        if self.client_thread:
            self.client_thread.join()  # Wait for the thread to finish
            self.client_thread = None  # Reset the thread object
            
    def on_open(self, ws):
        print(f"Connection opened")
        # send_message(ws, "Hello, WebSocket!")
        self.state= WebSocketClientState.OPEN
        self.connected = True
        if self.cb_open != None:
           self.cb_open()
                    
    def on_message(self, ws, message):
        if self.wait_for_cmd_reply:
           self.reply=message
           #print(f"Received reply: {message}")
           self.wait_for_cmd_reply = False
        else:
           print(f"Received message: {message}")
           if self.cb_rx!= None:
              self.cb_rx(message)
        
    def on_close(self, ws, close_status_code, close_msg):
        print(f"Connection closed")
        self.state= WebSocketClientState.CLOSE
        self.reply=None
        self.wait_for_cmd_reply = True   
        self.connected = False     
        if self.cb_close != None:        
          self.cb_close(close_msg)
              
    def on_error(self, ws, error):
        print(f"Error: {error}")
        self.state= WebSocketClientState.ERROR
        if self.cb_error != None:        
          self.cb_error(error)