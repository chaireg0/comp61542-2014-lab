'''
Created on 18 Mar 2014

@author: user
'''




def table_from_pubs(pubs):
    pubs_table = []
    for pub in pubs:
        pubs_table.append(pub.to_textlist())

    return pubs_table