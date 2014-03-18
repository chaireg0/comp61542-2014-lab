'''
Created on 18 Mar 2014

@author: user
'''

def sortPublicationsByFirstAuthors (publist):
    return sorted(publist, key=lambda pub: pub.authors[0]) # sort by author's name