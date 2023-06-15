import cv2
import numpy as np
import time 
import python_color2gray as pyc2g

def numpy_color2gray(input_filename, output_filename=None, scale=None):
    
    """
    Grayscale image filter.
    Turn a image of choice given by filename to a grayscale image.
    Implemented with numpy. 
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



def _grayscale(orginal_image):
    
    """
    Grayscales an RGB-image with numpy implementation. 
    
    -----------------------------------------
    Arguments:
        orginal_image : numpy ndarray 
            the orginal image, in RGB, represented as a numpy array
    
    Returns: 
        grayscale_image : numpy ndarray
            The transformed image, in RGB, represented as a numpy array
            
    -----------------------------------------
    """
    R_value = orginal_image[:,:,0] * 0.21
    G_value = orginal_image[:,:,1] * 0.72
    B_value = orginal_image[:,:,2] * 0.07
    
    grayscale_image = R_value + G_value + B_value
       
    return grayscale_image


def timing_numpy_gray(n):
    
    """
    Calls the grayscale function n times and returns the mean time 
    
    Input: int n - number of runs 
    Returns (float): the mean time after n runs 
        
    """
    ts = 0
    for i in range(n):
        t0 = time.perf_counter()
        numpy_color2gray("rain.jpeg", "numpy_rain.jpeg")
        t1 = time.perf_counter()

        ts += (t1-t0)
    
    return ts/n


if __name__ == "__main__":
    
    n = 3
    mean_t = timing_numpy_gray(n)
    mean_python = pyc2g.timing_python_gray(n)
    compare = mean_python/mean_t
    
    f = open("numpy_report_color2gray.txt", "w")
    
    f.write("Timing : numpy_color2gray" 
            "\nAverage runtime running numpy_color2gray after 3 runs : " + str(round(mean_t, 3)) + " s" 
            "\nAverage runtime running of numpy_color2gray is " + str(round(compare, 3)) + " times faster than python_color2gray."
            "\nTiming performed using : time.perf_counter()" 
            "\nimage: 'rain.jpeg' (H, W, C) = (400, 600, 3)")
    
    f.close()
    
    test_scale = numpy_color2gray("rain.jpeg", output_filename = 'scaled_rain_gray.jpeg', scale = 0.5)

    print(round(mean_t, 3))