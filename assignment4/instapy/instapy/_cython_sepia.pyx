import numpy as np

cpdef _sepiaa(orginal_image, level):
    
    """
    Add sepia filter to a RGB-image with cython implementation. 
    
    -----------------------------------------
    Arguments:
        orginal_image : numpy ndarray 
            the orginal image, in RGB, represented as a numpy array
        
        level : float, optional, default=1.0
            Ammount of sepia-effect added to image. Must be a float between 0 and 1, where 1 is 100%, 0 is 0%.
    
    Returns: 
        grayscale_image : numpy ndarray
            The transformed image, in RGB, represented as a numpy array
            
    -----------------------------------------
    """
    
    #height, width, channels
    cpdef int H,W,C
    H, W, C = orginal_image.shape    
    
    sepia_image = np.empty_like(orginal_image)
    
    #sepia_matrix = [[ 0.393 , 0.769 , 0.189] ,
    #                [ 0.349 , 0.686 , 0.168] ,
    #                [ 0.272 , 0.534 , 0.131]]
    
    cpdef int i,j
    cpdef float val_R, val_G, val_B, k
    
    for i in range(H):
        for j in range(W): 
            
            red = orginal_image[i,j,0]
            green = orginal_image[i,j,1]
            blue = orginal_image[i,j,2]
            
            k = 1-level
            #red
            val_R = red * (0.393 + (0.607*k)) + green * (0.769 - (0.769*k))  + blue * (0.189 - (0.189*k))
            
            #green
            val_G = red * (0.349 - (0.349*k)) + green * (0.686 + (0.314*k)) + blue * (0.168 - (0.168*k))
            
            #blue
            val_B = red * (0.272 - (0.272*k)) + green * (0.534 - (0.534*k)) + blue * (0.131 + (0.869*k))
            
            sepia_image[i, j, 0] = min(255, val_R)
            sepia_image[i, j, 1] = min(255, val_G)
            sepia_image[i, j, 2] = min(255, val_B)
    
            
    return sepia_image