#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script generates Makefile that can be used to import countries
# into libosmscout and generate geocoder-nlp database

import os, json, codecs
from hierarchy import Hierarchy
from mapbox_country_pack import country_pack as mapbox_pack
from valhalla_country_pack import country_pack as valhalla_pack


fmake = open("Makefile.import", "w")
fmake.write("# This Makefile is generated by script prepare_countries.py\n\n")
fmake.write("BUILDER_GEOCODER=./build_geocoder.sh\n")
fmake.write("BUILDER_MAPNIK=./build_mapnik.sh\n")
fmake.write("BUILDER_OSMSCOUT=./build_osmscout.sh\n")
fmake.write("BASE_DIR=distribution\n")
fmake.write("PBF_DIR=splitted\n")
fmake.write("\nall: $(BASE_DIR)/all_countries_done\n\techo All Done\n\n")

all_countries = ""

def spath(name):
    return name.replace('/','-')

def pbfname(name):
    return name.replace("/", "-") + ".pbf"

########### Main loop #############
provided_countries = {}

fmake.write("$(BASE_DIR)/geocoder-nlp/.directory:\n\tmkdir -p $(BASE_DIR)/geocoder-nlp/\n\ttouch $(BASE_DIR)/geocoder-nlp/.directory\n\n")
fmake.write("$(BASE_DIR)/mapnik/countries/.directory:\n\tmkdir -p $(BASE_DIR)/mapnik/countries/\n\ttouch $(BASE_DIR)/mapnik/countries/.directory\n\n")
fmake.write("$(BASE_DIR)/osmscout/.directory:\n\tmkdir -p $(BASE_DIR)/osmscout/\n\ttouch $(BASE_DIR)/osmscout/.directory\n\n")

for root, folders, files in os.walk(Hierarchy.base_dir):
    if "name" in files and not Hierarchy.ignore(root):
        name = Hierarchy.get_full_name(root)
        poly = root + "/poly"
        print Hierarchy.get_id(root), name, Hierarchy.get_postal(root), Hierarchy.get_postcodes(root)

        cid = Hierarchy.get_id(root)
        provided_countries[cid] = { "id": cid,
                                    "type": "territory",
                                    "name": Hierarchy.get_full_name(root),
                                    "postal_country": { "path": "postal/countries-v1/" + Hierarchy.get_postal(root) },
                                    "osmscout": { "path": "osmscout/" + spath(cid) },
                                    "geocoder_nlp": { "path": "geocoder-nlp/" + spath(cid) },
                                    "mapnik_country": { "path": "mapnik/countries/" + spath(cid) },
                                    "mapboxgl_country": mapbox_pack(poly),
                                    "valhalla": valhalla_pack(poly),
        }

        pbf = "$(PBF_DIR)/" + pbfname(cid)

        # geocoder-nlp
        country_target = "$(BASE_DIR)/geocoder-nlp/" + spath(cid) + ".timestamp"

        all_countries += country_target + " "
        fmake.write(country_target + ": $(BASE_DIR)/geocoder-nlp/.directory " + pbf +
                    "\n\t$(BUILDER_GEOCODER) $(PBF_DIR)/" + pbfname(cid) + " $(BASE_DIR) " +
                    spath(cid) + " " + Hierarchy.get_postal(root) + " " + Hierarchy.get_postcodes(root) + "\n\n")

        # mapnik
        country_target = "$(BASE_DIR)/mapnik/countries/" + spath(cid) + ".timestamp"

        all_countries += country_target + " "
        fmake.write(country_target + ": $(BASE_DIR)/mapnik/countries/.directory " + pbf +
                    "\n\t$(BUILDER_MAPNIK) $(PBF_DIR)/" + pbfname(cid) + " $(BASE_DIR) " +
                    spath(cid) + "\n\n")

        # osmscout
        country_target = "$(BASE_DIR)/osmscout/" + spath(cid) + ".timestamp"

        all_countries += country_target + " "
        fmake.write(country_target + ": $(BASE_DIR)/osmscout/.directory " + pbf +
                    "\n\t$(BUILDER_OSMSCOUT) $(PBF_DIR)/" + pbfname(cid) + " $(BASE_DIR) " +
                    spath(cid) + " " + poly + "\n\n")

fmake.write("\n$(BASE_DIR)/all_countries_done: " + all_countries + "\n\techo > $(BASE_DIR)/all_countries_done\n\n")

# save provided countries
fjson = open("countries.json", "w")
fjson.write( json.dumps( provided_countries, sort_keys=True, indent=4, separators=(',', ': ')) )

print "\nExamine generated Makefile.import and run make using it. See build.sh and adjust the used executables first\n"
