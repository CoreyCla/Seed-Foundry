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


# Similar to list_prods from above, but it returns a dictionary with product IDs as keys and SKU objects as values
def dict_prods(prods):
    if isinstance(prods, list):
        prod_dict = {}
        for i in prods:
            x = i['id']
            prod_dict[x] = i
        return prod_dict
    elif isinstance(prods, dict):
        if 'data' in prods.keys():
            x = prods['data']
            return dict_prods(x)
    else:
        raise TypeError('This method can only accept lists or dictionaries as its input.')


# Function takes an ID and a dictionary then returns true if the product is in that dictionary. Particularly useful
# if used in conjuction with the dict_prods/list_prods functions.
def find_spec_id(prod_id, prod_dict):
    for i in prod_dict:
        if prod_id in i.keys():
            return True
        else:
            return False


# Takes an ID and a list of products as input and returns the object associated with the id, or false if it doesn't
# exist
def find_spec_prod(prod_id, prod_list):
    for i in prod_list:
        if prod_id in i.values():
            return i
        else:
            return False


# This function takes a product id and a dictionary of all SKUs, then returns list of all the SKUs that have that
# product as their base product. If no product exists, it returns false.
def list_prod_skus(prod_id, skus):
    if 'data' in skus.keys():
        skus_list = []
        for i in skus['data']:
            if i['product'] == prod_id:
                skus_list.append(i)
        return skus_list
    else:
        return False


# Takes a list of SKUs, then returns a dictionary with the key being the attribute, and the value being a list of
# possible attribute options. Should only be used if the list of SKUs is attached to a single base product. Otherwise
# the user will be given attribute combinations that won't return a SKU object.
def list_attr(sku_dict):
    sku_attr_list = {}
    for i in sku_dict:
        for k, v in i['attributes'].items():
            if k not in sku_attr_list.keys():
                sku_attr_list[k] = [v]
            else:
                # Ensures that there are no duplicates
                if v not in sku_attr_list[k]:
                    sku_attr_list[k].append(v)
    return sku_attr_list


# Takes a list of SKU objects and an attribute, then returns a list of SKU objects that have that attribute
def sku_by_attr(attr, skus):
    if isinstance(skus, dict):
        for k, v in skus['attributes'].items():
            if attr in v:
                return skus
    elif isinstance(skus, list):
        new_skus = []
        for i in skus:
            if attr == i:
                new_skus.append(i)
            else:
                new_skus.append(sku_by_attr(attr, i))
        return new_skus


# Returns all the product item cookies.
def retrieve_cart():
    cart_items = []
    for i in request.cookies:
        print(i)
        if i.startswith('prod') or i.startswith('sk'):
            cart_items.append(i)
    return cart_items

