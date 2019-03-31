from flask import request


# Returns a list of Stripe product ids
def find_prod_ids(prod_dict):
    list_out = []
    for k in prod_dict:
        list_out.append(k.id)
    return list_out


# Returns all of the sku objects associated with a product id
# Takes a dictionary ( obtained with stripe.SKU.list() ) and the product id as arguments
def retrieve_skus_for_product(sku_dict, product_id):
    product_skus = []  # all found skus for the product id

    for s in sku_dict:
        if s['product'] == product_id:
            product_skus.append(s)
    return product_skus


# This function requires only one API call. Previously the function made a separate API call for each product, and also
# returned SKUs. For the product page we only need product objects. This can be used to sort SKUs as well.
# It takes the
# *** Create logic for checking if the SKU is set to "Active" before returning the list.
def list_prods(prods):
    prod_list = []
    for k, v in prods.items():
        if k == 'data':
            prod_list = v
    return prod_list


# Similar to list_prods from above, but it returns a dictionary with product IDs as keys and product objects as values
def dict_prods(prods):
    prod_dict = {}
    if isinstance(prods, list):
        for i in prods:
            if isinstance(i, dict) and i['id'] in i.keys():
                x = i['id']
                prod_dict[x] = i
    elif isinstance(prods, dict):
        for k, v in prods.items():
            if 'id' in prods.keys():
                x = prods['id']
                prod_dict[x] = v
            elif isinstance(v, dict):
                dict_prods(v)
    else:
        raise TypeError('This method can only accept lists or dictionaries as its input.')
    return prod_dict

# Takes an ID as input and returns true if it is in a list of product objects
# *** Doesnt work ***
# def find_spec_id(prod_id, prod_list):
#     for i in prod_list:
#         if prod_id in i.values():
#             return True
#         else:
#             return False


# Function takes an ID and a dictionary then returns true if the product is in that dictionary. Particularly useful
# if used in conjuction with the dict_prods/list_prods functions.
def find_spec_id(prod_id, prod_dict):
    for i in prod_dict:
        if prod_id in i.keys():
            return True
        else:
            return False


# Takes an ID as input and returns the object associated with the id, or false if it doesn't exist
def find_spec_prod(prod_id, prod_list):
    for i in prod_list:
        if prod_id in i.values():
            return i
        else:
            return False


# Returns all the product item cookies
def retrieve_cart():
    cart_items = []
    for i in request.cookies:
        print(i)
        if i.startswith('prod') or i.startswith('sk'):
            cart_items.append(i)
    return cart_items

