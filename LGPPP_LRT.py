#!/usr/bin/python3

import os, sys
from utilities import setup_dirs, parse_arguments
from Tokens.createViews import createViews,get_db
from Tokens.createObsIDView import createViews_per_OBSID
from Tokens.resetErrorTokens import reset
from Tokens.removeObsIDTokens import deleteDocs
from Tokens.createTokens import loadTokens
from termios import tcflush, TCIOFLUSH

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

try:
    PICAS_DB=config['Picas']['PICAS_DB']
    PICAS_USR=config['Picas']['PICAS_USR']
    PICAS_USR_PWD=config['Picas']['PICAS_USR_PWD']
    COUCHDB_SERVER_URL_AND_PORT=config['Picas']['COUCHDB_SERVER_URL_AND_PORT']
except (NoSectionError, NoOptionError):
    print("Configuration file not valid or complete!")

###########
#Dictionary of input variables to make keeping track of values easier
###########

d_vars = {"srmfile":"","cfgfile":"","fadir":".","resuberr":False,"TSplit":True,"OBSID":"","sw_dir":"/cvmfs/softdrive.nl/wjvriend/lofar_stack","sw_ver":"2.16","parsetfile":"-","jdl_file":"","customscript":""}

start_dir = os.getcwd()

def submit_to_picas(resuberr, PICAS_DB, PICAS_USR, PICAS_USR_PWD, COUCHDB_SERVER_URL_AND_PORT, OBSID):

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


if __name__ == "__main__":
    parse_arguments(sys.argv, d_vars)
    setup_dirs(d_vars)
    #prepare_sandbox()

    #check_state_and_stage()
    
    ####################
    ##Wait for keystroke
    ###################

    yes = set(['yes','y', 'ye','yea','yesh','Y','oui', ''])
    no = set(['no','n','N'])
    print("")
    print("Do you want to continue? Y/N (Enter continues)")

    tcflush(sys.stdin, TCIOFLUSH) #Flush input buffer to stop enter-spammers
    choice = input().lower()

    if choice in yes:
       pass
    elif choice in no:
       sys.exit()
    else:
       sys.exit()

    submit_to_picas(d_vars['resuberr'], PICAS_DB, PICAS_USR, PICAS_USR_PWD, COUCHDB_SERVER_URL_AND_PORT, d_vars['OBSID'])	
    #start_jdl()
    print("https://goo.gl/CtHlbP")
    sys.exit()
