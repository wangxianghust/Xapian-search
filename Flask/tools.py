#echo_server.py
import json
import sys
import xapian
import support
from server_format import str_parser

def select_weight(option):
	if option == 0:
		bm = xapian.BB2Weight(1.0)		
	elif option == 1:
		bm = xapian.BM25PlusWeight(1.0, 0, 1.0, 0.5, 0.5, 1.0)
	elif option == 2:
		bm = xapian.BM25Weight(1.0, 0.0, 1.0, 0.5, 0.3)
	elif option == 3:		
		bm = xapian.BoolWeight()
	elif option == 4:
		bm = xapian.CoordWeight()
	elif option == 5:
		bm = xapian.DLHWeight()  #maybe some problem
	elif option == 6:
		bm = xapian.DPHWeight()
	elif option == 7:
		bm = xapian.IfB2Weight(1)
	elif  option == 8:
		bm = xapian.IneB2Weight(1)
	elif option == 9:
		bm = xapian.InL2Weight(1)
	elif option == 10:
		bm = xapian.LMWeight(0.0, 1, -1.0, -1.0)  #the second parameter is TWO_STAGE_SMOOTHING
	elif option == 11:
		bm = xapian.PL2PlusWeight(1, 0.8)
	elif option == 12:
		bm = xapian.PL2Weight(1)
	elif option == 13:
		bm = xapian.TfIdfWeight("ntn")
	elif option == 14:
		bm = xapian.TradWeight(1.0)

	return bm

#End of the funcion 

def search(dbpath, querystring, option=0, offset=0, pagesize=10):
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