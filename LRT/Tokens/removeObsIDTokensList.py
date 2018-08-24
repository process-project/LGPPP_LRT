import sys
import couchdb
from couchdb import Server
from couchdb.design import ViewDefinition

# python removeTokens.py [obsID] [db_name] [username] [pwd]
# - updated by JBR OONK (ASTRON/LEIDEN) DEC 2015
"""
   Connect to the server with [username] [pwd]
   Delete the documents in the [db_name] couchdb database:
"""

def deleteDoc(db):

     # CREATE LIST
     OBSID = sys.argv[1]
     tokens = []

     #read each file in the "datasets/[OBSID]" directory
     subbandPath = 'datasets' + '/' + OBSID + '/' + 'subbandlist' #path to file with subbands
     srmPath     = 'datasets' + '/' + OBSID + '/' + 'srmlist' #path to file with SURL input

     # for each subband create one token
     with open(subbandPath) as f1:
        for line in f1:
           subband_num = line.strip('\n')
           #print subband_num
           #tab_sap=subband_num.split('_')[0]
           #print tab_sap
           #tab_tab=subband_num.split('_')[1]
           #print tab_tab
           tk_name='token_' + OBSID + '_' + str(subband_num)+'v1.5'
           #print tk_name
           tokens.append(tk_name)
     print(tokens)

     # DELETE LISTED TOKENS
     #v=db.view("Monitor/done")
     v=db.view("Observations/"+sys.argv[1])
     #v=db.view("Observations/"+sys.argv[1]+"/token_L527931_000_000")
     for x in v:
         document = db[x['key']]
         token_name = x['key']
         #if token_name == "token_L527931_000_000":
         if token_name in tokens:
             print("will delete: ", token_name)
             db.delete(document)

def get_db():
    server = couchdb.Server("https://picas-lofar.grid.surfsara.nl:6984")
    username = sys.argv[3]
    pwd = sys.argv[4]
    server.resource.credentials = (username,pwd)
    db = server[sys.argv[2]]
    return db

if __name__ == '__main__':
   #Create a connection to the server
   db = get_db()
   #Delete the Docs in database
   deleteDoc(db)
