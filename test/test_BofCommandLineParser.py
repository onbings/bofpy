import sys
import os
# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import argparse
from unittest.mock import patch

#from ..bofpy.BofCommandLineParser import (  
from bofpy.BofCommandLineParser import (                                                                                
    Bof_Cli_Check
)
#from ..bofpy.BofSocket import (       
from bofpy.BofSocket import (                               
    Bof_Ip_Address
)
class TestBofCommandLineParser(unittest.TestCase):
# The @patch('sys.argv', ['script_name', '--your', 'arguments']) decorator is used in conjunction
# with the unittest.mock.patch module in Python. 
# It is a way to temporarily replace the value of sys.argv for the duration of a test case.
    @patch('sys.argv', ['unit_test', '--ip', 'tcp://1.2.3.4:5', '--verbose'])
    def test_Bof_Cli_Check(self):
        cli_parser = argparse.ArgumentParser(description="This script is used to communicate with iot")
        ip_address = Bof_Ip_Address("")
        requiredArguments = cli_parser.add_argument_group("Mandatory arguments")
        requiredArguments.add_argument("--ip", dest="ip", help="The ip address of iot 'tcp://ip:port'", type=ip_address.parse_ip_endpoint, required=True)
        cli_parser.set_defaults(verbose=False)
        cli_parser.add_argument("--verbose", dest="verbose", action="store_true", help="Activate verbose mode.")
        args = Bof_Cli_Check("Unit Test", cli_parser)
        self.assertEqual(args.ip[0], True)
        self.assertEqual(args.ip[1], 'tcp')
        self.assertEqual(args.ip[2], '1.2.3.4')
        self.assertEqual(args.ip[3], 5)
        self.assertEqual(args.verbose, True)
if __name__ == '__main__':
    unittest.main()
