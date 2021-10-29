#python3
import os
import logging
import re

def validate_init_params(params):
    """
    Args:
        params: (d)
            Must contain all the parameters passed in
            as shown in function.
        cfg_d: (d)
            #models_dir: (s) Path to all models
    Returns:
        vp: (d) "Validated Params"
            genome_ref: (s)
            mutantpool_ref: (s)
    """

    #Validated params dict
    vp = {}

    if 'genome_ref' in params:
        vp['genome_ref'] = params['genome_ref']
    else:
        raise Exception("Genome Ref not passed in params.")

    if 'mutantpool_ref' in params:
        vp['mutantpool_ref'] = params['mutantpool_ref']
    else:
        raise Exception("Genome Ref not passed in params.")

    return vp


