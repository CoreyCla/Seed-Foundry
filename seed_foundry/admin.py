from __future__ import print_function
import functools
import os
import stripe

import sys

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('admin', __name__, url_prefix='/admin')

stripe_keys = {
    'secret_key': os.environ['SECRET_KEY'],
    'publishable_key': os.environ['PUBLISHABLE_KEY']
    }

stripe.api_key = stripe_keys['secret_key']


@bp.route('/createproduct', methods=('GET', 'POST'))
def createproduct():
    if request.method == 'POST':
        pName = request.form['name']
        active = request.form['active']
        pCaption = request.form['caption']
        pDescription = request.form['description']
        pImage = [request.form['image']]
        pAttribute1 = request.form['attribute1']
        pAttribute2 = request.form['attribute2']
        pAttribute3 = request.form['attribute3']
        pAttribute4 = request.form['attribute4']
        pAttribute5 = request.form['attribute5']

        pAttributes = []
        inputAttributes = [pAttribute1, pAttribute2, pAttribute3, pAttribute4, pAttribute5]

        for x in inputAttributes:
            if x != "":
                pAttributes.append(x)




        pActive = False

        if active == "true":
            pActive = True

        error = ""

        if not pName:
            error = 'Please enter a name'
        if not pDescription:
            error = 'Please enter a description'
        if not pCaption:
            error = 'Please enter a caption'
        if error == "":
            # do something with product later, return to products page
            stripe.Product.create(
                name=pName,
                type='good',
                active=pActive,
                description=pDescription,
                caption=pCaption,
                images=pImage,
                attributes=pAttributes
            )

            return redirect(url_for('products'))

        flash(error)

    return render_template('admin/createproduct.html')
