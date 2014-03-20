'''
Created on 18 Mar 2014

author: vnicolao
'''

class Academic(object):
    """
    classdocs
    """


    def __init__(self, firstName, lastName):
        '''
        Constructor
        '''
        
        self.firstName = firstName
        self.lastName = lastName
        
        self.publications = {}
    
    def add_publication(self, year, publication):
        if year not in self.publications:
            self.publications[year] = []
        self.publications[year].append(publication)
        
    def average_pubs_per_year(self):
        counter = 0
        sum_of_publications = 0
        for key in self.publications:
            sum_of_publications += len(self.publications[key])
            counter += 1
        return sum_of_publications/float(counter)
