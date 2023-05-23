"""
CMSI 662 Homework I: Secure shopping cart application
Author: Claudia Gusti 
Date: 5/19/23
"""
import copy
import re

def is_sku_format(sku_code):
    """Helper function to validate if a string is in proper SKU format

    Args:
        sku_code (str): input sku code 

    Returns:
        Bool : whether or not input sku code is in the proper format or not
    """
    pattern = r'^[A-Z]{3}_[A-Z]{3}_\d{2}$'
    match = re.match(pattern, sku_code)
    return match is not None

class SKU:
    """
    SKU containing SKU code (unique identifier for each item available at the store)
    """
    def __init__(self, code):
        self.__code = SKU.validated(code)
        
    @staticmethod
    def validated(code):
        """validates if sku code is in the proper format and is a string, if so return code"""
        if type(code) != str:
            raise TypeError('SKU code must be a string')
        if not is_sku_format(code):
            raise ValueError('SKU code must be formatted correctly')
        return code
    
    def __str__(self):
        """Return a printed string of sku code"""
        return f'SKU code: {self.__code}'

class Quantity:
    """
    Quantity class that to signify how much of an item is contained in the shopping cart
    """
    def __init__(self, value):
        self.__value = Quantity.validated(value)
    
    @staticmethod
    def validated(value):
        """Helper method to validate/establish bounds that the quanity of an item

        Args:
            value (int): number of items input into the shopping cart

        Returns:
            value : correct numerical quantity of an item to be input to the shopping cart
        """
        if (type(value) != int):
            raise TypeError('Quantity must be an integer')
        if (value <= 0): 
            raise ValueError('Quantity must be greater than 0')
        return value

def validatedString(value, maxLength=1000):
    """
    Helper function to validate that am input is within bounds and 
    is of type string
    """
    if (type(value) != str): 
        raise TypeError('Value must be a string')
    if (value.length > maxLength):
        raise ValueError(f'Value must be no more than {maxLength} characters')
    return value

def validateNumber(value, minLen=1, maxLen=10):
    """
    Helper function to validate that a number input is within bounds and 
    is of type integer
    """
    if (type(value) != int):
        raise TypeError('value of must be a number')
    if (value < minLen): 
        raise ValueError(f'Value must be at least {minLen}')
    if (value > maxLen):
        raise ValueError(f'Value must be at most ${maxLen}')
    return value

class Item: 
    """
    Item class that consists of a unique SKU identifier, description of the
    item and price of one unit of the item
    """
    def __init__(self, sku, description, price):
        self.__sku = SKU.validated(sku)
        self.__description = validatedString(description)
        self.__price = validateNumber(price)
    def get_sku(self):
        return self.__sku
    def get_description(self):
        return self.__description
    def get_price(self):
        return self.__price

class ShoppingCart:
    def __init__(self, cart_id, customerId, items):
        """
        Shopping cart class that is identified by a unique cart_id, customer_id 
        and contains items 
        Args:
            cart_id (str): unique cart identifier
            customerId (str): unique customer identifier
            items (list): list of items currently in the shopping cart
        """
        self.__id = cart_id
        self.__customer_id = customerId
        self.__items = items
        
    def get_id(self):
        return self.__id
    
    def get_customer_id(self):
        return self.__customer_id
    
    def get_items(self): #Must return a deep copy of items 
        return copy.deepcopy(self.__items)
    
    def updateItemQuantity(sku, quantity):
        pass
    

    
    


