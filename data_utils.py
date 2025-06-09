from lsst.summit.utils import ConsDbClient
from lsst.daf.butler import Butler

def get_exp_catalog(save=False, username=None, token=None):
    """
    Parameters
    ----------
    save : bool, optional
        option to save exposure catalog, default False

    username : str, optional
        username on USDF, default None
        (required if running the script as a job)
        
    token : str, optional
        token to used to access ConsDB, default None
        (required if running the script as a job)
    Returns
    -------
    consdb : astropy.table.Table
        exposure catalog queried from the ConsDB LSSTCam visit1 table with columns 
        (exposure_id, band, exp_time, ra, dec, sky_rotation, img_type, physical_filter,
        airmass, obs_star_mjd, dimm_seeing, humidity, pressure, wind_speed, wind_dir, air_temp
        observation_reason)
    """
    
    query = """
        SELECT v.visit_id as exposure_id, v.band, v.exp_time, v.s_ra as ra, v.s_dec as dec, v.sky_rotation,
        v.img_type, v.physical_filter, v.airmass, v.obs_start_mjd, v.dimm_seeing, v.humidity, v.pressure,
        v.wind_speed, v.wind_dir, v.air_temp, v.observation_reason
        FROM cdb_lsstcam.visit1 v
        """

    if username is None or token is None:
        #assume that the user is running this from the Rubin Science Platform (RSP)
        client = ConsDbClient('http://consdb-pq.consdb:8080/consdb/')
    else:
        #assume that the user is running this from USDF 
        client = ConsDbClient(f"https://{username}:{token}@usdf-rsp.slac.stanford.edu/consdb")
    
    consdb = client.query(query)
    
    if save:
        outfile = f'lsstcam_exposure_catalog.csv'
        consdb.write(outfile, overwrite=True)
        
    return consdb

def initialize_butler(butler_dict=None):
    """
    Parameters
    ----------
    butler_dict : dict, optional 
        dictionary containing three keys: 'repo', 'collections', 'instrument'
        used to initialize Butler object. Default is None.

    Returns
    -------
    butler : lsst.daf.butler.Butler 
        butler used to query data products
    """
    if butler_dict is None:
        repo = "/repo/embargo_new" 
        collections = ['LSSTCam/runs/DRP/20250420_20250521/w_2025_21/DM-51076']
        instrument = "LSSTCam"
    else:
        repo = butler_dict['repo']
        collections = butler_dict['collections']
        instrument = butler_dict['instrument']
    
    butler = Butler(
            repo, 
            collections=collections,
            instrument=instrument)

    return butler
    
def get_dataset_refs(data_product):
    """
    Parameters
    ----------
    data_product : str
        name of data product to be queried

    Return 
    ------
    dataset_refs : list
        list of butler dataset references in the given butler collection
    """
    dataset_refs = butler.query_datasets(data_product, find_first=True, limit=1000000)

    return dataset_refs