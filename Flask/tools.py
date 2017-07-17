#echo_server.py
import json
import sys
import xapian
import support
from server_format import str_parser

def select_weight(option):
	if option == 0:
		bm = xapian.BM25Weight(1.0, 0.0, 1.0, 0.5, 0.3)
	elif option == 1:
		bm = xapian.BoolWeight()
	elif option == 2:
		bm = xapian.BB2Weight(1.0)
	elif option == 3:
		bm = xapian.BM25PlusWeight(1.0, 0, 1.0, 0.5, 0.5, 1.0)
	elif option == 4:
		bm = 
	elif option == 5:
		bm = 
	elif option == 6:
		bm = 
	elif option == 7:
		bm = 
	elif option == 8:
		bm = 
	elif option == 9:
		bm = 
	elif option == 10:
		bm = 
	elif option == 11:
		bm = 
	elif option == 12:
		bm = 
	elif option == 13:
		bm = 
	elif option == 14:
		bm = 
	elif option == 15:
		bm = 

	return bm

#End of the funcion 

def search(dbpath, querystring, offset=0, pagesize=10, option=0):
	# offset - defines starting point within result set
	# pagesize - defines number of records to retrive
	db = xapian.Database(dbpath)
	queryparser = xapian.QueryParser()

	# choose a language
	queryparser.set_stemmer(xapian.Stem("en"))
	queryparser.set_stemming_strategy(queryparser.STEM_SOME)

	queryparser.add_prefix("title", "S")
	queryparser.add_prefix("description", "XD")

	query = queryparser.parse_query(querystring)

	enquire = xapian.Enquire(db)

	#select different weighting schema
	bm = select_weight(option)
	enquire.set_weighting_scheme(bm)

	enquire.set_query(query)

	matches = []
	ret = ""
	for  match in enquire.get_mset(offset, pagesize):
		fields = json.loads(match.document.get_data())
		tmp = u"%(rank)i: #%(docid)3.3i %(title)s"%{
			'rank' : match.rank + 1,
			'docid' : match.docid,
			'title' : fields.get('TITLE', u''),
			}
		ret += tmp
 		ret += '\n'
		matches.append(match.docid)
	support.log_matches(querystring, offset, pagesize, matches)
	return ret

### END of function