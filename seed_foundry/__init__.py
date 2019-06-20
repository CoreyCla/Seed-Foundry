import os
from flask import Flask, render_template, request, make_response, jsonify
import stripe
import seed_foundry.prod_mgmt
from . import admin


def create_app(test_config=None):
    # Creates variables for securely storing our API keys. Right now these are the test keys, in the future our live
    # keys will replace these
    stripe_keys = {
        'secret_key': os.environ['SECRET_KEY'],
        'publishable_key': os.environ['PUBLISHABLE_KEY']
    }

    stripe.api_key = stripe_keys['secret_key']

    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template('index.html', key=stripe_keys['publishable_key'])

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/products')
    def products():
        prod_list = prod_mgmt.list_prods(stripe.Product.list())
        return render_template('/products/index.html', prod_list=prod_list)

    @app.route('/products/create', methods=['GET', 'POST'])
    def create_product():
        if request.method == 'POST':
            stripe.Product.create(
                name=request.form['prod_name'],
                type='good',
                description=request.form['prod_description'],
                attributes=[request.form['prod_size'], request.form['prod_color']]
            )
            return render_template('/products/create.html')
        else:
            return render_template('/products/create.html')

    @app.route('/charge', methods=['POST'])
    def charge():
        # Amount in cents
        amount = 500

        customer = stripe.Customer.create(
            email='customer@example.com',
            source=request.form['stripeToken']
        )

        charge = stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description='Flask Charge'
        )

        return render_template('charge.html', amount=amount)

    @app.route('/item')
    def item():
        item_id = request.args.get('item_id')
        prod = stripe.Product.retrieve(item_id)
        # Puts all the SKUs associated with the given product and puts them into a list
        skus = prod_mgmt.list_prod_skus(item_id, stripe.SKU.list())
        # Takes a list of SKUs and returns a list of  dictionaries with all possible attributes
        attr_items = prod_mgmt.list_attr(skus)
        if prod is not None:
            return render_template('/products/item.html', product=prod, attr_items=attr_items)
        else:
            return render_template('/products/index.html')

    @app.route("/item/update-entry", methods=["POST"])
    def update_entry():
        return "Updated!"

    @app.route('/setcookie', methods=['POST'])
    def set_cookie():
        if request.method == 'POST':
            prod_id = request.form['prod_id']
            # Sets variable to a dictionary that contains all SKUs
            prod_list = prod_mgmt.dict_prods(stripe.SKU.list())
            if request.cookies.get(prod_id):
                return render_template('/cart.html')
            else:
                if prod_mgmt.find_spec_id(prod_id, prod_list):
                    sku_obj = prod_mgmt.find_spec_prod(prod_id, prod_list)
                    resp = make_response(render_template('/cart.html'))
                    resp.set_cookie(prod_id, sku_obj)
                else:
                    raise NameError('Bad API call. Product SKU is not available or is incorrect.')
                return resp
        else:
            return render_template('/cart.html')

    @app.route('/cart')
    def cart():
        cart_items = prod_mgmt.get_cookies()
        # print(cart_items)
        prod_mgmt.get_cookies()
        return render_template('/cart.html', cart_items=cart_items)

    app.register_blueprint(admin.bp)

    return app
