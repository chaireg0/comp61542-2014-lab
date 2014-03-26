'''
Created on 26 Mar 2014

@author: vnicolao
'''
import unittest
from comp61542.statistics import utils

class Test(unittest.TestCase):


    def testConvertingAuthorNameToListWhichMatches(self):
        authorName = "George V. Chairepetis"
        author_parts = ["Chairepetis", "George", "V."]
        self.assertEqual(author_parts, utils.convertAuthorNameToList(authorName))


    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()