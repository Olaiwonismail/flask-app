from flask import render_template, url_for, flash, redirect, request, Blueprint,make_response
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt,bootstrap
import ast,random,string

from app.models import User, Product

 #, send_reset_emai
products= Blueprint('products',__name__)

@products.route("/item/<int:id>")
def item(id):
    product = Product.query.get_or_404(id)
    reviews = ast.literal_eval(product.reviews)
    tags = ast.literal_eval(product.tags)
    list = []
    items = Product.query.all()
    for item in items:
        # print(item.tags)
        if tags[0] in item.tags:
            list.append(item)
        else:
            # print(False)
            pass
    random.shuffle(list)
    list= list[:3]

    return render_template('products/products.html',product = product,reviews=reviews,list = list)


@products.route("/wishlist/<int:id>",methods = ['POST','GET'])
def wishlist(id):
    if current_user.is_authenticated:
        print('successful')
        user = current_user


        product = Product.query.get_or_404(id)
        wishlist = user.wishlist
        wishlist = wishlist +' '+ (str(id))
        user.wishlist = wishlist
        db.session.commit()
        print(user.wishlist)
    else:
        return redirect(url_for('users.login'))
    # return render_template('main/base.html')

@products.route('/wishlist/items/',methods = ['POST','GET'])
@login_required
def wishlist_items():
    user = current_user
    wishlist = user.wishlist
    wishlist = list(map(int,wishlist.split()))
    wishlist = list(set(wishlist))
    wishlist = Product.query.filter(Product.id.in_(wishlist)).all()
    return render_template('products/wishlist.html',wishlist=wishlist)

@products.route('/add_to_cart/<int:id>/',methods = ['POST','GET'])
@login_required
def add_to_cart(id):

    if request.cookies.get('cart'):

        cart = request.cookies.get('cart')
        print(cart)
        response =make_response('    ')
        response.set_cookie('cart',cart+ ' ' +str(id))
        return response
    else:


        response =make_response('   ')
        response.set_cookie('cart',str(id))
        return response

    return 'Done'


@products.route('/cart/',methods = ['POST','GET'])
@login_required
def cart():
    cart = request.cookies.get('cart')
    # print(cart)
    user = current_user
    if cart:
        cart = list(map(int,cart.split()))
        cart = list(set(cart))
        cart = Product.query.filter(Product.id.in_(cart)).all()
    else:
        pass
    return render_template('products/cart.html',cart=cart)

@products.route('/remove_from_cart/<int:id>/',methods = ['POST','GET'])
@login_required
def remove_from_cart(id):
    cart = request.cookies.get('cart')
    print(cart)
    # user = current_user
    if cart:
        cart = list(map(int,cart.split()))
        cart = list(set(cart))


        cart.remove(id)
        cart = ' '.join(map(str,cart))
        response =make_response('   ')
        response.set_cookie('cart',cart)
        return response
    else:
        pass
    return 'Done'
