import sys
import os
# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
import socket
import ftplib
from unittest.mock import patch
from unittest.mock import Mock
from io import StringIO
from typing import List

#from ..bofpy.BofSocket import (  
from bofpy.BofSocket import (                                                           
    Bof_Ip_Address,
    Bof_Ftp_Socket,
    Bof_Ftp_Client
)
class TestBofIpAddress(unittest.TestCase):

    def test_parse_ip_endpoint(self):
        ip_address = Bof_Ip_Address("http://127.0.0.1:8080")
        self.assertEqual(ip_address.parse_ip_endpoint("http://127.0.0.1:8080"), (True, "http", "127.0.0.1", 8080))

    def test_build_ip_endpoint(self):
        ip_address = Bof_Ip_Address("http://127.0.0.1:8080")
        self.assertEqual(ip_address.to_string(), "http://127.0.0.1:8080")

    def test_to_string(self):
        ip_address = Bof_Ip_Address("http://127.0.0.1:8080")
        self.assertEqual(ip_address.to_string(), "http://127.0.0.1:8080")

class TestBofFtpSocket(unittest.TestCase):
# The @patch('socket.socket') decorator is used in the unit test to temporarily replace the socket.socket 
# class with a mock object during the execution of the test. 
# The @patch('ftplib.FTP') decorator is used in the unit test to temporarily replace the ftplib.
# FTP class with a mock object during the execution of the test. 
    @patch('socket.socket')
    def test_connect_tcp_successful(self, mock_socket):
        ftp_socket = Bof_Ftp_Socket()
        mock_socket.return_value.connect.return_value = None
        self.assertTrue(ftp_socket.connect("tcp://127.0.0.1:21"))

    @patch('socket.socket')
    def test_connect_udp_successful(self, mock_socket):
        ftp_socket = Bof_Ftp_Socket()
        mock_socket.return_value.bind.return_value = None
        self.assertTrue(ftp_socket.connect("udp://127.0.0.1:21"))

    @patch('socket.socket')
    def test_connect_tcp_failure(self, mock_socket):
        ftp_socket = Bof_Ftp_Socket()
        mock_socket.return_value.connect.side_effect = socket.error("Connection error")
        self.assertFalse(ftp_socket.connect("tcp://127.0.0.1:21"))

    # Add more tests for read_string, read_binary, write_string, write_binary, disconnect

class TestBofFtpClient(unittest.TestCase):

    @patch('ftplib.FTP')
    def test_connect_successful(self, mock_ftp):
        ftp_client = Bof_Ftp_Client()
        mock_ftp.return_value.login.return_value = "230 User logged in."
        sts,code,resp = ftp_client.connect(1000, "ftp://127.0.0.1:21", "user", "password", True)
        self.assertTrue(sts)
        self.assertEqual(code,230)
        self.assertEqual(resp,"User logged in.")
        
    @patch('ftplib.FTP')
    def test_connect_failure(self, mock_ftp):
        ftp_client = Bof_Ftp_Client()
        mock_ftp.return_value.login.side_effect = ftplib.error_perm("530 Login incorrect.")
        sts,code,resp = ftp_client.connect(1000, "ftp://127.0.0.1:21", "user", "password", True)
        self.assertFalse(sts)
        self.assertEqual(code,530)
        self.assertEqual(resp,"Login incorrect.")

    @patch('ftplib.FTP')
    def test_is_connected(self, mock_ftp):
        ftp_client = Bof_Ftp_Client()
        self.assertFalse(ftp_client.is_connected())
        ftp_client.connected = True
        self.assertTrue(ftp_client.is_connected())

    @patch('ftplib.FTP')
    def test_quit_successful(self, mock_ftp):
        ftp_client = Bof_Ftp_Client()
        mock_ftp.return_value.quit.return_value = "221 Goodbye."
        sts, code, resp = ftp_client.quit()
        self.assertTrue(sts)
        #self.assertEqual(code, 221)
        #self.assertEqual(resp, "Goodbye.")

    @patch('ftplib.FTP')
    def test_quit_failure(self, mock_ftp):
        ftp_client = Bof_Ftp_Client()
        mock_ftp.return_value.quit.side_effect = ftplib.error_reply("500 Syntax error.")
        sts, code, resp = ftp_client.quit()
        self.assertFalse(sts)
        self.assertEqual(code, 500)
        self.assertEqual(resp, "Syntax error.")

    @patch('ftplib.FTP')
    def test_send_command_successful(self, mock_ftp):
        ftp_client = Bof_Ftp_Client()
        mock_ftp.return_value.sendcmd.return_value = "200 OK."
        sts, code, resp = ftp_client.send_command("SOME_CMD")
        self.assertTrue(sts)
        self.assertEqual(code, 200)
        self.assertEqual(resp, "OK.")

    @patch('ftplib.FTP')
    def test_send_command_failure(self, mock_ftp):
        ftp_client = Bof_Ftp_Client()
        mock_ftp.return_value.sendcmd.side_effect = ftplib.error_reply("500 Syntax error.")
        sts, code, resp = ftp_client.send_command("INVALID_CMD")
        self.assertFalse(sts)
        self.assertEqual(code, 500)
        self.assertEqual(resp, "Syntax error.")

    @patch('ftplib.FTP')
    def test_retr_successful(self, mock_ftp):
        ftp_client = Bof_Ftp_Client()
        mock_callback = Mock()
        mock_ftp.return_value.retrbinary.return_value = "226 Transfer complete."
        sts, code, resp = ftp_client.retr("RETR_CMD", mock_callback, 1024, None)
        self.assertTrue(sts)
        self.assertEqual(code, 226)
        self.assertEqual(resp, "Transfer complete.")

    @patch('ftplib.FTP')
    def test_retr_failure(self, mock_ftp):
        ftp_client = Bof_Ftp_Client()
        mock_callback = Mock()
        mock_ftp.return_value.retrbinary.side_effect = ftplib.error_reply("550 File not found.")
        sts, code, resp = ftp_client.retr("INVALID_CMD", mock_callback, 1024, None)
        self.assertFalse(sts)
        self.assertEqual(code, 550)
        self.assertEqual(resp, "File not found.")

    @patch('ftplib.FTP')
    def test_store_successful(self, mock_ftp):
        ftp_client = Bof_Ftp_Client()
        mock_callback = Mock()
        mock_data_provider = Mock()
        mock_ftp.return_value.storbinary.return_value = "226 Transfer complete."
        sts, code, resp = ftp_client.store("STOR_CMD", mock_callback, 1024, mock_data_provider)
        self.assertTrue(sts)
        self.assertEqual(code, 226)
        self.assertEqual(resp, "Transfer complete.")

    @patch('ftplib.FTP')
    def test_store_failure(self, mock_ftp):
        ftp_client = Bof_Ftp_Client()
        mock_callback = Mock()
        mock_data_provider = Mock()
        mock_ftp.return_value.storbinary.side_effect = ftplib.error_reply("550 Permission denied.")
        sts, code, resp = ftp_client.store("STOR_CMD", mock_callback, 1024, mock_data_provider)
        self.assertFalse(sts)
        self.assertEqual(code, 550)
        self.assertEqual(resp, "Permission denied.")

if __name__ == '__main__':
    unittest.main()
