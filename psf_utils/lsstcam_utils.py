import numpy as np

from lsst.obs.lsst import LsstCam
import lsst.afw.cameraGeom as afwCameraGeom

def visit_to_date(visit_arr):
    v = visit_arr.astype(str)
    date = [visit[0:8] for visit in v]
    return date
    
def pixel_to_focal(x, y, detid):
    """
    Parameters
    ----------
    x, y : float
        point in units of pixels of detector image
    detid : int 
        integer id of the detector (between 0-189).

    Returns
    -------
    fpx, fpy : np.ndarray
        focal plane position in millimeters in DVCS
        See https://lse-349.lsst.io/
    """
    det = LsstCam.getCamera()[detid]
    
    tx = det.getTransform(afwCameraGeom.PIXELS, afwCameraGeom.FOCAL_PLANE)
    fpx, fpy = tx.getMapping().applyForward((x, y))    

    return fpx, fpy

    
def detector_type(detectors):
    """
    Parameters
    ----------
    detectors : np.ndarray of int
        list of detector ids

    Returns
    ------- 
    det_type_itl : np.ndarray of bool
        mask array which is 1 if the detector type is ITL, 0 otherwise

    det_type_e2v : np.ndarray of bool
        mask array which is 1 if the detector type is E2V, 0 otherwise
    """
    itl = np.append(np.arange(0, 36), np.append(np.arange(72, 81), np.arange(162, 189)))
    e2v = np.array([i for i in np.arange(0, 189) if i not in itl])

    itl_mask = np.isin(detectors, itl)
    e2v_mask = np.isin(detectors, e2v)

    det_type_itl = np.full(np.size(detectors), 0, dtype=np.int32)
    det_type_e2v = np.full(np.size(detectors), 0, dtype=np.int32)
    
    det_type_itl[itl_mask] = 1
    det_type_e2v[e2v_mask] = 1

    return det_type_itl, det_type_e2v