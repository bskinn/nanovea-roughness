import csv
import itertools as itt
from enum import Enum

import numpy as np
from scipy.integrate import simps
from scipy.optimize import minimize


# #####  NANOVEA DATA IMPORT  #####

class NanoveaData(Enum):
    Filename = 'fname'
    Counts = 'counts'
    Incs = 'incs'
    ZData = 'zdata'


def nanovea_data_from_scanfile(fname):
    """Load a Nanovea data file and return structured contents."""
    with open(fname) as f:
        # Create a CSV reader from the indicated file.
        csvr = csv.reader(f)

        def gen(it):
            """Emit each value from the imported data file."""
            for line in it:
                for val in line:
                    try:
                        yield float(val)
                    except ValueError:
                        # Assume NM point; -1 key value
                        # -1 is ok b/c all Nanovea export data is +'ve
                        yield -1

        # Generate the array from the emitted CSV data
        arr = np.fromiter(gen(csvr), dtype=np.float)

    # Reshape the resulting array into three columns, x/y/z
    arr = arr.reshape((arr.shape[0]//3, 3))

    if arr[0, 0] == arr[1, 0]:
        # Data was scanned along the y-axis first
        # The number of x-points is the number of times the zero
        # value occurs in the y-data column
        xct = np.sum(arr == arr[0, 1], axis=0)[1]

        # The number of y-points then must be the total
        # number of rows in the dataset divided by the
        # number of x-points
        yct = arr.shape[0] // xct

        # Increments account for possibility of data not starting at zero
        xinc = arr[yct, 0] - arr[0, 0]
        yinc = arr[1, 1] - arr[0, 1]

        # Pull the grid data for all three coords
        # Need to transpose here because when the y-data is
        # running in the innermost cycle in the data file,
        # it lies along the columns (axis=0), when it's desired
        # to lie along the rows (axis=1); see bottom
        xgrid = arr[:,0].reshape((yct, xct), order='F').T
        ygrid = arr[:,1].reshape((yct, xct), order='F').T
        zgrid = arr[:,2].reshape((yct, xct), order='F').T
    else:
        # Data was scanned along the x-axis first
        # Everything(?) here is x/y reversed from the above.
        yct = np.sum(arr == arr[0,0], axis=0)[0]
        xct = arr.shape[0] // yct
        xinc = arr[1, 0] - arr[0, 0]
        yinc = arr[xct, 1] - arr[0, 1]
        xgrid = arr[:,0].reshape((xct, yct), order='F')
        ygrid = arr[:,1].reshape((xct, yct), order='F')
        zgrid = arr[:,2].reshape((xct, yct), order='F')

    # At this point, -1 values are replaced with nan,
    # and the x-coordinate increases along axis=0.
    # This is for semantic consistency with x corresponding
    # to the first axis of the array, even though that means
    # the x-coordinate runs down the screen when the ndarray
    # is print()'ed
    zgrid[zgrid == -1] = np.nan

    out_d = {NanoveaData.Filename: fname,
             NanoveaData.Counts: [xct, yct],
             NanoveaData.Incs: [xinc, yinc],
             NanoveaData.ZData: zgrid}

    return out_d


# #####  PLANE RESIDUALS CALCULATION  #####

def plane_array(params, arr):
    """Helper function to generate plane data from a model fit.
    
    Plane data is generated over the same grid as the input 'arr`'.
    
    params[0] is the x-coefficient
    params[1] is the y-coefficient
    params[2] is the constant
    
    Function is nan-safe.
    
    """
    X, Y = np.meshgrid(*map(np.arange, arr.shape), indexing='ij')
    
    return params[0]*X + params[1]*Y + params[2]
    

def get_residuals(arr):
    """Calculate residuals over best-fit plane.

    Requires that the spacing increments in both the x- and y-directions
    are uniform.

    """
    def fit_resids(params, arr):
        """Helper function to do the fitting.
        
        params[0] is the x-coefficient
        params[1] is the y-coefficient
        params[2] is the constant
        
        Returns the array of residuals.
        
        Function is nan-safe.
        
        """
        return arr - plane_array(params, arr)
    
    
    def fit_func(params, arr):
        """Helper function to do the fitting.
        
        params[0] is the x-coefficient
        params[1] is the y-coefficient
        params[2] is the constant
        
        Fit function is the SSD from data to plane.
        
        Function is nan-safe.
        
        """
        return np.nansum(fit_resids(params, arr) ** 2)
    
    res = minimize(fit_func, [0, 0, 0], args=(arr,), method='Nelder-Mead')
    
    return fit_resids(res.x, arr), res.x


# #####    ROUGHNESS CALCULATIONS  #####

def Sa_calc(arr):
    """Calculate the Sa of the given array over a best-fit plane.
    
    Sa is the mean of the absolute residuals relative to the fitted surface.
    
    ASSUMES x- and y-spacings are (possibly different) CONSTANTS.
    
    Function is nan-safe.
    
    """
    resids = get_residuals(arr)
    
    return simps(simps(np.nan_to_num(np.abs(resids)))) / np.sum(np.isfinite(resids))


def Sq_calc(arr):
    """Calculate the Sq of the given array over a best-fit plane.
    
    Sq is the RMS value of the residuals relative to the fitted surface.
    
    ASSUMES x- and y-spacings are (possibly different) CONSTANTS.
    
    Function is nan-safe.
    
    """
    resids = get_residuals(arr, x, y, **kwargs)
    
    return np.sqrt(np.nansum(resids ** 2.0) / np.sum(np.isfinite(resids)))


def Sz_calc(arr):
    """Calculate the Sz of the given array over a best-fit plane.
    
    Sz is the difference between the maximum and minimum signed residuals
    relative to the fitted surface.
    
    ASSUMES x- and y-spacings are (possibly different) CONSTANTS.
    
    Function is nan-safe.
    
    """
    resids = get_residuals(arr, x, y, **kwargs)
    
    return np.nanmax(resids) - np.nanmin(resids)


def Sp_calc(arr):
    """Calculate the Sp of the given array over a best-fit plane.
    
    Sp is the maximum signed residual relative to the fitted surface.
    
    ASSUMES x- and y-spacings are (possibly different) CONSTANTS.
    
    Function is nan-safe.
    
    """
    resids = get_residuals(arr, x, y, **kwargs)
    
    return np.nanmax(resids)


def Sv_calc(arr):
    """Calculate the Sv of the given array over a best-fit plane.
    
    Sv is the absolute value of the most-negative residual relative to the fitted surface.
    
    ASSUMES x- and y-spacings are (possibly different) CONSTANTS.
    
    Function is nan-safe.
    
    """
    resids = get_residuals(arr, x, y, **kwargs)
    
    return np.abs(np.nanmin(resids))



