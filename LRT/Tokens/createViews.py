# ============================================================================================= #
# author: Natalie Danezi <anatoli.danezi@surfsara.nl>	--  SURFsara				#
# helpdesk: Grid Services <grid.support@surfsara.nl>	--  SURFsara				#
#												#
# usage: python createViews.py [picas_db_name] [picas_username] [picas_pwd]			#
# description:											#
#	Connect to the server with [picas_username] [picas_pwd]					#
#	Create the following Views in [picas_db_name]:						#
#		todo View : lock_timestamp == 0 && done_timestamp == 0				#
#		locked View : lock_timestamp > 0 && done_timestamp == 0				#
#		done View : lock_timestamp > 0 && done _timestamp > 0 && doc.output == 0	#
#               error View : lock_timestamp > 0 && done _timestamp > 0 && doc.output > 0	#
#		overview_total View : sum tokens per View (Map/Reduce)				#
# ============================================================================================= #

import sys
if not 'couchdb' in sys.modules:
        import couchdb
from couchdb import Server
from couchdb.design import ViewDefinition

def createViews(db):
   generalViewCode='''
function(doc) {
   if(doc.type == "token") {
    if(%s) {
      emit(doc._id, doc._id);
    }
  }
}
'''
   # todo View
   todoCondition = 'doc.lock == 0 && doc.done == 0'
   todo_view = ViewDefinition('Monitor', 'todo', generalViewCode %(todoCondition))
   todo_view.sync(db)
   # locked View
   lockedCondition = 'doc.lock > 0 && doc.done == 0'
   locked_view = ViewDefinition('Monitor', 'locked', generalViewCode %(lockedCondition))
   locked_view.sync(db)
   # done View
   doneCondition = 'doc.lock > 0 && doc.done > 0 && doc.output == 0'
   done_view = ViewDefinition('Monitor', 'done', generalViewCode %(doneCondition))
   done_view.sync(db)
   #
   errorCondition = 'doc.lock > 0 && doc.done > 0 && doc.output > 0'
   error_view = ViewDefinition('Monitor', 'error', generalViewCode %(errorCondition))
   error_view.sync(db)

   # overview_total View -- lists all views and the number of tokens in each view
   overviewMapCode='''
function(doc) {
   if(doc.type == "token") {
       if (doc.lock == 0 && doc.done == 0){
          emit('todo', 1);
       }
       if(doc.lock > 0 && doc.done == 0) {
          emit('locked', 1);
       }
       if(doc.lock > 0 && doc.done > 0 && doc.output == 0) {
          emit('done', 1);
       }
       if(doc.lock > 0 && doc.done > 0 && doc.output > 0) {
          emit('error', 1);
       }
   }
}
'''
   overviewReduceCode='''
function (key, values, rereduce) {
   return sum(values);
}
'''
   overview_total_view = ViewDefinition('Monitor', 'overview_total', overviewMapCode, overviewReduceCode)
   overview_total_view.sync(db)

def get_db(PICAS_DB, PICAS_USR, PICAS_USR_PWD, COUCHDB_SERVER_URL_AND_PORT):
    print("COUCHDB_SERVER_URL_AND_PORT = {0}".format(COUCHDB_SERVER_URL_AND_PORT))
    server = couchdb.Server(COUCHDB_SERVER_URL_AND_PORT)
    username = PICAS_USR 
    pwd = PICAS_USR_PWD
    server.resource.credentials = (username,pwd)
    print("PICAS_DB = {0}, PICAS_USR = {1}, PICAS_USR_PWD ={2}, COUCHDB_SERVER_URL_AND_PORT={3}".format(PICAS_DB, PICAS_USR, PICAS_USR_PWD, COUCHDB_SERVER_URL_AND_PORT)) 
    print("Before db = server[PICAS_DB]")
    # import pdb; pdb.set_trace()
    db = server[PICAS_DB]
    print("Got passed db = server[PICAS_DB]")
    return db
