#echo_server.py
import socket

import json
import sys
import xapian
import support
from format import str_parser

#database path
db_path = 'db'

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
	enquire.set_query(query)

	matches = []
	ret = ""
	for  match in enquire.get_mset(offset, pagesize):
		fields = json.loads(match.document.get_data())
		print(u"%(rank)i: #%(docid)3.3i %(title)s"%{
			'rank' : match.rank + 1,
			'docid' : match.docid,
			'title' : fields.get('TITLE', u''),
 			})
		tmp = u"%(rank)i: #%(docid)3.3i %(title)s"%{
			'rank' : match.rank + 1,
			'docid' : match.docid,
			'title' : fields.get('TITLE', u''),
 			}
 		ret += tmp
 		ret += '\n '
		matches.append(match.docid)
	support.log_matches(querystring, offset, pagesize, matches)
	return ret

	### END of function

	

host = ''
port = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

s.listen(1)

conn, addr = s.accept()

print('Connected by', addr)

while True:
    #data is a string received from socket.
    data = conn.recv(1024)
    data = data.decode()
    if not data:break
    #data = '%s%s' % (data, ' handled by server')
    data = str_parser(data)
    tmp = search(db_path, querystring = data)
    #ret = "\n".join(tmp)
    conn.sendall(tmp.encode())
conn.close()