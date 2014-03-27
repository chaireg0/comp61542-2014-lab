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
        data = "dblp_curated_sample.xml"
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
        self.assertEqual(72, author.conference_papers)
        self.assertEqual(4, author.book_chapters)
        self.assertEqual(62, author.journal_papers)
        self.assertEqual(1, author.books)
        self.assertEquals(139, author.total_papers())


    def test_that_db_calculates_number_of_publications_for_authors_as_first_author(self):
        self.db.calculate("Alon Y. Halevy")
        author = self.db.getAuthor("Alon Y. Halevy")
        PublicationType = [
    "Conference Paper", "Journal", "Book", "Book Chapter"]
        self.assertEqual(1, author.first[PublicationType[0]])
        self.assertEqual(0, author.first[PublicationType[3]])
        self.assertEqual(1, author.first[PublicationType[1]])
        self.assertEqual(0, author.first[PublicationType[2]])
        self.assertEqual(2, author.first["overall"])

    def test_that_db_calculates_number_of_publications_for_authors_as_last_author(self):
        self.db.calculate("Alon Y. Halevy")
        author = self.db.getAuthor("Alon Y. Halevy")
        PublicationType = [
    "Conference Paper", "Journal", "Book", "Book Chapter"]
        self.assertEqual(0, author.last[PublicationType[0]])
        self.assertEqual(0, author.last[PublicationType[3]])
        self.assertEqual(2, author.last[PublicationType[1]])
        self.assertEqual(0, author.last[PublicationType[2]])
        self.assertEqual(2, author.first["overall"])
    
    def test_that_db_calculates_number_of_publications_for_authors_as_sole_author(self):
        self.db.calculate("Alon Y. Halevy")
        author = self.db.getAuthor("Alon Y. Halevy")
        PublicationType = [
    "Conference Paper", "Journal", "Book", "Book Chapter"]
        self.assertEqual(10, author.sole[PublicationType[0]])
        self.assertEqual(2, author.sole[PublicationType[3]])
        self.assertEqual(7, author.sole[PublicationType[1]])
        self.assertEqual(0, author.sole[PublicationType[2]])
        self.assertEqual(19, author.sole["overall"])
    
    def test_that_db_calculates_number_of_coauthors_for_author(self):
        self.db.calculate("Alon Y. Halevy")
        author = self.db.getAuthor("Alon Y. Halevy")
        self.assertEquals(195, author.coauthors)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_that_']
    unittest.main()