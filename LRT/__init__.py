import json, os, uuid
from os import path
from LRT.LGPPP import submit_to_picas, setup_dirs
from LRT.utilities import parse_arguments

###########
#Dictionary of input variables to make keeping track of values easier
###########

d_vars = {"srmfile":"","cfgfile":"","fadir":".","resuberr":False,"TSplit":True,"OBSID":"","sw_dir":"/cvmfs/softdrive.nl/wjvriend/lofar_stack","sw_ver":"2.16","parsetfile":"-","jdl_file":"","customscript":""}

def give_name():
    jsonfile = give_config()
    name = list(jsonfile.keys())[0]
    return name

# Copied from https://github.com/EOSC-LOFAR/LGPPP_LOFAR_pipeline/blob/master/LGPPP_LOFAR_pipeline/__init__.py 
def give_version():
    return "0.0"

def give_config():
    json_config_file = os.path.join(os.path.dirname(__file__), "data", "config.json")
    with open(json_config_file) as json_data:
        return json.load(json_data)

def give_argument_names(required=False):
    jsonfile = give_config()
    name = list(jsonfile.keys())[0]
    required = jsonfile[name]["schema"]["required"]
    properties = set(jsonfile[name]["schema"]["properties"].keys())
    if required:
        return required
    else:
        return properties

# Copied from https://github.com/EOSC-LOFAR/LGPPP_LOFAR_pipeline/blob/master/LGPPP_LOFAR_pipeline/__init__.py 
def write_observations(observation, fn):
    srm_uris = observation.split('|')
    with open(fn, 'w') as f:
        for srm_uri in srm_uris:
            f.write(srm_uri + '\n')

# Copied from https://github.com/EOSC-LOFAR/LGPPP_LOFAR_pipeline/blob/master/LGPPP_LOFAR_pipeline/__init__.py 
def write_config(config, fn):
    with open(fn, 'w') as f:
        f.write('''AVG_FREQ_STEP   = {avg_freq_step}
                   AVG_TIME_STEP   = {avg_time_step}
                   DO_DEMIX        = {do_demix}
                   DEMIX_FREQ_STEP = {demix_freq_step}
                   DEMIX_TIME_STEP = {demix_time_step}
                   DEMIX_SOURCES   = {demix_sources}
                   SELECT_NL       = {select_nl}
                   PARSET		= {parset}
                   '''.format(**config))

# Copied from https://github.com/EOSC-LOFAR/LGPPP_LOFAR_pipeline/blob/master/LGPPP_LOFAR_pipeline/__init__.py 
def run_pipeline(observation, **config):
    cwd = os.getcwd()
    print("Current working directory = ")
    pdir = cwd
    job_id = str(uuid.uuid4())

    obs_fn = path.join(pdir, 'srm.' + job_id + '.txt')
    write_observations(observation, obs_fn)
    config_fn = path.join(pdir, 'master_setup.' + job_id + '.cfg')
    write_config(config, config_fn)

    # Redundant now.
    # run(pdir, obs_fn, config_fn, job_id)
    parse_arguments([obs_fn, config_fn], d_vars)
    setup_dirs(d_vars)
    submit_to_picas(d_vars['resuberr'], d_vars['OBSID'])
    return 'Input and log files *.' + job_id + '.* in dir ' + pdir
