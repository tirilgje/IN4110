import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytest


from instapy import grayscale_image, sepia_image


@pytest.mark.parametrize("implementation", ("python", "numpy", "numba"))
def test_grayscale(implementation):
    """
    
    Tests that all implementations of gray_scale filter works as expected
    - tests the shape of the filtered image 
    - tests a random value of the filtered image 
    
    """

    #Generate a 3D numpy array with pixel values randomly choosen between 0 and 255
    np.random.seed(4110)
    low = 0
    high = 255
    N = 100
    
    # low (inclusive), high (exclusive)
    test_image = np.random.randint(low, high + 1, size=(N, N, 3)).astype("uint8")
    
    #Create a random test image 
    cv2.imwrite("test_image.jpg", test_image)
    test_image = cv2.imread("test_image.jpg")
    
    #Choose a random pixel
    idx = np.random.randint(N, size=2)
    i = idx[0]
    j = idx[1]
    
    #Using numpy to calculate the expected value
    expected_value = test_image[i, j, :] @ np.array([0.07, 0.72, 0.21])
    
    #Scale the image with the choosen implementation 
    test_gray_image = grayscale_image("test_image.jpg", implementation=implementation)


    if implementation == "numpy":
        #the numpy implementation should return a 2D array with shape NxN
        assert test_image.shape != test_gray_image.shape
        assert len(test_gray_image.shape) == 2
        assert test_gray_image[i, j] == int(expected_value)
    else:
        #The other implementations returns a 3D array with shape NxNx3.
        assert test_image.shape == test_gray_image.shape
        assert len(test_gray_image.shape) == 3
        assert test_gray_image.shape[2] == 3
        assert test_gray_image[i,j,0] == int(expected_value)
        assert test_gray_image[i,j,1] == int(expected_value)
        assert test_gray_image[i,j,2] == int(expected_value)




@pytest.mark.parametrize("implementation", ("python", "numpy", "numba"))
def test_sepia(implementation):
    """
    Tests that all implementations of sepia_scale works as expected. 
    - tests the shape
    - tests a random value of the filtered image 
    """
    
    #Generate a 3D numpy array with pixel values randomly choosen between 0 and 255
    np.random.seed(4110)
    low = 0
    high = 255
    N = 100
    
    # low (inclusive), high (exclusive)
    test_image = np.random.randint(low, high + 1, size=(N, N, 3)).astype("uint8")
    
    #Create a random test image 
    cv2.imwrite("test_image.jpg", test_image)
    test_image = cv2.imread("test_image.jpg")
    
    # expected random pixel value
    idx = np.random.randint(N, size=3)
    i = idx[0]
    j = idx[1]

    sepia_matrix = np.array([[0.131, 0.534, 0.272],
                             [0.168, 0.686, 0.349],
                             [0.189, 0.769, 0.393]])
    
    expected = (test_image[i, j, :] @ sepia_matrix.T).astype("uint8")
    expected[np.where(expected > 255)] = 255

    test_sepia_image = sepia_image("test_image.jpg", implementation=implementation)

    # Test shape 
    assert test_sepia_image.shape == test_image.shape
    assert test_sepia_image.shape[2] == 3
    
    #test random value(s)
    assert np.array_equal(test_sepia_image[i, j, :], expected)
    
    assert test_sepia_image[i,j,0] == expected[0]
    assert test_sepia_image[i,j,1] == expected[1]
    assert test_sepia_image[i,j,2] == expected[2]
