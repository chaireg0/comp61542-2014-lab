'''
Created on 28 Apr 2014

@author: vnicolao
'''
import unittest
import comp61542.views as views
from os import path
import comp61542
from comp61542.database import database

class Test(unittest.TestCase):


    def setUp(self):
        directory, _ = path.split(__file__)
        data = "dblp_curated_sample.xml"
        comp61542.app.config['TESTING'] = True
        comp61542.app.config['DATASET'] = data
        self.db = database.Database()
        self.db.read(path.join(directory, "..", "data", data))
        comp61542.app.config['DATABASE'] = self.db
        self.app = comp61542.app.test_client()
        
    def tearDown(self):
        pass


    def test_breadcrump_level_1(self):
        
        self.app.get("/averages")
        self.assertEqual(self.db.breadcrump[0]["name"], "Home")
        self.assertEqual(self.db.breadcrump[0]["link"], "/")
        self.assertEqual(self.db.breadcrump[1]["name"], "Averages")
        self.assertEqual(self.db.breadcrump[1]["link"], "/averages")
        
        self.app.get("/coauthors")
        self.assertEqual(self.db.breadcrump[0]["name"], "Home")
        self.assertEqual(self.db.breadcrump[0]["link"], "/")
        self.assertEqual(self.db.breadcrump[1]["name"], "coauthors")
        self.assertEqual(self.db.breadcrump[1]["link"], "/coauthors")
        
        self.app.get("/")
        self.assertEqual(self.db.breadcrump[0]["name"], "Home")
        self.assertEqual(self.db.breadcrump[0]["link"], "/")
        self.assertEqual(self.db.breadcrump[1], None)        
        
    def test_breadcrump_level_2(self):
        self.app.get("/authors/search")
        self.assertEqual(self.db.breadcrump[1]["name"], "Author search")
        self.assertEqual(self.db.breadcrump[1]["link"], "/authors/search")
        someauthorname = self.db.authors[0].name
        self.app.get("/authors/search/author?fname="+someauthorname)
        self.assertEqual(self.db.breadcrump[1]["name"], "Author search")
        self.assertEqual(self.db.breadcrump[1]["link"], "/authors/search")
        self.assertEqual(self.db.breadcrump[2]["name"], someauthorname)
        self.assertEqual(self.db.breadcrump[2]["link"], "/profile/" + someauthorname)
        
        someotherauthorname = self.db.authors[1].name
        self.app.get("/authorsDegreeOfSeparation")
        self.assertEqual(self.db.breadcrump[1]["name"], "Degree of separation")
        self.assertEqual(self.db.breadcrump[1]["link"], "/authorsDegreeOfSeparation")
        self.assertEqual(self.db.breadcrump[2], None)
        url = "/authorsDegreeOfSeparation?authorA=" + someauthorname + "&authorB=" + someotherauthorname
        self.app.get(url)
        self.assertEqual(self.db.breadcrump[1]["name"], "Degree of separation")
        self.assertEqual(self.db.breadcrump[1]["link"], "/authorsDegreeOfSeparation")
        self.assertEqual(self.db.breadcrump[2]["name"], someauthorname + " | " + someotherauthorname )
        self.assertEqual(self.db.breadcrump[2]["link"], url)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_breadcrump_level_1']
    unittest.main()