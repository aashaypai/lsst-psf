

def moment2ellipticity(ixx, iyy, ixy):
    """
    Parameters
    ----------
    ixx : float
        second moment of PSF

    iyy : float
        second moment of PSF

    ixy : float
        second moment of PSF

    Returns
    -------
    e1 : float
        ellipticity of PSF
        
    e2 : float
        ellipticity of PSF
        
    T : float
        size of PSF in pixels
    """
    e1 = (ixx-iyy)/(ixx+iyy)
    e2 = 2*ixy/(ixx+iyy)
    T = ixx+iyy
    return e1, e2, T
    


