from secure_shopping_cart import *
import re 
import pytest

"""Testing utility functions""" 

#Testing sku checker function
def test_is_sku_format_valid():
    # Valid SKU format
    assert is_sku_format("ABC_DEF_21") == True
    assert is_sku_format("XYZ_GHI_99") == True

def test_is_sku_format_invalid():
    # Invalid SKU format
    assert is_sku_format("abc_def_21") == False  # Lowercase letters
    assert is_sku_format("ABC_DEF_2") == False  # Missing digit
    assert is_sku_format("ABC_DEF_210") == False  # Extra digit
    assert is_sku_format("ABC_DEF_") == False  # Missing digit and underscore
    assert is_sku_format("AB_CD_12") == False  # Incorrect format
    
def test_is_sku_format_type_error():
    #Type error for non-string input
    with pytest.raises(TypeError):
        is_sku_format(123)
def test_is_sku_format_empty_string():
    # ValueError for empty string
    with pytest.raises(ValueError):
        is_sku_format("")

def test_is_sku_format_none():
    # ValueError for None input
    with pytest.raises(TypeError):
        is_sku_format(None)

def test_is_sku_format_whitespace():
    # ValueError for whitespace-only string
    with pytest.raises(ValueError):
        is_sku_format("    ")

#Testing customer id format checker function 
# # Valid CID format examples
# valid_cids = ['ABC12345DE-A', 'XYZ98765FG-Q']

# Invalid CID format examples
# invalid_cids = ['AB123456DE-A', 'ABC12345DE-F', 'XYZ98765FG-AQ', '12345DE-A', 'ABC12345DE-1']

def test_valid_cids():
    valid_cids = ['ABC12345DE-A', 'XYZ98765FG-Q']
    for cid in valid_cids:
        assert is_cid_format(cid) == True

def test_invalid_cids():
    invalid_cids = ['AB123456DE-A', 'ABC12345DE-F', 'XYZ98765FG-AQ', '12345DE-A', 'ABC12345DE-1']
    for cid in invalid_cids:
        assert is_cid_format(cid) == False

#Testing string checker function
def test_validatedString_valid():
    # Valid string within maxLength
    assert validatedString("Hello") == "Hello"
    assert validatedString("Lorem ipsum dolor sit amet") == "Lorem ipsum dolor sit amet"
    
def test_validatedString_exceed_max_length():
    # String exceeds maxLength
    with pytest.raises(ValueError):
        validatedString("This is a very long string that exceeds the maximum length", maxLength=20)
    
def test_validatedString_empty_string():
    # Empty string
    assert validatedString("") == ""

def test_validatedString_non_string_value():
    # Non-string value
    with pytest.raises(TypeError):
        validatedString(123)
        
def test_validatedString_custom_max_length():
    # Valid string with custom maxLength
    assert validatedString("Hello", maxLength=10) == "Hello"
    assert validatedString("Lorem ipsum", maxLength=20) == "Lorem ipsum"

def test_validatedString_none_value():
    # None value
    with pytest.raises(TypeError):
        validatedString(None)


#Testing Number validation function 
def test_validateNumber_valid():
    # Valid numbers within bounds
    assert validateNumber(5.0) == 5.0
    assert validateNumber(50.0) == 50.0

def test_validateNumber_greater_than_max():
    # Number greater than maxLen
    with pytest.raises(ValueError):
        validateNumber(200.0)

def test_validateNumber_non_number_value():
    # Non-number value
    with pytest.raises(TypeError):
        validateNumber("not a number")

def test_validateNumber_equal_to_min():
    # Number equal to minLen
    assert validateNumber(0.0) == 0.0

def test_validateNumber_equal_to_max():
    # Number equal to maxLen
    assert validateNumber(100.0) == 100.0


#Testing SKU class 
def test_SKU_valid():
    # Valid SKU code
    sku = SKU("ABC_DEF_21")
    assert str(sku) == "SKU code: ABC_DEF_21"

def test_SKU_invalid_type():
    # Invalid SKU code type
    with pytest.raises(TypeError):
        SKU(123)

def test_SKU_invalid_format():
    # Invalid SKU code format
    with pytest.raises(ValueError):
        SKU("invalid_sku_code")

def test_SKU_private_code():
    # Accessing private __code attribute
    sku = SKU("ABC_DEF_21")
    with pytest.raises(AttributeError):
        sku.__code


#Testing Quantity class
def test_Quantity_valid():
    # Valid quantity
    quantity = Quantity(5)
    assert quantity.get_value() == 5

def test_Quantity_invalid_type():
    # Invalid quantity type
    with pytest.raises(TypeError):
        Quantity("invalid")

def test_Quantity_invalid_value():
    # Invalid quantity value
    with pytest.raises(ValueError):
        Quantity(0)

#Testing Item class
def test_Item_valid():
    # Valid item
    item = Item("ABC_DEF_21", "Widget", 10.0)
    assert item.get_sku() == "ABC_DEF_21"
    assert item.get_description() == "Widget"
    assert item.get_price() == 10.0

def test_Item_invalid_sku():
    # Invalid SKU
    with pytest.raises(ValueError):
        Item("invalid_sku", "Widget", 10.0)

def test_Item_invalid_description():
    # Invalid description
    with pytest.raises(TypeError):
        Item("ABC_DEF_21", 33, 10.0)
        
def test_Item_invalid_price():
    # Invalid price
    with pytest.raises(ValueError):
        Item("ABC_DEF_21", "Widget", -10.0)

def test_SKU_private_attributes():
    # Accessing private __code attribute
    item = Item("ABC_DEF_21", "Widget", 10.0)
    with pytest.raises(AttributeError):
        item.__sku
    with pytest.raises(AttributeError):
        item.__description
    with pytest.raises(AttributeError):
        item.__price
        
#Testing CustomerID class
def test_valid_cids():
    valid_cids = ['ABC12345DE-A', 'XYZ98765FG-Q']
    for cid in valid_cids:
        customer_id = CustomerId(cid)
        assert customer_id._CustomerId__value == cid

def test_invalid_cids():
    invalid_cids = ['AB123456DE-A', 'ABC12345DE-F', 'XYZ98765FG-AQ', '12345DE-A', 'ABC12345DE-1']
    for cid in invalid_cids:
        with pytest.raises(ValueError):
            CustomerId(cid)

def test_non_string_value():
    with pytest.raises(TypeError):
        CustomerId(12345)
        
#Testing catalog class 
def test_valid_sku_from_catalog():
    sku = 'ABC_DEF_21'
    assert catalog.validatedHas(sku) is None

def test_invalid_sku():
    sku = 'INVALID_SKU'
    with pytest.raises(ValueError):
        catalog.validatedHas(sku)

def test_immutable_catalog():
    with pytest.raises(TypeError): #'mappingproxy' object does not support item assignment
        catalog.items['ABC_DEF_21'] = Item('ABC_DEF_21','modified apple', 1.0)
    
    with pytest.raises(AttributeError):
        catalog.items.pop('ABC_DEF_21')

    with pytest.raises(AttributeError):
        catalog.items.clear()

#Testing Inventory class 
def test_validate_has():
    # Test for valid SKU and sufficient inventory
    inventory.validateHas('ABC_DEF_21', 50)  # No exception should be raised

    # Test for invalid SKU
    with pytest.raises(ValueError):
        inventory.validateHas('INVALID_SKU', 50)  # Should raise ValueError

    # Test for insufficient inventory
    with pytest.raises(ValueError):
        inventory.validateHas('ZZZ_BOB_77', 250)  # Should raise ValueError

def test_immutable_inventory():
    # Attempt to modify the items dictionary
    with pytest.raises(TypeError):
        inventory.items['ABC_DEF_21'] = 50  

    with pytest.raises(TypeError):
        del inventory.items['ABC_DEF_21']  

    with pytest.raises(AttributeError):
        inventory.items.clear()  

    with pytest.raises(AttributeError):
        inventory.items.update({'ZZZ_BOB_77': 250})  # Should raise AttributeError

    with pytest.raises(AttributeError):
        inventory.items.pop('ABC_DEF_21')  # Should raise AttributeError

    with pytest.raises(AttributeError):
        inventory.items.popitem()  # Should raise AttributeError
