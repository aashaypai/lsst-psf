import os, sys
import numpy as np
import h5py

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'psf_utils')))

import data_utils as du
import lsstcam_utils as lu
import psf_utils as pu

import psf_catalog as pc

## to add columns to the PSF catalog, go to psf_catalog.py

def main(username, collection):
    ## initialize butler
    butler_dict = dict(repo = "/repo/embargo_new", 
                       collections = [collection],
                       instrument = "LSSTCam"
                      )
    
    butler = du.initialize_butler(butler_dict=butler_dict)
    
    ## get dataset refs to the Piff PSF catalog
    dataset_refs = du.get_dataset_refs(butler, data_product='refit_psf_star')
    
    ## read token for ConsDB
    with open("../token.txt", "r") as file:
        token = file.readline()
    
    ## get exposure catalog from ConsDB
    consdb = du.get_exposure_catalog(username = username, token = token)
    
    ## make PSF catalog
    psf_catalog = pc.make_psf_catalog(dataset_refs = dataset_refs,
                                   consdb = consdb,
                                   butler = butler)

    comments = ['version=0.1.0', 'date:2025-06-03', 
                f'collection: {collection}']
    ## write PSF catalog
    pc.write_psf_catalog(psf_catalog = psf_catalog,
                         filename = "LSSTCam_DRP_PSF_catalog.h5", 
                         comments = comments)

if __name__ == '__main__':
    ## change these if necessary ##
    username = 'pai'
    collection = 'LSSTCam/runs/DRP/20250420_20250521/w_2025_21/DM-51076'
    
    main(username = username, collection = collection)
                         
    
                                   
    