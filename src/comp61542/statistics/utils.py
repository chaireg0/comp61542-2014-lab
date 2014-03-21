'''
Created on 18 Mar 2014

@author: user
'''




def table_from_pubs(pubs):
    pubs_table = []
    for pub in pubs:
        pubs_table.append(pub.to_textlist())

    return pubs_table

def author_stats_fist_last(author):
    return [author['name'], str(author['first']), str(author['last'])]

def author_stats_fist_last_table(author):
    header = ("Name", "Times appeared first", "Times appeared last")
    return (header, [author_stats_fist_last(author)])

