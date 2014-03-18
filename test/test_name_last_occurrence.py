'''
Created on 18 Mar 2014

@author: user
'''
import unittest


from comp61542.objects import academic
from comp61542.objects.academic import Academic
from comp61542.database import database
from comp61542.database.database import Publication

from comp61542.statistics import utils


class Test(unittest.TestCase):



    def testSortByFirstAuthor(self):
        pub1 = Publication("", "", "", ["Joe Bloggs", "Harry Potter", "Lady Gaga", "John Keane"])
        pub2 = Publication("", "", "", ["John Sargeant", "Joe Robinson", "Justin Bieber"])
        pub3 = Publication("", "", "", ["Aristotle", "Alexander the Great"])
        
        publist = [pub1, pub2, pub3]
        
        sortedpublist = utils.sortPublicationsByFirstAuthors(publist)
        
        self.assertEquals([pub3, pub1, pub2], sortedpublist, "pub3 should come first, then pub2, then pub1 instead is " + str(sortedpublist))
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()