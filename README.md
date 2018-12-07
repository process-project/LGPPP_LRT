# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* LGPPP stands for LOFAR Grid PreProcessing Pipeline. It is part of LRT (LOFAR Reductions Tools). The actual PPP software is not in this repository, it can, however, be launched through the interface we provide here.
* This does require access to the "Picas" database, which requires credentials as a config.ini file which we do not provide here.
* These tools were developed by SURFsara and by the [LOFAR e-infra group](https://www.universiteitleiden.nl/en/research/research-facilities/science/lofar-e-infrastructure-group) (enabled by e-infra grants 1600022, 160152, 170194 from SURFsura).
* The original authors are Raymond Oonk and Natalie Danezi. It was somewhat refactored by Hanno Spreeuw from the Netherlands eScience Center - for the European Open Science Cloud Pilot for LOFAR - primarily to make this software pip installable.
* SURFsara and the LOFAR e-infra group will provide no guarantees, warranty or accept any liability related to this repository and code.
* Nowhere should any usernames or passwords be shared without explicit authorization from both SURFsara and the [LOFAR e-infra group](https://www.universiteitleiden.nl/en/research/research-facilities/science/lofar-e-infrastructure-group). 

### How do I get set up? ###

* git clone this repo and `pip install .` in the directory containing `setup.py`.
* `export PICASCONFIG_PATH=/path/to/config.ini`