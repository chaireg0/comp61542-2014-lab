'''
Created on 18 Mar 2014

@author: user
'''

def sortPublicationsByFirstAuthors (publist):
    return sorted(publist, key=lambda pub: pub.authors[0]) # sort by author's name


def sortPublicationsByYear(publist):
    return sorted(publist, key=lambda pub: pub.year) # sort by publication's year

def sortPublicationsByTitle(publist):
    return sorted(publist, key=lambda pub: pub.title) # sort by publication's title