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
        p_name = request.form['name']
        active = request.form['active']
        p_caption = request.form['caption']
        p_description = request.form['description']
        p_image = [request.form['image']]
        p_attribute1 = request.form['attribute1']
        p_attribute2 = request.form['attribute2']
        p_attribute3 = request.form['attribute3']
        p_attribute4 = request.form['attribute4']
        p_attribute5 = request.form['attribute5']

        p_attributes = []
        input_attributes = [p_attribute1, p_attribute2, p_attribute3, p_attribute4, p_attribute5]

        for x in input_attributes:
            if x != "":
                p_attributes.append(x)




        p_active = False

        if active == "true":
            p_active = True

        error = ""

        if not p_name:
            error = 'Please enter a name'
        if not p_description:
            error = 'Please enter a description'
        if not p_caption:
            error = 'Please enter a caption'
        if error == "":
            # do something with product later, return to products page
            stripe.Product.create(
                name=p_name,
                type='good',
                active=p_active,
                description=p_description,
                caption=p_caption,
                images=p_image,
                attributes=p_attributes
            )

            return redirect(url_for('products'))

        flash(error)

    return render_template('admin/createproduct.html')
