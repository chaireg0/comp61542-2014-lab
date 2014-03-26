from comp61542 import app
from database import database
from flask import (render_template, request)
from comp61542.statistics import utils
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
    return render_template("averages.html", args=args)

@app.route("/coauthors")
def showCoAuthors():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
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
    return render_template("coauthors.html", args=args)

@app.route("/")
def showStatisticsMenu():
    dataset = app.config['DATASET']
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
    db.title_cache = args['title']
    
    return render_template('statistics_details.html', args=args)

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
def displayAuthorFirstLastStats():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    try:
        authorname = request.args.get('fname')
        args = {"dataset":dataset, "id":authorname}
        first = db.get_times_as_first(authorname)
        last = db.get_times_as_last(authorname)
        author = {'name':authorname, 'first':first, 'last':last}
        args['title'] = "Author First/Last stats"
        db.title_cache = args['title']
        
        args['data'] = utils.author_stats_fist_last_table(author)
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
    args['data'] = (db.header_cache, db.cache)
    try:
        args['title'] = db.title_cache
    except:
        pass #no title cached
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
    
def displayAuthorStats(authorname, args):
    db = app.config['DATABASE']
    
    try:
        author_stats = db.get_author_stats(authorname)
        author = {'name':authorname, "Conference": author_stats[0], "Journal": author_stats[1], "Book": author_stats[2],
                      "Book Chapter": author_stats[3], "first": author_stats[4], "last": author_stats[5],
                      "Total": author_stats[6], "coauthors": author_stats[7]}
        args['data'] = utils.author_all_stats_table(author)
        args['title'] = str(authorname)
        db.title_cache = args['title']
        return render_template('search_for_author.html', args=args)
    except:
        return searchPage()


def displayAuthorListWithHyperlinks(authors, args):
    db = app.config['DATABASE']
    
    args['title'] = "Search result"
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
    authors = db.search_author(authorname)
    
    if (len(authors) == 1):
        author_name = authors[0].name
        return displayAuthorStats(author_name, args)
    else:
        return displayAuthorListWithHyperlinks(authors, args)
    
    
    
@app.route('/authors/search')
def searchPage():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":'search'}
    args['title'] = 'Search'
    db.title_cache = args['title']
    args['data'] = '/authors/search/author'
    return render_template('search.html', args=args)

@app.route("/author")
def firstlast():
    dataset = app.config['DATASET']
    db = app.config['DATABASE']
    args = {"dataset":dataset, "id":'search'}
    args['title'] = 'Search'
    db.title_cache = args['title']
    args['data'] = '/author/firstlast'
    return render_template('search.html', args=args)
