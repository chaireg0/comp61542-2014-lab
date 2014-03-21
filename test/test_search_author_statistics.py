import unittest
from os import path
from comp61542.database.database import Author, Publication
from comp61542.database import database
from comp61542.statistics import utils
from comp61542 import views
import comp61542

class TestSearchAuthorStatistics(unittest.TestCase):

    def setUp(self):
        auth1 = Author("Author1")
        auth2 = Author("Author2")
        auth3 = Author("Author3")
        auth4 = Author("Author4")
        
        self.pub1 = Publication(0, "Pub1", "2002", [0, 1, 2])
        self.pub2 = Publication(3, "Pub2", "1999", [3, 0, 2])
        self.pub3 = Publication(1, "Pub3", "2012", [0])

        directory, _ = path.split(__file__)
        data = "dblp_curated_sample.xml"
        comp61542.app.config['TESTING'] = True
        comp61542.app.config['DATASET'] = data
        comp61542.app.config['DATABASE'] = path.join(directory, "..", "data", data)
        
        db = database.Database()
        db.authors = [auth1, auth2, auth3, auth4]
        db.publications = [self.pub1, self.pub2, self.pub3]
        self.db = db
        comp61542.app.config['DATABASE'] = self.db
        self.app = comp61542.app.test_client()
        
    def test_search_author(self):
                
        pub_list = self.db.search_by_author("Author1")
        self.assertTrue(self.pub1 in pub_list and self.pub2 in pub_list and self.pub3 in pub_list)
        
        pub_list = self.db.search_by_author("Author3")
        self.assertTrue(self.pub1 in pub_list and self.pub2 in pub_list)

    def test_that_author_appears_n_times_as_first_author(self):
        n = self.db.get_times_as_first("Author1")
        self.assertEqual(n, 2)
        
        n = self.db.get_times_as_first("Author2")
        self.assertEqual(n, 0)
    
    def test_that_author_appears_n_times_as_last_author(self):
        n = self.db.get_times_as_last("Author1")
        self.assertEqual(n, 1)    
        
        n = self.db.get_times_as_last("Author2")
        self.assertEqual(n, 0) 
        
        n = self.db.get_times_as_last("Author3")
        self.assertEqual(n, 2) 

    def test_search_function_for_author(self):
        author_stats = self.db.get_author_stats("Author1")
        self.assertEqual(author_stats, [1, 1, 0, 1, 2, 1, 3, 3])
        
        author_stats = self.db.get_author_stats("Author2")
        self.assertEqual(author_stats, [1, 0, 0, 0, 0, 0, 1, 2])    
         
    def test_table_for_author_first_last_stats(self):
        times_appeared_first = self.db.get_times_as_first("Author1")
        times_appeared_last = self.db.get_times_as_last("Author1")
        author = {"name": "Author1", "first": times_appeared_first, "last": times_appeared_last}
        
        table_for_html_generation = utils.author_stats_fist_last(author)
        
        self.assertEquals(["Author1", "2", "1"], table_for_html_generation)
      
    def test_table_for_author_first_last_stats_with_header(self):
        times_appeared_first = self.db.get_times_as_first("Author1")
        times_appeared_last = self.db.get_times_as_last("Author1")
        author = {"name": "Author1", "first": times_appeared_first, "last": times_appeared_last}
        
        table_for_html_generation = utils.author_stats_fist_last_table(author)
        
        self.assertEqual(("Name", "Times appeared first", "Times appeared last"),\
                           table_for_html_generation[0])
        self.assertEquals([["Author1", "2", "1"]], table_for_html_generation[1])
