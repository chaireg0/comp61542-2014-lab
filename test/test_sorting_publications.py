'''
Created on 18 Mar 2014

@author: user
'''
import unittest
from os import path

from comp61542.database.database import Publication, Database, Author

from comp61542.statistics import utils
from comp61542 import views
import comp61542
class Test(unittest.TestCase):

    def setUp(self):
        directory, _ = path.split(__file__)
        data = "dblp_curated_sample.xml"
        comp61542.app.config['TESTING'] = True
        comp61542.app.config['DATASET'] = data
        db = Database()
        db.read(path.join(directory, "..", "data", data))
        comp61542.app.config['DATABASE'] = db
        
        self.app = comp61542.app.test_client()


    def testSortByFirstAuthor(self):
        
        authors = ["Joe Bloggs", "Harry Potter", "Lady Gaga",\
                    "John Keane", "John Sargeant", "Joe Robinson", "Justin Bieber", "Aristotle", "Alexander the Great"]
        db = comp61542.app.config["DATABASE"]
        
        db.authors= [Author(authors[0]), Author(authors[1]), Author(authors[2]), Author(authors[3])]
        for i in range(4, len(authors)):
            db.authors.append(Author(authors[i]))
            
        pub1 = Publication("", "", "", [0, 1, 2, 3])
        pub2 = Publication("", "", "", [4, 5, 6])
        pub3 = Publication("", "", "", [7, 8])
        
        
        publist = [pub1, pub2, pub3]
        db.publications = publist
        sortedpublist = db.sortPublicationsByFirstAuthors()
        
        self.assertEquals([pub3, pub1, pub2], sortedpublist)
    
        
    def testSortByYear(self):
        pub1 = Publication("", "", 2008, "")
        pub2 = Publication("", "", 1993, "")
        pub3 = Publication("", "", 1999, "")
        
        publist = [pub1, pub2, pub3]
        
        db = comp61542.app.config["DATABASE"]
        db.publications = publist
        sortedpublist = db.sortPublicationsByYear()
        
        self.assertEquals([pub2, pub3, pub1], sortedpublist,\
                           "pub2 should come first, then pub3, then pub1. However, the result is " + str(sortedpublist))

    def testSortByTitle(self):
        pub1 = Publication("", "Putin's love with Tzar", "", "")
        pub2 = Publication("", "High-tech weapon", "", "")
        pub3 = Publication("", "Nuclear fission", "", "")
        
        publist = [pub1, pub2, pub3]
        
        db = comp61542.app.config["DATABASE"]
        db.publications = publist
        sortedpublist = db.sortPublicationsByTitle()
        
        self.assertEquals([pub2, pub3, pub1], sortedpublist,\
                           "pub2 should come first, then pub3, then pub1. However, the result is " + str(sortedpublist))
    
    def test_pub_to_textlist(self):
        
        pub1 = Publication(0, "Hello2", 2008, [1])
        pub2 = Publication(0, "Hello0", 1993, [1, 2, 3])
        pub3 = Publication(0, "Hello1", 1999, [1, 4])
        db = comp61542.app.config["DATABASE"]
        db.authors = [Author("S"), Author("Author1"), Author("Author2"), Author("Author3"), Author("Author4")]
        db.publications = [pub1, pub2, pub3]
        self.assertEquals(["Conference Paper", "Hello2", "2008", "Author1"], pub1.to_textlist())
        self.assertEquals(["Conference Paper", "Hello0", "1993", "Author1, Author2, Author3"], pub2.to_textlist())
        self.assertEquals(["Conference Paper", "Hello1", "1999", "Author1, Author4"], pub3.to_textlist())
    
    def test_table_of_list_of_publications(self):
        pub1 = Publication(0, "Hello2", 2008, [1])
        pub2 = Publication(0, "Hello0", 1993, [1, 2, 3])
        pub3 = Publication(0, "Hello1", 1999, [1, 4])
        db = comp61542.app.config["DATABASE"]
        db.authors = [Author("S"), Author("Author1"), Author("Author2"), Author("Author3"), Author("Author4")]
        db.publications = [pub1, pub2, pub3]
        
        pub_table = utils.table_from_pubs([pub1, pub2, pub3])
        
        self.assertEquals([["Conference Paper", "Hello2", "2008", "Author1"],\
                       ["Conference Paper", "Hello0", "1993", "Author1, Author2, Author3"],\
                         ["Conference Paper", "Hello1", "1999", "Author1, Author4"]], pub_table)
        
    def test_html_generation(self):
        comp61542.app.config['TESTING'] = True
        
        db = comp61542.app.config['DATABASE']
        
        self.app = comp61542.app.test_client()
        
        html = db.get_publication_list()
        
        self.assertTrue(len(html) > 0)
    
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()