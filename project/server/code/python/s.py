#echo_server.py

import socket
import select
import threading
import json
import sys
import xapian
import support
from format import str_parser

HOST = '127.0.0.1'
PORT = 8080
ADDR = (HOST, PORT)
BUF_SIZE = 1024
THREAD_NUM = 0
# database path
DB_PATH = 'db'

def search(dbpath, querystring, offset=0, pagesize=10):
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

def process_request(request, addr):
	while 1:
		data = request.recv(BUF_SIZE)
		if not data:
			break
		data = str_parser(data)
		tmp = search(DB_PATH, querystring = data)
		request.sendall(tmp)
	request.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.bind(ADDR)
server.listen(1)

while 1:
	# data is a string received from socket.
	r,w,e = select.select([server],[],[],0.5)
	if server in r:
		conn, addr = server.accept()
		THREAD_NUM += 1
		print('Connected by', addr)
		t = threading.Thread(target = process_request,
							name = 'server process thread '+str(THREAD_NUM),
							args = (conn, addr))
		t.start()