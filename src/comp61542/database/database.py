from comp61542.statistics import average, utils
import itertools
import numpy as np
from xml.sax import handler, make_parser, SAXException
from comp61542 import app

PublicationType = [
    "Conference Paper", "Journal", "Book", "Book Chapter"]

class Publication:
    CONFERENCE_PAPER = 0
    JOURNAL = 1
    BOOK = 2
    BOOK_CHAPTER = 3

    def __init__(self, pub_type, title, year, authors):
        self.pub_type = pub_type
        self.title = title
        if year:
            self.year = int(year)
        else:
            self.year = -1
        self.authors = authors
    
    def to_textlist(self):
        authors = ""
        for author in self.authors:
            authors += app.config["DATABASE"].authors[author].name + ", "
        authors = authors[0:len(authors)-2]
        return [PublicationType[self.pub_type], self.title, str(self.year), authors]

    

class Author:
    def __init__(self, name):
        self.name = name
        
    def total_papers(self):
        try:
            return self.conference_papers + self.journal_papers + self.books + self.book_chapters
        except:
            return 0
class Stat:
    STR = ["Mean", "Median", "Mode"]
    FUNC = [average.mean, average.median, average.mode]
    MEAN = 0
    MEDIAN = 1
    MODE = 2

class Database:

    def __init__(self):
        
        self.sorted_by_first_author = False
        self.sorted_by_year = False
        self.sorted_by_title = False
        self.sorted_by_type = False
        self.breadcrump = [{"name":"Home", "link":"/"}, None, None]
    
    def set_breadcrump(self, name, link, level=1):
        self.breadcrump[2] = None
        if level < 1:
            self.breadcrump[1] = None
        self.breadcrump[level] = {"name":name, "link":link}
        
        
    def read(self, filename):
        self.publications = []
        self.authors = []
        self.author_idx = {}
        self.min_year = None
        self.max_year = None


        handler = DocumentHandler(self)
        parser = make_parser()
        parser.setContentHandler(handler)
        infile = open(filename, "r")
        valid = True
        try:
            parser.parse(infile)
        except SAXException as e:
            valid = False
            print "Error reading file (" + e.getMessage() + ")"
        infile.close()

        for p in self.publications:
            if self.min_year == None or p.year < self.min_year:
                self.min_year = p.year
            if self.max_year == None or p.year > self.max_year:
                self.max_year = p.year

        return valid

    def get_all_authors(self):
        return self.author_idx.keys()

    def get_coauthor_data(self, start_year, end_year, pub_type):
        coauthors = {}
        for p in self.publications:
            if ((start_year == None or p.year >= start_year) and
                (end_year == None or p.year <= end_year) and
                (pub_type == 4 or pub_type == p.pub_type)):
                for a in p.authors:
                    for a2 in p.authors:
                        if a != a2:
                            try:
                                coauthors[a].add(a2)
                            except KeyError:
                                coauthors[a] = set([a2])
        def display(db, coauthors, author_id):
            return "%s (%d)" % (db.authors[author_id].name, len(coauthors[author_id]))

        header = ("Author", "Co-Authors")
        self.header_cache = header
        data = []
        for a in coauthors:
            data.append([ display(self, coauthors, a),
                ", ".join([
                    display(self, coauthors, ca) for ca in coauthors[a] ]) ])
        self.cache = data
        self.header_cache = header
        self.sorted_cache = [ False for i in range(0, len(header))]    
        return (header, data)

    def get_average_authors_per_publication(self, av):
        header = ("Conference Paper", "Journal", "Book", "Book Chapter", "All Publications")
        self.header_cache = header
        auth_per_pub = [[], [], [], []]

        for p in self.publications:
            auth_per_pub[p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [ func(auth_per_pub[i]) for i in np.arange(4) ] + [ func(list(itertools.chain(*auth_per_pub))) ]
        self.cache = data
        
        self.sorted_cache = [ False for i in range(0, len(header))]
        return (header, data)

    def get_average_publications_per_author(self, av):
        header = ("Conference Paper", "Journal", "Book", "Book Chapter", "All Publications")
        self.header_cache = header
        pub_per_auth = np.zeros((len(self.authors), 4))

        for p in self.publications:
            for a in p.authors:
                pub_per_auth[a, p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [ func(pub_per_auth[:, i]) for i in np.arange(4) ] + [ func(pub_per_auth.sum(axis=1)) ]
        self.cache = data
        
        self.sorted_cache = [ False for i in range(0, len(header))]
        return (header, data)

    def get_average_publications_in_a_year(self, av):
        header = ("Conference Paper",
            "Journal", "Book", "Book Chapter", "All Publications")
        self.header_cache = header
        ystats = np.zeros((int(self.max_year) - int(self.min_year) + 1, 4))

        for p in self.publications:
            ystats[p.year - self.min_year][p.pub_type] += 1

        func = Stat.FUNC[av]
        
        self.sorted_cache = [ False for i in range(0, len(header))]
        data = [ func(ystats[:, i]) for i in np.arange(4) ] + [ func(ystats.sum(axis=1)) ]
        self.cache = data
        return (header, data)

    def get_average_authors_in_a_year(self, av):
        header = ("Conference Paper",
            "Journal", "Book", "Book Chapter", "All Publications")
        self.header_cache = header
        yauth = [ [set(), set(), set(), set(), set()] for _ in range(int(self.min_year), int(self.max_year) + 1) ]

        for p in self.publications:
            for a in p.authors:
                yauth[p.year - self.min_year][p.pub_type].add(a)
                yauth[p.year - self.min_year][4].add(a)

        ystats = np.array([ [ len(S) for S in y ] for y in yauth ])

        func = Stat.FUNC[av]

        data = [ func(ystats[:, i]) for i in np.arange(5) ]
        self.cache = data
        self.sorted_cache = [ False for i in range(0, len(header))]
        return (header, data)

    def get_publication_summary_average(self, av):
        header = ("Details", "Conference Paper",
            "Journal", "Book", "Book Chapter", "All Publications")
        self.header_cache = header
        pub_per_auth = np.zeros((len(self.authors), 4))
        auth_per_pub = [[], [], [], []]

        for p in self.publications:
            auth_per_pub[p.pub_type].append(len(p.authors))
            for a in p.authors:
                pub_per_auth[a, p.pub_type] += 1

        name = Stat.STR[av]
        func = Stat.FUNC[av]

        data = [
            [name + " authors per publication"]
                + [ func(auth_per_pub[i]) for i in np.arange(4) ]
                + [ func(list(itertools.chain(*auth_per_pub))) ],
            [name + " publications per author"]
                + [ func(pub_per_auth[:, i]) for i in np.arange(4) ]
                + [ func(pub_per_auth.sum(axis=1)) ] ]
        
        self.cache = data
        self.sorted_cache = [ False for i in range(0, len(header))]
        return (header, data)

    def get_publication_summary(self):
        header = ("Details", "Conference Paper",
            "Journal", "Book", "Book Chapter", "Total")
        self.header_cache = header
        
        plist = [0, 0, 0, 0]
        alist = [set(), set(), set(), set()]

        for p in self.publications:
            plist[p.pub_type] += 1
            for a in p.authors:
                alist[p.pub_type].add(a)
        # create union of all authors
        ua = alist[0] | alist[1] | alist[2] | alist[3]

        data = [
            ["Number of publications"] + plist + [sum(plist)],
            ["Number of authors"] + [ len(a) for a in alist ] + [len(ua)] ]
        
        self.cache = data
        
        self.sorted_cache = [ False for i in range(0, len(header))]
        return (header, data)

    def sortPublicationsByYear(self):
        self.sorted_by_year = not self.sorted_by_year
        return sorted(self.publications, key=lambda pub: pub.year, reverse=not self.sorted_by_year) # sort by publication's year

    def sortPublicationsByTitle(self):
        self.sorted_by_title = not self.sorted_by_title
        return sorted(self.publications, key=lambda pub: pub.title, reverse=not self.sorted_by_title) # sort by publication's title
    
    def sortPublicationsByType(self):
        self.sorted_by_type = not self.sorted_by_type
        return sorted(self.publications, key=lambda pub: PublicationType[pub.pub_type],\
                      reverse=not self.sorted_by_type) # sort by publication's type


    def get_average_authors_per_publication_by_author(self, av):
        header = ("Author", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "All publications")

        self.header_cache = header

        astats = [ [[], [], [], []] for _ in range(len(self.authors)) ]
        for p in self.publications:
            for a in p.authors:
                astats[a][p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [ [self.authors[i].name]
            + [ func(L) for L in astats[i] ]
            + [ func(list(itertools.chain(*astats[i]))) ]
            for i in range(len(astats)) ]
        return (header, data)

    def sortPublicationsByFirstAuthors(self):
        self.sorted_by_first_author = not self.sorted_by_first_author
        return sorted(self.publications, key=lambda pub: self.authors[pub.authors[0]].name,\
                       reverse=not self.sorted_by_first_author) # sort by author's name


    def get_publications_by_author(self):
        header = ("Author", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "Total")

        self.header_cache = header

        astats = [ [0, 0, 0, 0] for _ in range(len(self.authors)) ]
        for p in self.publications:
            for a in p.authors:
                astats[a][p.pub_type] += 1

        data = [ [self.authors[i].name] + astats[i] + [sum(astats[i])]
            for i in range(len(astats)) ]
        self.cache = data
        self.sorted_cache = [ False for i in range(0, len(header))]
        return (header, data)

    
    def sort_cache_generic(self, field):
        if (self.header_cache[field] == "Author" or self.header_cache[field] == "Author Name" ):
            sorted_pubs = sorted(self.cache, key=lambda pub: utils.convertAuthorNameToList(pub[field]),\
                                  reverse = self.sorted_cache[field])
        else:
            
            index = None
            reverse = self.sorted_cache[field]
            if "Author" in self.header_cache:
                index = self.header_cache.index("Author")
            if not index == None:
                sorted_pubs = sorted(self.cache, key=lambda pub: utils.convertAuthorNameToList(pub[index]))    
                self.cache = sorted_pubs
           
            try:
                sorted_pubs = sorted(self.cache, key=lambda pub: int(pub[field]), reverse = reverse)
            except:
                sorted_pubs = sorted(self.cache, key=lambda pub: pub[field], reverse = reverse)
            
        self.cache = sorted_pubs
        
        self.sorted_cache[field] = not self.sorted_cache[field]
        
        return self.cache

    
    def get_average_authors_per_publication_by_year(self, av):
        header = ("Year", "Conference papers",
            "Journals", "Books",
            "Book chapers", "All publications")

        self.header_cache = header

        ystats = {}
        for p in self.publications:
            try:
                ystats[p.year][p.pub_type].append(len(p.authors))
            except KeyError:
                ystats[p.year] = [[], [], [], []]
                ystats[p.year][p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [ [y]
            + [ func(L) for L in ystats[y] ]
            + [ func(list(itertools.chain(*ystats[y]))) ]
            for y in ystats ]
        self.cache = data
        
        self.sorted_cache = [ False for i in range(0, len(header))]
        return (header, data)

    def get_publications_by_year(self):
        header = ("Year", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "Total")

        self.header_cache = header

        ystats = {}
        for p in self.publications:
            try:
                ystats[p.year][p.pub_type] += 1
            except KeyError:
                ystats[p.year] = [0, 0, 0, 0]
                ystats[p.year][p.pub_type] += 1

        data = [ [y] + ystats[y] + [sum(ystats[y])] for y in ystats ]
        self.cache = data
        
        self.sorted_cache = [ False for i in range(0, len(header))]
        return (header, data)

    def get_average_publications_per_author_by_year(self, av):
        header = ("Year", "Conference papers",
            "Journals", "Books",
            "Book chapers", "All publications")

        self.header_cache = header

        ystats = {}
        for p in self.publications:
            try:
                s = ystats[p.year]
            except KeyError:
                s = np.zeros((len(self.authors), 4))
                ystats[p.year] = s
            for a in p.authors:
                s[a][p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [ [y]
            + [ func(ystats[y][:, i]) for i in np.arange(4) ]
            + [ func(ystats[y].sum(axis=1)) ]
            for y in ystats ]
        self.cache = data
        
        self.sorted_cache = [ False for i in range(0, len(header))]
        return (header, data)

    def get_author_totals_by_year(self):
        header = ("Year", "Number of conference papers",
            "Number of journals", "Number of books",
            "Number of book chapers", "Total")

        self.header_cache = header

        ystats = {}
        for p in self.publications:
            try:
                s = ystats[p.year][p.pub_type]
            except KeyError:
                ystats[p.year] = [set(), set(), set(), set()]
                s = ystats[p.year][p.pub_type]
            for a in p.authors:
                s.add(a)
        data = [ [y] + [len(s) for s in ystats[y]] + [len(ystats[y][0] | ystats[y][1] | ystats[y][2] | ystats[y][3])]
            for y in ystats ]
        self.cache = data
        
        self.sorted_cache = [ False for i in range(0, len(header))]
        return (header, data)

    def get_publication_list(self):
        header = ("Type", "Title",
            "Year", "Authors")
        
        self.header_cache = header
        
        data = utils.table_from_pubs(self.publications)
        self.cache = data
        
        self.sorted_cache = [ False for i in range(0, len(header))]
        return (header, data)

    def add_publication(self, pub_type, title, year, authors):
        if year == None or len(authors) == 0:
            print "Warning: excluding publication due to missing information"
            print "    Publication type:", PublicationType[pub_type]
            print "    Title:", title
            print "    Year:", year
            print "    Authors:", ",".join(authors)
            return
        if title == None:
            print "Warning: adding publication with missing title [ %s %s (%s) ]" % (PublicationType[pub_type], year, ",".join(authors))
        idlist = []
        for a in authors:
            try:
                idlist.append(self.author_idx[a])
            except KeyError:
                a_id = len(self.authors)
                self.author_idx[a] = a_id
                idlist.append(a_id)
                self.authors.append(Author(a))
        self.publications.append(
            Publication(pub_type, title, year, idlist))
        if (len(self.publications) % 100000) == 0:
            print "Adding publication number %d (number of authors is %d)" % (len(self.publications), len(self.authors))

        if self.min_year == None or year < self.min_year:
            self.min_year = year
        if self.max_year == None or year > self.max_year:
            self.max_year = year

    def _get_collaborations(self, author_id, include_self):
        data = {}
        for p in self.publications:
            if author_id in p.authors:
                for a in p.authors:
                    try:
                        data[a] += 1
                    except KeyError:
                        data[a] = 1
        if not include_self:
            del data[author_id]
        return data

    def get_coauthor_details(self, name):
        author_id = self.author_idx[name]
        data = self._get_collaborations(author_id, True)
        
        return [ (self.authors[key].name, data[key])
            for key in data ]

    def get_network_data(self):
        na = len(self.authors)

        nodes = [ [self.authors[i].name, -1] for i in range(na) ]
        links = set()
        for a in range(na):
            collab = self._get_collaborations(a, False)
            nodes[a][1] = len(collab)
            for a2 in collab:
                if a < a2:
                    links.add((a, a2))
        return (nodes, links)

    
    def search_by_author(self, auth_name):
        pub_list = []
        authors = [ author.name for author in self.authors ]
        author_index = authors.index(auth_name)
        for p in self.publications:
            if author_index in p.authors:
                pub_list.append(p)
        return pub_list

    
    def get_times_as_first(self, auth_name, pub_type=4):
        pub_list = self.get_publications_by_type(auth_name, pub_type)
        author_index = self.author_idx[auth_name]
        counter = 0
        for p in pub_list:
            if p.authors[0] == author_index and len(p.authors) != 1:
                counter +=1
        return counter

    def get_times_as_last(self, auth_name, pub_type=4):
        pub_list = self.get_publications_by_type(auth_name, pub_type)
        authors = [ author.name for author in self.authors ]
        author_index = authors.index(auth_name)
        counter = 0
        for p in pub_list:
            if p.authors[-1] == author_index and len(p.authors) != 1:
                counter +=1
        return counter
    
    def get_times_as_sole(self, auth_name, pub_type=4):
        pub_list = self.get_sole_publications(auth_name, pub_type)
        return len(pub_list)

    def get_author_stats(self, auth_name):
        pub_list = self.search_by_author(auth_name)
        conf_counter = 0
        journal_counter = 0
        book_counter = 0
        bchapter_counter = 0
        for p in pub_list:
            if p.pub_type == 0:
                conf_counter += 1
            elif p.pub_type == 1:
                journal_counter += 1
            elif p.pub_type == 2:
                book_counter += 1
            elif p.pub_type == 3:
                bchapter_counter += 1
        
        coauthors = self._get_collaborations(self.author_idx[auth_name], False)
        
        first_counter = self.get_times_as_first(auth_name)
        last_counter = self.get_times_as_last(auth_name)
        sole_counter = self.get_times_as_sole(auth_name)
        return [conf_counter, journal_counter, book_counter, bchapter_counter, 
                first_counter, last_counter, sole_counter, len(pub_list), len(coauthors.keys())]

    
    def search_author(self, search_word):
        authors = []
        authors.extend(author for author in self.authors if (search_word.lower() in author.name.lower()))
        if len(authors) == 0:
            raise Exception()
        return sorted(authors, key=lambda author: author.name)

    def get_publications_by_type(self, auth_name, pub_type=4):
        pub_list = []
        all_pubs = self.search_by_author(auth_name)
        if (pub_type == 4):
            pub_list = all_pubs
            return pub_list
        else:
            for p in all_pubs:
                if p.pub_type==pub_type:
                    pub_list.append(p)
        return pub_list
    
    def get_sole_publications(self, auth_name, pub_type=4):
        pub_list = self.get_publications_by_type(auth_name, pub_type)
        sole_pub_list = []
        for p in pub_list:
            if len(p.authors) == 1:
                sole_pub_list.append(p)
        return sole_pub_list

    

    
    def get_all_authors_stats(self, pub_type=4):
        header = ("Author", "Number of first author",
            "Number of last author", "Number of sole author")
        self.header_cache = header
        
        auth_pub_list = []
        authors = [ author.name for author in self.authors ]
        for a in authors:
            auth_pub_list.append(self.get_author_stats_per_type(a, pub_type))
        self.cache = auth_pub_list
        self.sorted_cache = [ False for i in range(0, len(header))]
        
        return (header, auth_pub_list)

    def calculate(self, author_name):
        stats = self.get_author_stats(author_name)
        author = self.getAuthor(author_name)
        
        author.conference_papers = stats[0]
        author.journal_papers = stats[1]
        author.books = stats[2]
        author.book_chapters = stats[3]
        author.coauthors = stats[8]
        counter = 0
        author.first = {}
        author.last = {}
        author.sole = {}
        for pub_type in PublicationType:
            stats = self.get_author_stats_per_type(author_name, counter)
            counter += 1
            author.first[pub_type] = stats[1]
            author.last[pub_type] = stats[2]
            author.sole[pub_type] = stats[3]
        
        stats = self.get_author_stats_per_type(author_name)
        author.first["overall"] = stats[1]
        author.last["overall"] = stats[2]
        author.sole["overall"] = stats[3]
        
    def getAuthor(self, author_name):
        return self.authors[self.author_idx[author_name]]
        
    def get_author_stats_per_type(self, author_name, pub_type=4):            
        return [str(author_name), self.get_times_as_first(author_name, pub_type),
                self.get_times_as_last(author_name, pub_type), 
                self.get_times_as_sole(author_name, pub_type)]                

    def get_author_profile(self, author_name):
        self.calculate(author_name)
        author = self.getAuthor(author_name)
        tables = []
        table = {}
        table["rows"] = []
        table["title"] = "Number of publications" 
        table["header"] = []
        table["header"].extend(PublicationType)
        table["header"].append("Overall")
        table["rows"].append([author.conference_papers, author.journal_papers, author.books, author.book_chapters, author.total_papers()])
        tables.extend([table])
        
        table={}
        table["rows"] = []
        table["title"] = "Number of publications as first Author" 
        table["header"] = []
        table["header"].extend(PublicationType)
        table["header"].append("Overall")
        table["rows"].append([author.first[PublicationType[0]], author.first[PublicationType[1]],\
                               author.first[PublicationType[2]], author.first[PublicationType[3]],\
                                author.first["overall"]])
        
        tables.append(table)
        table = {}
        table["rows"] = []
        table["title"] = "Number of publications as last Author" 
        table["header"] = []
        table["header"].extend(PublicationType)
        table["header"].append("Overall")
        table["rows"].append([author.last[PublicationType[0]], author.last[PublicationType[1]],\
                               author.last[PublicationType[2]], author.last[PublicationType[3]],\
                                author.last["overall"]])
        
        tables.append(table)
        table = {}
        table["rows"] = []
        table["title"] = "Number of publications as sole Author" 
        table["header"] = []
        table["header"].extend(PublicationType)
        table["header"].append("Overall")
        table["rows"].append([author.sole[PublicationType[0]], author.sole[PublicationType[1]],\
                               author.sole[PublicationType[2]], author.sole[PublicationType[3]],\
                                author.sole["overall"]])
        tables.append(table)
        table={}
        table["rows"] = []
        table["title"] = "Coauthors" 
        table["header"] = ["Number of co-authors"]
        table["rows"].append([author.coauthors])
        
        tables.append(table)
        
        return tables

    def bfs(self, authorA, authorB):
        if authorA == authorB:
            return 0
        Q=[]
        Q.append(authorA)
        print Q, 'queue'
        distance = -1
        visited = [ False for i in range(0, len(self.authors))]
        token = -2
        
        Q.append(token)
        while len(Q) > 0 and (not (len(Q) == 1 and token in Q)):
            
            
            if Q[0] == authorB:
                return distance
            if Q[0] == token:
                distance+=1
                Q.append(token)

            if not Q[0] == token and not visited[Q[0]]:
                visited[Q[0]] = True
                
                adjacency_list = [ author for author in range(0, len(self.authors))\
                                   if self.degrees_of_separation_graph[Q[0]][author] == 1]
                print adjacency_list, Q[0]
                for coauthor in adjacency_list:
                    if coauthor != Q[0]:
                        Q.append(coauthor)
                    
            Q.pop(0)
            print 'new queue', Q    
        return -1
                    

    def generate_degrees_of_separation_graph(self):
        self.degrees_of_separation_graph = [ [0 for i in range(0, len(self.authors))] for j in range(0, len(self.authors)) ]
        for pub in self.publications:
            for authorA in pub.authors:
                for authorB in pub.authors:
                    self.degrees_of_separation_graph[authorA][authorB] = 1
        
        
        
class DocumentHandler(handler.ContentHandler):
    TITLE_TAGS = [ "sub", "sup", "i", "tt", "ref" ]
    PUB_TYPE = {
        "inproceedings":Publication.CONFERENCE_PAPER,
        "article":Publication.JOURNAL,
        "book":Publication.BOOK,
        "incollection":Publication.BOOK_CHAPTER }

    def __init__(self, db):
        self.tag = None
        self.chrs = ""
        self.clearData()
        self.db = db

    def clearData(self):
        self.pub_type = None
        self.authors = []
        self.year = None
        self.title = None

    def startDocument(self):
        pass

    def endDocument(self):
        pass

    def startElement(self, name, attrs):
        if name in self.TITLE_TAGS:
            return
        if name in DocumentHandler.PUB_TYPE.keys():
            self.pub_type = DocumentHandler.PUB_TYPE[name]
        self.tag = name
        self.chrs = ""

    def endElement(self, name):
        if self.pub_type == None:
            return
        if name in self.TITLE_TAGS:
            return
        d = self.chrs.strip()
        if self.tag == "author":
            self.authors.append(d)
        elif self.tag == "title":
            self.title = d
        elif self.tag == "year":
            self.year = int(d)
        elif name in DocumentHandler.PUB_TYPE.keys():
            self.db.add_publication(
                self.pub_type,
                self.title,
                self.year,
                self.authors)
            self.clearData()
        self.tag = None
        self.chrs = ""

    def characters(self, chrs):
        if self.pub_type != None:
            self.chrs += chrs
