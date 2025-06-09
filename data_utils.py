from lsst.summit.utils import ConsDbClient

def get_exp_catalog(save=False, username=None, token=None):
    """
    Parameters
    ----------
    save : bool, default False
        option to save exposure catalog

    username : str, default None
        username on USDF 
        (required if running the script as a job)
        
    token : str, default None
        token to used to access ConsDB 
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


