# Returns a list of Stripe product ids
def find_prod_ids(prod_dict):
    list_out = []
    for k in prod_dict:
        list_out.append(k.id)
    return list_out
