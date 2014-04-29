'''
Created on 28 Apr 2014

@author: vnicolao
'''
import unittest
import xmlrpclib
import comp61542
from os import path
from comp61542.database import database

class Test(unittest.TestCase):

    def setUp(self):
        directory, _ = path.split(__file__)
        data = "dblp_curated_separations.xml"
        comp61542.app.config['TESTING'] = True
        comp61542.app.config['DATASET'] = data
        self.db = database.Database()
        self.db.read(path.join(directory, "..", "data", data))
        comp61542.app.config['DATABASE'] = self.db

    def test_graph_construction(self):
        # Create an object to represent our server.
        server_url = 'http://127.0.0.1:20738/RPC2'
        server = xmlrpclib.Server(server_url)
        G = server.ubigraph
        
        G.clear()
        vertices = []
        edges = []
        self.db.generate_degrees_of_separation_graph()
        print len(self.db.authors)
        for i in range(0, len(self.db.authors)):
            vertices.append(G.new_vertex())
            G.set_vertex_attribute(vertices[i], "label", self.db.authors[i].name)
        for i in range(0, len(self.db.authors)):
            for j in range(0, len(self.db.authors)):
                if (i != j and self.db.degrees_of_separation_graph[i][j] == 1):
                    edges.append(G.new_edge(vertices[i],vertices[j]))
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()