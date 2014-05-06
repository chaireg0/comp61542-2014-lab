from comp61542 import app
from database import database
from flask import (render_template, request)
from comp61542.statistics import utils
import json
from flask.json import jsonify
def format_data(data):
    fmt = "%.2f"
    result = []
    for item in data:
        if type(item) is list:
            result.append(", ".join([ (fmt % i).rstrip('0').rstrip('.') for i in item ]))
        else:
            result.append((fmt % item).rstrip('0').rstrip('.'))
    return result

@app.route("/averages")
def showAverages():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    db.set_breadcrump(name="Averages", link= "/averages")
    
    args = {"dataset":dataset, "id":"averages"}
    args['title'] = "Averaged Data"
    db.title_cache = args['title']
    tables = []
    headers = ["Average", "Conference Paper", "Journal", "Book", "Book Chapter", "All Publications"]
    averages = [ database.Stat.MEAN, database.Stat.MEDIAN, database.Stat.MODE ]
    tables.append({
        "id":1,
        "title":"Average Authors per Publication",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_authors_per_publication(i)[1])
                for i in averages ] })
    tables.append({
        "id":2,
        "title":"Average Publications per Author",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_publications_per_author(i)[1])
                for i in averages ] })
    tables.append({
        "id":3,
        "title":"Average Publications in a Year",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_publications_in_a_year(i)[1])
                for i in averages ] })
    tables.append({
        "id":4,
        "title":"Average Authors in a Year",
        "header":headers,
        "rows":[
                [ database.Stat.STR[i] ]
                + format_data(db.get_average_authors_in_a_year(i)[1])
                for i in averages ] })

    args['tables'] = tables
    args["breadcrump"] = db.breadcrump
    return render_template("averages.html", args=args)



@app.route("/coauthors")
def showCoAuthors():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    db.set_breadcrump(name="coauthors", link= "/coauthors")
    
    PUB_TYPES = ["Conference Papers", "Journals", "Books", "Book Chapters", "All Publications"]
    args = {"dataset":dataset, "id":"coauthors"}
    args["title"] = "Co-Authors"
    
    db.title_cache = args['title']
    start_year = db.min_year
    if "start_year" in request.args:
        start_year = int(request.args.get("start_year"))

    end_year = db.max_year
    if "end_year" in request.args:
        end_year = int(request.args.get("end_year"))

    pub_type = 4
    if "pub_type" in request.args:
        pub_type = int(request.args.get("pub_type"))

    args["data"] = db.get_coauthor_data(start_year, end_year, pub_type)
    args["start_year"] = start_year
    args["end_year"] = end_year
    args["pub_type"] = pub_type
    args["min_year"] = db.min_year
    args["max_year"] = db.max_year
    args["start_year"] = start_year
    args["end_year"] = end_year
    args["pub_str"] = PUB_TYPES[pub_type]
    db.args_cache = args
    db.title_cache = args['title']
    args["breadcrump"] = db.breadcrump
    return render_template("coauthors.html", args=args)

@app.route("/firstLastSoleType")
def showAuthorFirstLastSolePerType():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    db.set_breadcrump(name="Author order", link="/firstLastSoleType")
    PUB_TYPES = ["Conference Papers", "Journals", "Books", "Book Chapters", "All Publications"]
    args = {"dataset":dataset, "id":"firstLastSoleType"}
    args["title"] = "Author First/Last/Sole per publication type"
    
    db.title_cache = args['title']
    
    pub_type = 4
    if "pub_type" in request.args:
        pub_type = int(request.args.get("pub_type"))

    args["data"] = db.get_all_authors_stats(pub_type)
    args["pub_type"] = pub_type
    args["pub_str"] = PUB_TYPES[pub_type]
    db.args_cache = args
    db.title_cache = args['title']
    return render_template('authorFirstLastSolePerType.html', args=args)

@app.route("/")
def showStatisticsMenu():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    db.set_breadcrump(name="Home", link= "/", level=0)
    
    args = {"dataset":dataset}
    return render_template('statistics.html', args=args)

@app.route("/statisticsdetails/<status>")
def showPublicationSummary(status):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":status}
    if (status == "publication_summary"):
        args["title"] = "Publication Summary"
        args["data"] = db.get_publication_summary()
        
    if (status == "publication_author"):
        args["title"] = "Author Publication"
        args["data"] = db.get_publications_by_author()

    if (status == "publication_year"):
        args["title"] = "Publication by Year"
        args["data"] = db.get_publications_by_year()

    if (status == "author_year"):
        args["title"] = "Author by Year"
        args["data"] = db.get_author_totals_by_year()
    
    if (status == "author_first_last_sole"):
        args["title"] = "Author statistics"
        args["data"] = db.get_all_authors_stats()
        
    if (status == "author_first_last_sole_per_type"):
        args["title"] = "Author statistics per type"
        args["data"] = db.get_all_authors_stats(3)
        
    db.title_cache = args['title']
    db.set_breadcrump(name=args["title"], link="/statisticsdetails/" + status )
    args["breadcrump"] = db.breadcrump
    return render_template('statistics_details.html', args=args)

@app.route("/authorsDegreeOfSeparation")
def displayDegreeOfSeparation():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    db.set_breadcrump(name="Degree of separation", link="/authorsDegreeOfSeparation")
    args = {"dataset":dataset}
    args["title"] = "Degree Of Separation"
#    author_names = [ author.name for author in db.authors ]
#    authors = [ author.name for author in db.authors ]
    author_A = " - "
    author_B = " - "
    degree_of_separation = " - "
    args["graph_js"] = None
    db.cache_graph = None
    if "authorA" in request.args and "authorB" in request.args:
        author_A = request.args.get("authorA")
        author_B = request.args.get("authorB")
        db.generate_degrees_of_separation_graph()
        degree_of_separation=db.bfs(db.author_idx[author_A], db.author_idx[author_B])
<<<<<<< HEAD
        shortestPathGraph=db.dfs(db.author_idx[author_A], db.author_idx[author_B], degree_of_separation+1)
        shortestPathDict=db.convertIDGraphToNames(shortestPathGraph)
        args["shortest_path"]=shortestPathDict
=======
>>>>>>> vasilis/master
        url = "/authorsDegreeOfSeparation?authorA=" + author_A + "&authorB=" + author_B
        db.set_breadcrump(name=author_A + " | " + author_B, link=url, level=2)
        graph = db.dfs(db.author_idx[author_A], db.author_idx[author_B], degree_of_separation+1)
        db.cache_graph = graph
    if degree_of_separation==-1:
        degree_of_separation="X"
<<<<<<< HEAD
        args["shortest_path"]="X"
    else:
        args["degree_of_separation"] = degree_of_separation
        args["shortest_path"]=shortestPathDict
=======
>>>>>>> vasilis/master
    args["columns"] = ("Author A", "Author B", "Degree of Separation")
    author_names = db.author_idx.keys()
    author_names.sort()
    args["author_names"] = author_names
    args["authorA"] = author_A
    args["authorB"] = author_B
    args["breadcrump"] = db.breadcrump
    
    
    return render_template("authorsDegreeOfSeparation.html", args=args)

@app.route("/graph/<authora>/<authorb>")
def getGraph(authora, authorb):
    db = app.config['DATABASE']
    db.generate_degrees_of_separation_graph()
    degree_of_separation=db.bfs(db.author_idx[authora], db.author_idx[authorb])
    graph = db.dfs(db.author_idx[authora], db.author_idx[authorb], degree_of_separation+1)
    return jsonify(db.convertIDGraphToNames(graph))

@app.route("/publications/<sortby>")
def displayPublications(sortby):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":sortby}
    sortby = sortby.lower()
    args["title"] = "Publications"  
        
    if (sortby == "year"):
        db.publications = db.sortPublicationsByYear()
    elif (sortby == "authors"):
        db.publications = db.sortPublicationsByFirstAuthors()
    elif (sortby == "title"):
        db.publications = db.sortPublicationsByTitle()
    elif sortby == "type":
        db.publications = db.sortPublicationsByType()
    else:
        db.publications = db.sortPublicationsByTitle()
        
    args["data"] = db.get_publication_list()
    db.title_cache = args['title']
    
    return render_template('publications.html', args=args)

@app.route("/author/firstlast")
def displayAuthorFirstLastSoleStats():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    try:
        authorname = request.args.get('fname')
        args = {"dataset":dataset, "id":authorname}
        first = db.get_times_as_first(authorname)
        last = db.get_times_as_last(authorname)
        author = {'name':authorname, 'first':first, 'last':last}
        args['title'] = "Author First/Last/Sole stats"
        db.title_cache = args['title']
        
        args['data'] = utils.author_stats_fist_last_table(author)
        db.cache = args['data'][1]
        db.header_cache = args['data'][0]
        db.sorted_cache = [ False for i in range(0, len(db.header_cache))]
        return render_template('author_first_last.html', args=args)
    except:
        return firstlast()
   
@app.route("/stats/<field>")
def sortByField(field):
    db = app.config['DATABASE']
    dataset = app.config['DATASET']
    field = int(field)
    args = {"dataset":dataset, "id":field}
    db.sort_cache_generic(field)
    db.set_breadcrump(name="Order by field: " + db.header_cache[field], link="/stats/"+str(field), level=2)
    args['data'] = (db.header_cache, db.cache)
    try:
        args['title'] = db.title_cache
    except:
        pass #no title cached
    args["breadcrump"] = db.breadcrump
    return render_template('statistics_details.html', args = args)

@app.route("/stats/coauthors/<field>")
def sortByCoauthorField(field):
    db = app.config['DATABASE']
    field = int(field)
    db.sort_cache_generic(field)
    
    args = db.args_cache    
    args['data'] = (db.header_cache, db.cache)
    try:
        args['title'] = db.title_cache
    except:
        pass #no title cached
    
        
    db.title_cache = args['title']

    
    return render_template('coauthors.html', args = args)

@app.route("/stats/authors/<field>")
def sortStatsField(field):
    db = app.config['DATABASE']
    field = int(field)
    db.sort_cache_generic(field)
    
    args = db.args_cache    
    args['data'] = (db.header_cache, db.cache)
    try:
        args['title'] = db.title_cache
    except:
        pass #no title cached
    
        
    db.title_cache = args['title']

    args["breadcrump"] = db.breadcrump    
    return render_template('authorFirstLastSolePerType.html', args = args)


    
def displayAuthorStats(authorname, args):
    db = app.config['DATABASE']
    
    try:
        author_stats = db.get_author_stats(authorname)
        author = {'name':authorname, "Conference": author_stats[0], "Journal": author_stats[1], "Book": author_stats[2],
                      "Book Chapter": author_stats[3], "first": author_stats[4], "last": author_stats[5], "sole": author_stats[6],
                      "Total": author_stats[7], "coauthors": author_stats[8]}
        args['data'] = utils.author_all_stats_table(author)
        args['title'] = str(authorname)
        db.title_cache = args['title']
        return render_template('search_for_author.html', args=args)
    except:
        return searchPage()


def displayAuthorListWithHyperlinks(authors, args):
    db = app.config['DATABASE']
    
    args['title'] = "Search result"
    db.title_cache = args['title']
    header = ["Author Name"]
    data = [[author.name] for author in authors]
    args['data'] = (header, data)
    db.cache = data
    db.header_cache = header
    db.sorted_cache = [False for i in range(0, len(header))]
    return render_template('author_list.html', args=args)

@app.route("/authors/search/author")
def searchAuthorByKeyword():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    authorname = request.args.get('fname')
    
    args = {"dataset":dataset, "id":authorname}
    try:
        authors = db.search_author(authorname)
    except:
        return searchPage()
    if (len(authors) == 1):
        author_name = authors[0].name
        return getAuthorProfile(author_name)
    else:
        return displayAuthorListWithHyperlinks(authors, args)
    
    
    
@app.route('/authors/search')
def searchPage():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    db.set_breadcrump(name="Author search", link="/authors/search")
    args = {"dataset":dataset, "id":'search'}
    args['title'] = 'Search'
    db.title_cache = args['title']
    args['data'] = '/authors/search/author'
    
    args['author_search_type'] = 'Search author'
    args['author_search_type_link'] = '/authors/search'
    args["breadcrump"] = db.breadcrump
    return render_template('search.html', args=args)

@app.route("/author")
def firstlast():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":'search'}
    args['title'] = 'Search'
    db.title_cache = args['title']
    args['data'] = '/author/firstlast'
    
    args['author_search_type'] = 'Number of times author appeared first or last'
    args['author_search_type_link'] = '/author'
    return render_template('search.html', args=args)

def showAllAuthorsFirstLastSole():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    PUB_TYPES = ["Author", "Journals", "Books", "Book Chapters", "All Publications"]
    args = {"dataset":dataset, "id":"coauthors"}
    args["title"] = "Co-Authors"
    
    db.title_cache = args['title']
    start_year = db.min_year
    if "start_year" in request.args:
        start_year = int(request.args.get("start_year"))

    end_year = db.max_year
    if "end_year" in request.args:
        end_year = int(request.args.get("end_year"))

    pub_type = 4
    if "pub_type" in request.args:
        pub_type = int(request.args.get("pub_type"))

    args["data"] = db.get_coauthor_data(start_year, end_year, pub_type)
    args["start_year"] = start_year
    args["end_year"] = end_year
    args["pub_type"] = pub_type
    args["min_year"] = db.min_year
    args["max_year"] = db.max_year
    args["start_year"] = start_year
    args["end_year"] = end_year
    args["pub_str"] = PUB_TYPES[pub_type]
    db.args_cache = args
    db.title_cache = args['title']
    return render_template("coauthors.html", args=args)


@app.route("/profile/<author>")
def getAuthorProfile(author):
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    db.set_breadcrump(name=author, link="/profile/"+author, level=2)
    args = {"dataset":dataset, "id":"coauthors"}
    args['title'] = author + " profile"
    
    tables = db.get_author_profile(author)
    args["tables"] = tables
    args["breadcrump"] = db.breadcrump
    return render_template('author_profile.html',args=args )