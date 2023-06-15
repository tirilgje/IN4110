from .python_filters import python_color2gray, python_color2sepia
from .numpy_filters import numpy_color2gray, numpy_color2sepia
from .numba_filters import numba_color2gray, numba_color2sepia
#from.cython_filters import cython_color2gray, cython_color2sepia
import time
import numpy as np



def grayscale_image(input_filename, 
                    output_filename=None, 
                    scale=None, 
                    implementation="numpy",
                    timing_on=False):
    
    """
    Grayscale image filter.
    Turn a image of choice given by filename to a grayscale image.
    Implementation method is given as an agrument. 
    Savnes and returns the transformed image. 
    -----------------------------------------
    Arguments:
        input_filename : str 
            filename or path to the image 
        
        output_filename: str, optinal, default=None 
            filename or path to the transformed image
            
        scale : float, optional, default=None
            Scale factor to resize image. (e.g. 0.5 halves image dimentions)
        
        implementation : str, optional, default="numpy"
            Choose the implementation method, {"python", "numpy", "numba", "cython"}
        
        timing_on : bool, optional, default=False
            If True, the mean time of 3 runs will be printed. 
    
    Returns: 
        grayscale_image : numpy ndarray
            The transformed image with as a numpy array. 
            
    -----------------------------------------
    """
    

        
    map_implementations = {"python": python_color2gray, 
                           "numpy": numpy_color2gray, 
                           "numba":numba_color2gray, 
                           "cython":'cython_color2gray'}
    
    
    if implementation not in map_implementations.keys():
        raise ValueError("Not valid implementation method")
    
    grayscale_image = map_implementations[implementation](input_filename, output_filename, scale)
    
    
    if timing_on:
        tot_t = 0
        for i in range(3):
            t0 = time.perf_counter()
            map_implementations[implementation](input_filename, output_filename, scale)
            t1 = time.perf_counter()
            
            tot_t += (t1-t0)
            
        mean_t = tot_t/3
        
        print("Average runtime over 3 runs: ", round(mean_t,3), "( gray,", implementation, ")") 
    
    
    return grayscale_image

def sepia_image(input_filename, 
                output_filename=None,  
                scale=None, 
                level=1.0,
                implementation="numpy",
                timing_on=False):
    
    
    
    """
    Adds sepia filter to the image.
    Turn a image of choice given by filename to a sepia image.
    Implemented with XXX. 
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
            
        implementation : str, optional, default="numpy"
            Choose the implementation method, {"python", "numpy", "numba", "cython"}
        
        timing_on : bool, optional, default=False
            If True, the mean time of 3 runs will be printed. 
    
    Returns: 
        grayscale_image : numpy ndarray
            The transformed image with as a numpy array. 
            
    -----------------------------------------
    """
    
    """
    Arguments:
        input_filename (str): Filename or path of the image 
        output_filename (str): [optional, None by default] filename or path of the filtred image
        method (str): [optional, "numpy" by default] spesify the implementation method
        
    Returns:
        grayscale_image (numpy ndarray): The filtered image 
        
    """
    
    
    map_implementations = {"python": python_color2sepia, 
                           "numpy": numpy_color2sepia, 
                           "numba":numba_color2sepia, 
                           "cython":'cython_color2sepia'}
    
    
    if implementation not in map_implementations.keys():
        raise ValueError("Not valid implementation method")
    
    sepia_image = map_implementations[implementation](input_filename, output_filename, scale, level)
    
    
    if timing_on:
        tot_t = 0
        for i in range(3):
            t0 = time.perf_counter()
            map_implementations[implementation](input_filename, output_filename, scale, level)
            t1 = time.perf_counter()
            
            tot_t += (t1-t0)
            
        mean_t = tot_t/3
        
        print("Average runtime over 3 runs: ", round(mean_t, 3), "( sepia,", implementation, ")")
            
    return sepia_image




if __name__ == "__main__":
    
    image = "rain.jpeg"
    
    gray_py = grayscale_image(image, output_filename="gray_py.jpeg", implementation="python")
    gray_np = grayscale_image(image, output_filename="gray_np.jpeg", implementation="numpy")
    gray_nb = grayscale_image(image, output_filename="gray_nb.jpeg", implementation="numba")

    sepia_py = sepia_image(image, output_filename="sepia_py.jpeg", implementation="python")
    sepia_np = sepia_image(image, output_filename="sepia_np.jpeg", implementation="numpy")    
    sepia_nb = sepia_image(image, output_filename="sepia_nb.jpeg", implementation="numba")
    
