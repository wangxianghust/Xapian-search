import sys
import xapian

### Start of example
def delete_docs(dbpath,identifiers):
	db = xapian.WritableDatabase(dbpath, xapian.DB_OPEN)

	for identifier in identifiers:
		idterm = u'Q' + identifier
		db.delete_document(idterm)
### End of example code

if len(sys.argv) < 3:
	print("Usage: %s DBPATH..." % sys.argv[0])
	sys.exit(1)

delete_docs(dbpath = sys.argv[1], identifiers = sys.argv[2:])