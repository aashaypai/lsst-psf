import os
import numpy as np
import h5py

import data_utils as du
import lsstcam_utils as lu
import psf_utils as pu

## initialize butler
butler_dict = dict(repo = "/repo/embargo_new", 
                   collections = ['LSSTCam/runs/DRP/20250420_20250521/w_2025_21/DM-51076'],
                   instrument = "LSSTCam"
                  )

butler = du.initialize_butler(butler_dict=butler_dict)

## get dataset refs to the Piff PSF catalog
dataset_refs = du.get_dataset_refs(data_product='refit_psf_star')


