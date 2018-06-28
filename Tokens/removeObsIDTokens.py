import sys
if not 'couchdb' in sys.modules:
        import couchdb
from couchdb import Server
from couchdb.design import ViewDefinition

# python removeTokens.py [obsID] [db_name] [username] [pwd]
# - updated by JBR OONK (ASTRON/LEIDEN) DEC 2015
"""
   Connect to the server with [username] [pwd]
   Delete the documents in the [db_name] couchdb database:
"""

def deleteDocs(db, OBSID):
     #v=db.view("Monitor/done")
     v=db.view("Observations/"+OBSID)
     for x in v:
         document = db[x['key']]
         db.delete(document)
