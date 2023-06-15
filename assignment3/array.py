from functools import reduce

class Array:

    def __init__(self, shape, *values):
        """
        
        Initialize an array of 1-dimensionality. Elements can only be of type:
        - int
        - float
        - bool
        
        Make sure that you check that your array actually is an array, which means it is homogeneous (one data type).

        Args:
            shape (tuple): shape of the array as a tuple. A 1D array with n elements will have shape = (n,).
            *values: The values in the array. These should all be the same data type. Either numeric or boolean.

        Raises:
            ValueError: If the values are not all of the same type.
            ValueError: If the number of values does not fit with the shape.
        """
        #Define the shape and the array as a flat array
        self._shape = shape
        self._array = values
        
        #Sets with vaild types of values 
        self._valid_types = {int, float, bool}
        self._valid_numerical_types = {int, float}
        
        #Check if number of items fits the given shape (works for nD arrays)
        sum_of_items = reduce(lambda x, y: x*y, self._shape)
        if sum_of_items != len(self._array):
            raise ValueError("Number of values (" + str(len(self._array)) + 
                             ") does not fit with the shape (" + str(self._shape) + ").")
                  
        # Check if the values are of valid type
        my_types = set()
        
        for item in self._array: 
            if type(item) in self._valid_types:
                my_types.add(type(item))
                
                if len(my_types) > 1:
                    raise ValueError("Values are not all of the same type")       
            else:
                raise ValueError("Array contains unvalid type of value")       
        
        # Optional: If not all values are of same type, all are converted to floats.
            
        
    def __str__(self):
                        
        """Returns a nicely printable string representation of the array.

        Returns:
            str: A string representation of the array.

        """ 
        #Save time if the array is 1D, nD arrays needs to show correct shape
        if len(self._shape) == 1:
            shaped_array = self._array
        else:
            shaped_array = self._build_array(self._shape, list(self._array))
            
        return str(shaped_array)
    
    
    def __getitem__(self, item):
        """
        Returns value of item in array.
         Args:
            item (int): Index of value to return.
         Returns: 
            value: Value of the given item.
            
        """ 
        #Save time if the array is 1D, nD arrays needs to show correct shape
        if len(self._shape) == 1:
            shaped_array = self._array
        else:
            shaped_array = self._build_array(self._shape, list(self._array))
        
        return shaped_array[item]
             
    
    def __add__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """
        
        # check that the method supports the given arguments (check for data type and shape of array)  
         
        new_array = Array((0,))
        
        if type(other) in self._valid_numerical_types:
            new_values = tuple(map(lambda x: x + other, self._array))

        elif type(other) == Array:
            if self._shape == other._shape: 
                new_values = tuple(map(lambda x, y: x + y, self._array, other._array))

            else:
                raise ValueError("Shapes does not match, ", self._shape, other._shape, ".")
        else: 
            return NotImplemented
            
        new_array._shape = self._shape
        new_array._array = new_values
               
        return new_array
    
    def __radd__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """                
        return self.__add__(other)
    
    
    def __sub__(self, other):
        """Element-wise subtracts an Array or number from this Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to subtract element-wise from this array.

        Returns:
            Array: the difference as a new array.

        """
        
        new_array = Array((0,))
        
        if type(other) in self._valid_numerical_types:
            new_values = n4 = tuple(map(lambda x: x - other, self._array))
            
        elif type(other) == Array:
            if self._shape == other._shape:
                new_values = tuple(map(lambda x, y: x - y, self._array, other._array))
                
            else:
                raise ValueError("Shapes does not match, ", self._shape, other._shape, ".")
        else: 
            return NotImplemented 
        
        new_array._shape = self._shape
        new_array._array = new_values
               
        return new_array
    
    
    def __rsub__(self, other):
        """Element-wise subtracts this Array from a number or Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number being subtracted from.

        Returns:
            Array: the difference as a new array.

        """
        return self.__sub__(other)
    
    
    def __mul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
         
        new_array = Array((0,))
        
        if type(other) in self._valid_numerical_types:
            new_values = tuple(map(lambda x: x * other, self._array))
        elif type(other) == Array:
            if self._shape == other._shape: 
                new_values = tuple(map(lambda x, y: x * y, self._array, other._array))

            else:
                raise ValueError("Shapes does not match, ", self._shape, other._shape, ".")
        else: 
            return NotImplemented
            
        new_array._shape = self._shape
        new_array._array = new_values
               
        return new_array
    
    
    def __rmul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
 
        # Hint: this solution/logic applies for all r-methods
        return self.__mul__(other)
    
    
    def __eq__(self, other):
        """Compares an Array with another Array.

        If the two array shapes do not match, it should return False.
        If `other` is an unexpected type, return False.

        Args:
            other (Array): The array to compare with this array.

        Returns:
            bool: True if the two arrays are equal (identical). False otherwise.

        """
        
        if (type(other) == Array) and (self._shape == other._shape) and (self._array == other._array): 
            return True 
        else:
            return False 

        

    def is_equal(self, other):
        """Compares an Array element-wise with another Array or number.

        If `other` is an array and the two array shapes do not match, this method should raise ValueError.
        If `other` is not an array or a number, it should return TypeError.

        Args:
            other (Array, float, int): The array or number to compare with this array.

        Returns:
            Array: An array of booleans with True where the two arrays match and False where they do not.
                   Or if `other` is a number, it returns True where the array is equal to the number and False
                   where it is not.

        Raises:
            ValueError: if the shape of self and other are not equal.

        """
        if not (type(other) in self._valid_numerical_types or type(other) == Array):
            raise TypeError("Type is not supported")
            
        if type(other) == Array and self._shape != other._shape:
            raise ValueError("Shapes does not match, ", self._shape, other._shape, ".")
                    
        new_array = Array((0,))
        
        if type(other) in self._valid_numerical_types:
            new_values = tuple(map(lambda x: x == other, self._array))
                    
        elif type(other) == Array:
            new_values = tuple(map(lambda x, y: x == y, self._array, other._array))
      
        
        new_array._shape = self._shape
        new_array._array = new_values
        
        return new_array
    

    def min_element(self):
        """Returns the smallest value of the array.

        Only needs to work for type int and float (not boolean).

        Returns:
            float: The value of the smallest element in the array.

        """
        if self._shape[0] == 0:
            raise ValueError("() is an empty Array")
        elif not (type(self._array[0]) in self._valid_numerical_types):
            raise ValueError("Array does not contain numerical values")
        else:
            return float(min(self._array))

    
        
    def _build_array(self, shape_array, flat_list):
        """
        Returns flat_list as a nested tuple with shape described by shape_array
        shape_array must match number of items in flat list. 
        
        (We can assume that the input is correct because this method should only be called inside the class Array) 
        
        Args:
            shape_array (tulpe): The shape the funcion shuld return 
            flat_list (list): The array in list-form
            
        Returns (tulple): A tulpe with the elements in flat_list shaped in the dimentions of shape_array. 
       
        """

        shaped = []
        for _ in range(shape_array[0]):
            if len(shape_array) == 1: 
                shaped.append(flat_list.pop(0))
            else:
                shaped.append(self._build_array(shape_array[1:], flat_list))
        return tuple(shaped)