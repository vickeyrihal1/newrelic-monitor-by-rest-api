#!env python

import os
import yaml

# uri list
def uri_list(file):
    config = os.path.join(os.path.dirname(__file__), file)
    
    with open(config, "r") as file:
        uris_metadata = yaml.safe_load(file)

    # Make a list of all the prod uris
    uri_list = []

    for uris in uris_metadata.values():
        uri_list += list(uris.keys())
    return(uri_list)

