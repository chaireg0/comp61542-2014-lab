'''
Created on 27 Mar 2014

@author: vnicolao
'''
import unittest
from os import path

from comp61542.database.database import Publication, Database, Author

from comp61542.statistics import utils
import comp61542

class TestAuthorStats(unittest.TestCase):

    def setUp(self):
        directory, _ = path.split(__file__)
        data = "dblp_2000_2005_114_papers.xml"
        comp61542.app.config['TESTING'] = True
        comp61542.app.config['DATASET'] = data
        db = Database()
        db.read(path.join(directory, "..", "data", data))
        comp61542.app.config['DATABASE'] = db
        
        self.app = comp61542.app.test_client()
        self.db = db

    def test_that_db_calculates_number_of_publications_for_authors(self):
        self.db.calculate("Roberto Elli")
        author = self.db.getAuthor("Roberto Elli")
        self.assertEquals(author.conference_papers, 1)
        self.assertEquals(0, author.journal_papers)
        self.assertEquals(0, author.book_chapters)
        self.assertEquals(0, author.books)
        self.assertEquals(1, author.total_papers())

        self.db.calculate("Alon Y. Halevy")
        author = self.db.getAuthor("Alon Y. Halevy")
        self.assertEquals(author.conference_papers, 39)
        self.assertEquals(31, author.journal_papers)
        self.assertEquals(1, author.book_chapters)
        self.assertEquals(0, author.books)
        self.assertEquals(71, author.total_papers())


    def test_that_db_calculates_number_of_publications_for_authors_as_first_author(self):
        self.db.calculate("Alon Y. Halevy")
        author = self.db.getAuthor("Alon Y. Halevy")
        
        self.assertEqual(3, author.first["conference"])
        self.assertEqual(1, author.first["book_chapter"])
        self.assertEqual(0, author.first["journal"])
        self.assertEqual(0, author.first["book"])
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_that_']
    unittest.main()