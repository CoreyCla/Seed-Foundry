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


