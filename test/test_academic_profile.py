from os import path
import unittest
import comp61542.objects
from comp61542.objects import academic
from comp61542.objects.academic import Academic
from comp61542.objects.publication import Publication

class TestAcademicProfile(unittest.TestCase):

    
    def test_that_academic_has_a_correct_publications_per_year_average(self):
        academic = Academic('FirstName', 'LastName')
        
        counter = 5
        for i in range(0, 5):
            for j in range(0, counter):
                academic.add_publication(1980+i, Publication("Title" + str(i) + str(j)))
            counter -= 1
            if (counter == 0):
                counter = 5
        self.assertEqual(3, academic.average_pubs_per_year())
        
    
        
if __name__ == '__main__':
    unittest.main()
