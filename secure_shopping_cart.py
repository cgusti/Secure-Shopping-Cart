"""
CMSI 662 Homework I: Secure shopping cart application
Author: Claudia Gusti 
Date: 5/19/23
"""
import copy
import re
from dataclasses import dataclass

#Tested - DONE
def is_sku_format(sku_code): 
    """Helper function to validate if a string is in proper SKU format
    Args:
        sku_code (str): input sku code 

    Returns:
        Bool : whether or not input sku code is in the proper format or not
    """
    if (type(sku_code)) != str:
        raise TypeError('sku code needs to be a string')
    if not len(sku_code):
        raise ValueError('String is empty')
    if sku_code.isspace():
        raise ValueError('SKU cannot be an empty string')
    pattern = r'^[A-Z]{3}_[A-Z]{3}_\d{2}$'
    match = re.match(pattern, sku_code)
    return match is not None

#Tested - DONE
def validatedString(value, maxLength=100):
    """
    Helper function to validate that am input is within bounds and 
    is of type string
    Args: 
        value (int)
        maxLength (int)
    Returns: 
        int: 
    """
    if (type(value) != str): 
        raise TypeError('Value must be a string')
    if (len(value) > maxLength):
        raise ValueError(f'Value must be no more than {maxLength} characters')
    if value is None: 
        raise TypeError('Need to input string')
    return value

#Tested - DONE
def validateNumber(value, minVal=0.0, maxVal=100.0):
    """
    Helper function to validate that a number input is within bounds and 
    is of type integer
    """
    if (type(value) != float):
        raise TypeError('value of must be a number')
    if (value < minVal): 
        raise ValueError(f'Value must be at least {minVal}')
    if (value > maxVal):
        raise ValueError(f'Value must be at most ${maxVal}')
    return value

#Tested - DONE
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
    
    def get_value(self):
        return self.__value

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
    
@dataclass(frozen=True)
class Catalog: 
    items: dict
    
    def validatedHas(self, sku):
        if sku not in self.items:
            raise ValueError('Invalid SKU {sku}')

#creating an instance of constant and immutable catalogy
catalog = Catalog({
    'Apples': Item("ABC_DEF_21",'one apple fruit', 0.5),
    'Watermelon': Item("ZZZ_BOB_77",'one watermelon fruit', 10.0),
    'Wagyu meat': Item("YYY_JIL_77",'100g of of USA Wagyu meat', 12.0),
    'Oatly oat milk': Item("WWW_BIL_77",'1 carton of Oatly oat milk', 6.0),
})

class ShoppingCart:
    def __init__(self, cart_id, customerId):
        """
        Shopping cart class that is identified by a unique cart_id, customer_id 
        and contains items 
        Args:
            cart_id (str): unique cart identifier
            customerId (str): unique customer identifier
            items (dict): list of items currently in the shopping cart
        """
        self.__id = cart_id
        self.__customer_id = customerId
        self.__items = {}
        
    def get_id(self):
        return self.__id
    
    def get_customer_id(self):
        return self.__customer_id
    
    def get_items(self): #Must return a deep copy of items 
        return copy.deepcopy(self.__items)
    
    def add_items(self, sku, quantity):
        SKU.validated(sku)
        catalog.validatedHas(sku)
        Quantity.validated(quantity)
        self.__items.update(sku, quantity)
        
    def updateItemQuantity(self, sku, quantity):
        SKU.validated(sku)
        catalog.validatedHas(sku)
        Quantity.validated(quantity)
        self.__items.update({sku, quantity}) 
        
    def calculateTotalCost(self):
        total = 0
        for item, quantity in self.__items():
            total += quantity.get_value()
        return total
    
       
    


