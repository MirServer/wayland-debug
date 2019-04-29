#!/usr/bin/python3

import unittest
import os
import sys

def discover_recursive(suit, path):
    for i in os.listdir(path):
        sub = path + os.path.sep + i
        if os.path.isdir(sub):
            if os.path.basename(sub) == 'test':
                suite.addTest(unittest.TestLoader().discover(sub))
            else:
                discover_recursive(suit, sub)

suite = unittest.TestSuite()
discover_recursive(suite, os.path.dirname(sys.argv[0]))
runner = unittest.TextTestRunner()
result = runner.run(suite)
exit(0 if result.wasSuccessful() else 1)
