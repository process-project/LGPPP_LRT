#!/usr/bin/python3

import os, sys
from LRT.utilities import setup_dirs, parse_arguments
from LRT.Tokens.createViews import createViews,get_db
from LRT.Tokens.createObsIDView import createViews_per_OBSID
from LRT.Tokens.resetErrorTokens import reset
from LRT.Tokens.removeObsIDTokens import deleteDocs
from LRT.Tokens.createTokens import loadTokens

from configparser import ConfigParser, NoSectionError, NoOptionError
config = ConfigParser()
# Make sure PICASCONFIGPATH is exported in the shell where python manage.py runserver is issued.
config.read(os.path.join(os.environ["PICASCONFIGPATH"],'config.ini'))


start_dir = os.getcwd()

def submit_to_picas(resuberr, OBSID):

    try:
        PICAS_DB=config['Picas']['PICAS_DB']
        PICAS_USR=config['Picas']['PICAS_USR']
        PICAS_USR_PWD=config['Picas']['PICAS_USR_PWD']
        COUCHDB_SERVER_URL_AND_PORT=config['Picas']['COUCHDB_SERVER_URL_AND_PORT']
    except (KeyError, NoSectionError, NoOptionError):
        print("Configuration file not valid or complete, nothing submitted to Picas.")
        return

    os.chdir(start_dir+"/Tokens")

    # subprocess.call(['python','createViews.py',os.environ["PICAS_DB"],os.environ["PICAS_USR"],os.environ["PICAS_USR_PWD"]])
    #Create a connection to the server
    db = get_db(PICAS_DB, PICAS_USR, PICAS_USR_PWD, COUCHDB_SERVER_URL_AND_PORT)
    #Create the Views in database
    createViews(db)
    
    # subprocess.call(['python','createObsIDView.py',d_vars['OBSID'],os.environ["PICAS_DB"],os.environ["PICAS_USR"],os.environ["PICAS_USR_PWD"]])
    # import createObsIDView_simpler
    print(("db = ", db))
    #Create the Views in database
    print(("OBSID = ", OBSID))
    createViews_per_OBSID(db,OBSID)
    
    if resuberr:
	    # subprocess.call(['python','resetErrorTokens.py',os.environ["PICAS_DB"],os.environ["PICAS_USR"],os.environ["PICAS_USR_PWD"]])
	    reset(PICAS_DB, PICAS_USR, PICAS_USR_PWD, COUCHDB_SERVER_URL_AND_PORT) 
    else:
	    # subprocess.call(['python','removeObsIDTokens.py',d_vars['OBSID'],os.environ["PICAS_DB"],os.environ["PICAS_USR"],os.environ["PICAS_USR_PWD"]])
	    deleteDocs(db, OBSID)
	    # subprocess.call(['python','createTokens.py',d_vars['OBSID'],os.environ["PICAS_DB"],os.environ["PICAS_USR"],os.environ["PICAS_USR_PWD"]])
	    loadTokens(db, OBSID)
    #subprocess.call(['python','createViews.py',os.environ["PICAS_DB"],os.environ["PICAS_USR"],os.environ["PICAS_USR_PWD"]])
    #subprocess.call(['python','createObsIDView.py',d_vars['OBSID'],os.environ["PICAS_DB"],os.environ["PICAS_USR"],os.environ["PICAS_USR_PWD"]])
    #os.chdir("../../")
    os.chdir("../")

    os.remove('srmlist')
    os.remove('subbandlist')
