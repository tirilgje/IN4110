import numpy as np
#cimport numpy as np

#comeplie with: python setup.py build_ext --inplace


cpdef _grayscale(orginal_image):
    
    """
    Grayscales an RGB-image with cython implementation. 
    
    -----------------------------------------
    Arguments:
        orginal_image : numpy ndarray 
            the orginal image, in RGB, represented as a numpy array
    
    Returns: 
        grayscale_image : numpy ndarray
            The transformed image, in RGB, represented as a numpy array
            
    -----------------------------------------
    
    """
    
    
    cpdef int H, W, C 
    
    H, W, C = orginal_image.shape
    grayscale_image = np.zeros((H,W,C))
    
    cpdef int i,j
    
    for i in range(H):
        for j in range(W): 
            grayscale_image[i, j] += orginal_image[i, j, 0] * 0.21 \
                                   + orginal_image[i, j, 1] * 0.72 \
                                   + orginal_image[i, j, 2] * 0.07        
    return grayscale_image