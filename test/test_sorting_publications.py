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
        self.db = db

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
    
        sortedpublist = db.sortPublicationsByFirstAuthors()
        self.assertEqual([pub2, pub1, pub3], sortedpublist) #next call should sort in descending order
        
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
        
        sortedpublist = db.sortPublicationsByYear()
        self.assertEquals([pub1, pub3, pub2], sortedpublist)

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
    
        sortedpublist = db.sortPublicationsByTitle()
        self.assertEquals([pub1, pub3, pub2], sortedpublist)
    
    def testSortByType(self):
        pub1 = Publication(0, "", "", "")
        pub2 = Publication(1, "", "", "")
        pub3 = Publication(2, "", "", "")
        
        publist = [pub1, pub2, pub3]
        
        db = comp61542.app.config["DATABASE"]
        db.publications = publist
        sortedpublist = db.sortPublicationsByType()
        
        self.assertEquals([pub3, pub1, pub2], sortedpublist)
    
        sortedpublist = db.sortPublicationsByType()
        self.assertEqual([pub2, pub1, pub3], sortedpublist)
        
        
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
        
    
    def test_that_database_caches_publications_after_a_get_pubs_by_author_call(self):
        self.db.get_publications_by_author()
        self.assertIsNotNone(self.db.cache)
    
    def test_that_database_sets_sorted_boolean_array_value_for_pubs_by_author_as_false(self):
        self.db.get_publications_by_author()
        self.assertIsNotNone(self.db.sorted_cache)
        
        for value in self.db.sorted_cache:
            self.assertFalse(value)
            
    def test_that_pubs_by_author_can_be_sorted_using_first_field(self):
        self.db.get_publications_by_author()
        self.db.sort_cache_generic(0)
        for index in range(0, len(self.db.cache) - 1):
            self.assertTrue(self.db.cache[index] <= self.db.cache[index + 1],\
                            self.db.cache[index][0] + "<=" + self.db.cache[index + 1][0])

    def test_that_pubs_by_author_can_be_sorted_using_n_field(self):
        self.db.get_publications_by_author()
        for i in range(0, len(self.db.cache[0])):
            self.db.sort_cache_generic(i)
            for index in range(0, len(self.db.cache) - 1):
                valueA = self.db.cache[index][i]
                valueB = self.db.cache[index + 1][i]
                try:
                    valueA = int(valueA)
                    valueB = int(valueB)
                except:
                    print "Warning:", valueA, valueB
                    pass
                
                self.assertTrue(valueA <= valueB,\
                            str(self.db.cache[index][i]) + "<="\
                             + str(self.db.cache[index + 1][i]))
            
    
    def generic_sort(self, method):
        method()
        for i in range(0, len(self.db.cache[0])):
            self.db.sort_cache_generic(i)
            for index in range(0, len(self.db.cache) - 1):
                valueA = self.db.cache[index][i]
                valueB = self.db.cache[index + 1][i]
                try:
                    valueA = int(valueA)
                    valueB = int(valueB)
                except:
                    print "Warning:", valueA, valueB
                    pass
                
                self.assertTrue(valueA <= valueB,\
                            str(self.db.cache[index][i]) + "<="\
                             + str(self.db.cache[index + 1][i]))
        
        
    def test_that_database_caches_publication_summary(self):
        self.db.get_publication_summary()
        self.assertIsNotNone(self.db.cache)
        
    
    def test_generic_sort_for_publication_summary(self):
        self.generic_sort(self.db.get_publication_summary)
    
    def test_that_database_caches_publication_by_year(self):
        self.db.get_publications_by_year()
        self.assertIsNotNone(self.db.cache)

    def test_generic_sort_for_publications_by_year(self):
        self.generic_sort(self.db.get_publications_by_year)
        
    def test_that_database_caches_totals_publications_per_author(self):
        self.db.get_author_totals_by_year()
        self.assertIsNotNone(self.db.cache)
        
    def test_generic_sort_for_average_publications_per_author(self):
        self.generic_sort(self.db.get_author_totals_by_year)
        
    
    def test_that_sorting_parameters_are_updated_after_field_sort(self):
        self.generic_sort(self.db.get_publication_summary)
        for field_sort in self.db.sorted_cache:
            self.assertTrue(field_sort)
        self.generic_sort(self.db.get_author_totals_by_year)
        for field_sort in self.db.sorted_cache:
            self.assertTrue(field_sort)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()