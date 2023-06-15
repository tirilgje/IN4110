import cv2
import numpy as np
import time 

import _cython_grayscale as cg
import _cython_sepia as cs



#comeplie with: python setup.py build_ext --inplace

def cython_color2gray(input_filename, output_filename=None, scale=None):
    """
    Grayscale image filter.
    Turn a image of choice given by filename to a grayscale image.
    Implemented with cython. 
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
    
    #if resize is given 
    if scale is not None:
        orginal_image = cv2.resize(orginal_image, (0,0), fx = scale , fy = scale)
        
    orginal_image = cv2.cvtColor(orginal_image, cv2.COLOR_BGR2RGB)
    
    grayscale_image = cg._grayscale(orginal_image) 
    
    grayscale_image = grayscale_image.astype("uint8")
    
    #Write the image to file with correct filename 
    if output_filename is None:
        filename, ext = input_filename.split(".")
        full_filename = filename + "_grayscale." + ext
        cv2.imwrite(full_filename, grayscale_image)
    else:
        cv2.imwrite(output_filename, grayscale_image)
        
       
    return grayscale_image






def cython_color2sepia(input_filename, output_filename=None, scale=None, level=1.0):
    """
    Adds sepia filter to the image.
    Turn a image of choice given by filename to a sepia image.
    Implemented with cython. 
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
    
    #if resize is given
    if not scale is None:
        orginal_image = cv2.resize(orginal_image, (0,0), fx = scale , fy = scale)
    
    orginal_image = cv2.cvtColor(orginal_image, cv2.COLOR_BGR2RGB)
    sepia_image = cs._sepiaa(orginal_image, level)
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