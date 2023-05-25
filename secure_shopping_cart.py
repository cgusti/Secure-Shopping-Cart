"""
CMSI 662 Homework I: Secure shopping cart application
Author: Claudia Gusti 
Date: 5/19/23
"""
import copy
import re
from dataclasses import dataclass
import uuid
import types

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


def is_cid_format(customer_id):
    """Helper function to validate if a given customer id satisfies all requirements 

    Args:
        customer_id (str): candidate customer id

    Returns:
        Bool: returns True if customerID string satisfies all requirements
    """
    pattern = r'^[A-Z]{3}\d{5}[A-Z]{2}-[AQ]$'
    match = re.match(pattern, customer_id)
    return match is not None

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


class SKU:
    """
    SKU containing SKU code (unique identifier for each item available at the store)
    """
    def __init__(self, code):
        self.__code = SKU.validated(code)
        
    @staticmethod
    def validated(code):
        """validates if sku code is in the proper format and is a string, if so return correct and validated code"""
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


class CustomerId: 
    """Customer ID class containing customer id validators that are employed during construction time"""
    def __init__(self, value):
        self.__value = CustomerId.validated(value)
    @staticmethod
    def validated(value):
        if type(value) != str: 
            raise TypeError('Customer ID must be a string')
        if not is_cid_format(value):
            raise ValueError('Customer ID is in the wrong format')
        return value
    

@dataclass(frozen=True)
class Catalog:
    """catalog containing a mapping of all available unique product SKUs at the store to Item object

    Raises:
        ValueError: If given SKU does not match any SKUs contained in the catalog
    """
    items: types.MappingProxyType
    
    def validatedHas(self, sku):
        if sku not in self.items:
            raise ValueError('Invalid SKU {sku}')

#creating an instance of constant and immutable catalog. It is important to note 
#here that even though the Catalog class is marked as frozen=True, but the items attribute is a dictionary. 
# While the Catalog instance itself is immutable, the dictionary object it contains can still be modified
catalog = Catalog(types.MappingProxyType({
    'ABC_DEF_21': Item('ABC_DEF_21','one apple fruit', 0.5),
    'ZZZ_BOB_77': Item('ZZZ_BOB_77','one watermelon fruit', 10.0),
    'YYY_JIL_77': Item('YYY_JIL_77','100g of of USA Wagyu meat', 12.0),
    'WWW_BIL_77': Item('WWW_BIL_77','1 carton of Oatly oat milk', 6.0),
}))

#TESTED - DONE
@dataclass(frozen=True)
class Inventory:
    """Inventory to keep track of quantities of unique products/SKUs sold at the store

    Raises:
        ValueError: If SKU is invalid (not contained in the Inventory)
        ValueError: If there is not enough inventory for a unique SKU
    """
    items: types.MappingProxyType
    
    def validateHas(self, sku, desiredQuantity):
        #check if sku exists 
        if sku not in self.items:
            raise ValueError(f'Invalid SKU: {sku}')
        #check if there is enough inventory
        if self.items[sku] < desiredQuantity: 
            raise ValueError(f'Not enough inventory for SKU: {sku}')

inventory = Inventory(types.MappingProxyType({
    'ABC_DEF_21': 100,
    'ZZZ_BOB_77': 200,
    'YYY_JIL_77': 300,
    'WWW_BIL_77': 400,
}))

class ShoppingCart:
    def __init__(self, customerId):
        """
        Shopping cart class that is identified by a unique cart_id, customer_id 
        and contains items 
        Args:
            customerId (str): unique customer identifier
        """
        self.__id = uuid.uuid4()
        self.__customer_id = CustomerId.validated(customerId)
        self.__items = {}
        
    def get_id(self):
        return self.__id
    
    def get_customer_id(self):
        return self.__customer_id
    
    def get_items(self): #Must return a deep copy of items because item attribute is mutable
        return copy.deepcopy(self.__items)
    
    def add_items(self, sku, quantity):
        SKU.validated(sku)
        catalog.validatedHas(sku)
        Quantity.validated(quantity)
        #Quick check that we have enough inventory; however, since we 
        #don't have a transactional boundary here, we can't guarantee that the 
        #inventor wont' change between this check and the time we actually add the items
        #to the cart. 
        #A final check will be made the the checkout time, so this is ok for now
        inventory.validateHas(sku, quantity)
        #check if item already exists in cart
        if sku in self.__items:
            self.__items[sku] += quantity 
        else: 
            self.__items[sku] = quantity
        
    def updateItemQuantity(self, sku, quantity):
        SKU.validated(sku)
        catalog.validatedHas(sku)
        Quantity.validated(quantity)
        self.__items.update({sku : quantity}) 
    
    def removeItem(self, sku):
        SKU.validated(sku)
        del self.__items[sku]
    
    def calculateTotalCost(self):
        total = 0
        for sku, quantity in self.__items.items():
            item = catalog.items.get(sku) #take not that a MappxingProxy object is not subscriptable
            total += item.get_price() * quantity
        return total
    
    
    
