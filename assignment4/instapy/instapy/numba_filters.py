import cv2
import numpy as np
from numba import jit 


def numba_color2gray(input_filename, output_filename=None, scale=None):
    
    """
    Grayscale image filter.
    Turn a image of choice given by filename to a grayscale image.
    Implemented with numba. 
    Savnes and returns the transformed image. 
    -----------------------------------------
    Arguments:
        input_filename : str 
            filename or path to the image 
        
        output_filename: str, optinal, default=None 
            filename or path to the transformed image
            
        scale : float, optional, default=None
            Scale factor to resize image. (e.g. 0.5 halves image dimentions) 
    
    Returns: 
        grayscale_image : numpy ndarray
            The transformed image with as a numpy array. 
            
    -----------------------------------------
    """
    
    #Reads image, changes to RGB and grayscales it
    orginal_image = cv2.imread(input_filename)
    
    #resize if scale is given
    if scale is not None:
        orginal_image = cv2.resize(orginal_image, (0,0), fx = scale , fy = scale)
    
    orginal_image = cv2.cvtColor(orginal_image, cv2.COLOR_BGR2RGB)
    grayscale_image = _grayscale(orginal_image)
    grayscale_image = grayscale_image.astype("uint8")
    
    
    #Write the image to file with correct filename 
    if output_filename is None:
        filename, ext = input_filename.split(".")
        full_filename = filename + "_grayscale." + ext
        cv2.imwrite(full_filename, grayscale_image)
    else:
        cv2.imwrite(output_filename, grayscale_image)  
    
    return grayscale_image


@jit(nopython = True)
def _grayscale(orginal_image):
    
    """
    Grayscales an RGB-image with numba implementation. 
    
    -----------------------------------------
    Arguments:
        orginal_image : numpy ndarray 
            the orginal image, in RGB, represented as a numpy array
    
    Returns: 
        grayscale_image : numpy ndarray
            The transformed image, in RGB, represented as a numpy array
            
    -----------------------------------------
    """
    #height, width, channels
    H, W, C = orginal_image.shape
    
    grayscale_image = np.zeros((H,W,C))
    
    for i in range(H):
        for j in range(W): 
 
            grayscale_image[i, j] += orginal_image[i, j, 0] * 0.21 \
                                   + orginal_image[i, j, 1] * 0.72 \
                                   + orginal_image[i, j, 2] * 0.07 \
            
    return grayscale_image
    




def numba_color2sepia(input_filename, output_filename=None, scale=None, level=1.0):
    """
    Adds sepia filter to the image.
    Turn a image of choice given by filename to a sepia image.
    Implemented with numba. 
    Savnes and returns the transformed image. 
    -----------------------------------------
    Arguments:
        input_filename : str 
            filename or path to the image 
        
        output_filename: str, optinal, default=None 
            filename or path to the transformed image
            
        scale : float, optional, default=None
            Scale factor to resize image. (e.g. 0.5 halves image dimentions) 
        
        level : float, optional, default=1.0
            Ammount of sepia-effect added to image. Must be a float between 0 and 1, where 1 is 100%, 0 is 0%.
    
    Returns: 
        grayscale_image : numpy ndarray
            The transformed image with as a numpy array. 
            
    -----------------------------------------
    """
    #Reads image, changes to RGB and add sepia filter 
    orginal_image = cv2.imread(input_filename)
    
    #resize if scale is given
    if scale is not None:
        orginal_image = cv2.resize(orginal_image, (0,0), fx = scale , fy = scale)
        
    orginal_image = cv2.cvtColor(orginal_image, cv2.COLOR_BGR2RGB)
    sepia_image = _sepia(orginal_image, level)
    sepia_image = sepia_image.astype("uint8")
    #Changes Back to BGR
    sepia_image = cv2.cvtColor(sepia_image, cv2.COLOR_BGR2RGB)
    
    #Write the image to file with correct filename 
    if output_filename is None:
        filename, ext = input_filename.split(".")
        full_filename = filename + "_sepia." + ext
        cv2.imwrite(full_filename, sepia_image)
    else:
        cv2.imwrite(output_filename, sepia_image) 
          
    
    return sepia_image


@jit(nopython = True)
def _sepia(orginal_image, level):
    

    """
    Add sepia filter to a RGB-image with numba implementation. 
    
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
    H, W, C = orginal_image.shape    
    
    sepia_image = np.empty_like(orginal_image)
    
    #sepia_matrix = [[ 0.393 , 0.769 , 0.189] ,
    #                [ 0.349 , 0.686 , 0.168] ,
    #                [ 0.272 , 0.534 , 0.131]]
    
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