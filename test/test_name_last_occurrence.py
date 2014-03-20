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
        
        self.assertEquals([pub3, pub1, pub2], sortedpublist, "pub3 should come first, then pub1, then pub2. However, the result is " + str(sortedpublist))
        
    def testSortByYear(self):
        pub1 = Publication("", "", 2008, "")
        pub2 = Publication("", "", 1993, "")
        pub3 = Publication("", "", 1999, "")
        
        publist = [pub1, pub2, pub3]
        
        sortedpublist = utils.sortPublicationsByYear(publist)
        
        self.assertEquals([pub2, pub3, pub1], sortedpublist, "pub2 should come first, then pub3, then pub1. However, the result is " + str(sortedpublist))

    def testSortByTitle(self):
        pub1 = Publication("", "Putin's love with Tzar", "", "")
        pub2 = Publication("", "High-tech weapon", "", "")
        pub3 = Publication("", "Nuclear fission", "", "")
        
        publist = [pub1, pub2, pub3]
        
        sortedpublist = utils.sortPublicationsByTitle(publist)
        
        self.assertEquals([pub2, pub3, pub1], sortedpublist, "pub2 should come first, then pub3, then pub1. However, the result is " + str(sortedpublist))
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()