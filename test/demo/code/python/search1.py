import json
import sys
import xapian
import support

def search(dbpath, querystring, offset=0, pagesize=10):
	#offset - defines starting point within result set
	#pagesize - defines number of records to retrive
	db = xapian.Database(dbpath)
	queryparser = xapian.QueryParser()
	### choose a language
	queryparser.set_stemmer(xapian.Stem("en"))
	queryparser.set_stemming_strategy(queryparser.STEM_SOME)

	queryparser.add_prefix("title", "S")
	queryparser.add_prefix("description", "XD")

	query = queryparser.parse_query(querystring)

	enquire = xapian.Enquire(db)
	#####Schema Test
	#bm = xapian.BM25Weight(1.0, 0.0, 1.0, 0.5, 0.3)
	#enquire.set_weighting_scheme(bm)

	enquire.set_query(query)

	matches = []
	for  match in enquire.get_mset(offset, pagesize):
		fields = json.loads(match.document.get_data())
		print(u"%(rank)i: #%(docid)3.3i %(title)s"%{
			'rank' : match.rank + 1,
			'docid' : match.docid,
			'title' : fields.get('TITLE', u''),
 			})
		matches.append(match.docid)

	support.log_matches(querystring, offset, pagesize, matches)

	### END of function


if len(sys.argv) < 3:
	print("Usage: %s DBPATH QUERYTERM..." % sys.argv[0])
	sys.exit(1)

search(dbpath = sys.argv[1], querystring = " ".join(sys.argv[2:]))