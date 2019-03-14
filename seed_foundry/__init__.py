import os
from flask import Flask, render_template, request
import stripe
import seed_foundry.prod_mgmt


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
        # Creates a list of product ids to use when retrieving product objects
        prod_ids = prod_mgmt.find_prod_ids(stripe.Product.list())
        prod_list = []
        # Retrieves product objects by id and adds them to prod_list
        for item in prod_ids:
            prod_list.append(stripe.Product.retrieve(item))
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

    from . import admin
    app.register_blueprint(admin.bp)

    return app
