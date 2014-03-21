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


def author_all_stats(author):
    return [author['name'], str(author['Conference']), str(author['Journal']),
            str(author['Book']), str(author['Book Chapter']), str(author['first']),
            str(author['last']), str(author['Total']), str(author['coauthors'])]


def author_all_stats_table(author1, author2):
    header = ("Name", "Conference Papers", "Journal", "Book", "Book Chapters",
              "No. of first author", "No. of last author", "Total Publications",
              "Co-authors")
    return (header, [author_all_stats(author1), author_all_stats(author2)])


