"""
    Routes
    ~~~~~~
"""
import flask
from flask import Blueprint, make_response
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from product import Product
from wiki.core import Processor
from wiki.web.forms import EditorForm
from wiki.web.forms import LoginForm
from wiki.web.forms import SearchForm
from wiki.web.forms import URLForm
from wiki.web import current_wiki
from wiki.web import current_users
from wiki.web.user import protect

import json
import pickle

bp = Blueprint('wiki', __name__)


@bp.route('/')
@protect
def home():
    page = current_wiki.get('home')
    if page:
        return display('home')
    return render_template('home.html')


@bp.route('/index/')
@protect
def index():
    pages = current_wiki.index()
    return render_template('index.html', pages=pages)


@bp.route('/new_product/')
@protect
def new_product():
    return render_template('new_product.html')


@bp.route('/product_info', methods=['POST'])
def product_info():
    output = request.get_json()
    result = json.loads(output) # this converts the json output to a python dictionary

    i = 1
    tempTitle = ""
    tempDescription = ""
    tempPrice = ""
    tempBought = ""

    items = ""
    # Assigns values from the dictionary stored in the variable result
    # to their corresponding variable.
    for item in result:
        items += str(result[item]) + " "
        if i == 1:
            tempTitle = result[item]
        elif i == 2:
            tempDescription = result[item]
        elif i == 3:
            tempPrice = result[item]

        else:
            tempBought = result[item]

        i += 1

    Product.productList.clear()
    Product(tempTitle, tempDescription, tempPrice, tempBought)

    # The following code bellow is for data persistance
    pickle_infile = open("productData.pkl", "rb")
    pickle_file = pickle.load(pickle_infile)
    for data in pickle_file:
        Product.productList.append(data)

    # empty_list = []
    # overwrites pickle with productList
    pickle_outfile = open("productData.pkl", "wb")
    pickle.dump(Product.productList, pickle_outfile)
    # pickle.dump(empty_list, pickle_outfile)
    pickle_outfile.close()

    pickle_infile = open("productData.pkl", "rb")
    pickle_file = pickle.load(pickle_infile)
    print(pickle_file)

    return result

@bp.route('/product_list_info', methods=['POST'])
def product_list_info():
    Product.productList.clear()
    # The following code bellow is for data persistance
    pickle_infile = open("productData.pkl", "rb")
    pickle_file = pickle.load(pickle_infile)
    for data in pickle_file:
        Product.productList.append(data)

    # empty_list = []
    # overwrites pickle with productList
    pickle_outfile = open("productData.pkl", "wb")
    pickle.dump(Product.productList, pickle_outfile)
    # pickle.dump(empty_list, pickle_outfile)
    pickle_outfile.close()

@bp.route('/list/')
@protect
def list():
    # makes sure product list is populated correctly
    product_list_info()
    # create a list of all the products to send to the template
    list_of_product = []
    for x in Product.productList:
        list_of_product.append(x.getJson())
    return render_template('product_list.html', list_of_product= list_of_product)


@bp.route('/list/', methods=['GET', 'POST'])
def search_products():
    # get user input from product_list.html
    search_input = request.form['search_input']
    search_input = search_input.upper()
    # get all products (to be compared with search_input)
    product_list_info()
    all_products = []
    for x in Product.productList:
        all_products.append(x.getJson())

    return render_template('search_results.html', search_input=search_input, all_products=all_products)


@bp.route('/sort_price_descending')
@protect
def sort_price_descending():
    product_list_info()
    Product.productList.sort(key=lambda x: x.price, reverse=True)
    print(Product.productList)
    pickle_outfile = open("productData.pkl", "wb")
    pickle.dump(Product.productList, pickle_outfile)
    # pickle.dump(empty_list, pickle_outfile)
    pickle_outfile.close()
    #return render_template('product_list.html', list_of_product=Product.productList)
    list_of_product = []
    for x in Product.productList:
        list_of_product.append(x.getJson())
    return make_response({"output": list_of_product})


@bp.route('/sort_price_ascending')
@protect
def sort_price_ascending():
    product_list_info()
    Product.productList.sort(key=lambda x: x.price)
    print(Product.productList)
    pickle_outfile = open("productData.pkl", "wb")
    pickle.dump(Product.productList, pickle_outfile)
    # pickle.dump(empty_list, pickle_outfile)
    pickle_outfile.close()
    #return render_template('product_list.html', list_of_product=Product.productList)
    list_of_product = []
    for x in Product.productList:
        list_of_product.append(x.getJson())
    return make_response({"output": list_of_product})


@bp.route('/sort_title_asc')
@protect
def sort_title_ascending():
    product_list_info()
    Product.productList.sort(key=lambda x: x.title)
    print(Product.productList)
    pickle_outfile = open("productData.pkl", "wb")
    pickle.dump(Product.productList, pickle_outfile)
    # pickle.dump(empty_list, pickle_outfile)
    pickle_outfile.close()
    #return render_template('product_list.html', list_of_product=Product.productList)
    list_of_product = []
    for x in Product.productList:
        list_of_product.append(x.getJson())
    return make_response({"output": list_of_product})


@bp.route('/sort_title_desc')
@protect
def sort_title_descending():
    product_list_info()
    Product.productList.sort(key=lambda x: x.title, reverse=True)
    print(Product.productList)
    pickle_outfile = open("productData.pkl", "wb")
    pickle.dump(Product.productList, pickle_outfile)
    # pickle.dump(empty_list, pickle_outfile)
    pickle_outfile.close()
    #return render_template('product_list.html', list_of_product=Product.productList)
    list_of_product = []
    for x in Product.productList:
        list_of_product.append(x.getJson())
    return make_response({"output": list_of_product})

@bp.route('/buy_button_input', methods=['POST'])
def buy_button_input():
    product_list_info()
    product = request.json

    for x in Product.productList:
        if x.get_title() == product["title"] and x.get_description() == product["description"] and x.get_bought() == 0:
            x.buy_item()
            productSel = x
            break

        print(x.get_bought())

    for x in Product.productList:
        print(x.get_bought())

    print(Product.productList)
    pickle_outfile = open("productData.pkl", "wb")
    pickle.dump(Product.productList, pickle_outfile)
    # pickle.dump(empty_list, pickle_outfile)
    pickle_outfile.close()
    print("buy input ran")
    return productSel.getJson()

@bp.route('/buy_button_output', methods=['GET'])
@protect
def buy_button_output():
    list_of_product = []
    for x in Product.productList:
        list_of_product.append(x.getJson())
    return make_response({"output": list_of_product})

@bp.route('/<path:url>/')
@protect
def display(url):
    page = current_wiki.get_or_404(url)
    return render_template('page.html', page=page)


@bp.route('/create/', methods=['GET', 'POST'])
@protect
def create():
    form = URLForm()
    if form.validate_on_submit():
        return redirect(url_for(
            'wiki.edit', url=form.clean_url(form.url.data)))
    return render_template('create.html', form=form)


@bp.route('/edit/<path:url>/', methods=['GET', 'POST'])
@protect
def edit(url):
    page = current_wiki.get(url)
    form = EditorForm(obj=page)
    if form.validate_on_submit():
        if not page:
            page = current_wiki.get_bare(url)
        form.populate_obj(page)
        page.save()
        flash('"%s" was saved.' % page.title, 'success')
        return redirect(url_for('wiki.display', url=url))
    return render_template('editor.html', form=form, page=page)


@bp.route('/preview/', methods=['POST'])
@protect
def preview():
    data = {}
    processor = Processor(request.form['body'])
    data['html'], data['body'], data['meta'] = processor.process()
    return data['html']


@bp.route('/move/<path:url>/', methods=['GET', 'POST'])
@protect
def move(url):
    page = current_wiki.get_or_404(url)
    form = URLForm(obj=page)
    if form.validate_on_submit():
        newurl = form.url.data
        current_wiki.move(url, newurl)
        return redirect(url_for('wiki.display', url=newurl))
    return render_template('move.html', form=form, page=page)


@bp.route('/delete/<path:url>/')
@protect
def delete(url):
    page = current_wiki.get_or_404(url)
    current_wiki.delete(url)
    flash('Page "%s" was deleted.' % page.title, 'success')
    return redirect(url_for('wiki.home'))


@bp.route('/tags/')
@protect
def tags():
    tags = current_wiki.get_tags()
    return render_template('tags.html', tags=tags)


@bp.route('/tag/<string:name>/')
@protect
def tag(name):
    tagged = current_wiki.index_by_tag(name)
    return render_template('tag.html', pages=tagged, tag=name)


@bp.route('/search/', methods=['GET', 'POST'])
@protect
def search():
    form = SearchForm()
    if form.validate_on_submit():
        results = current_wiki.search(form.term.data, form.ignore_case.data)
        return render_template('search.html', form=form,
                               results=results, search=form.term.data)
    return render_template('search.html', form=form, search=None)


@bp.route('/user/login/', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = current_users.get_user(form.name.data)
        login_user(user)
        user.set('authenticated', True)
        flash('Login successful.', 'success')
        return redirect(request.args.get("next") or url_for('wiki.index'))
    return render_template('login.html', form=form)


@bp.route('/user/logout/')
@login_required
def user_logout():
    current_user.set('authenticated', False)
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('wiki.index'))


@bp.route('/user/')
def user_index():
    pass


@bp.route('/user/create/')
def user_create():
    pass


@bp.route('/user/<int:user_id>/')
def user_admin(user_id):
    pass


@bp.route('/user/delete/<int:user_id>/')
def user_delete(user_id):
    pass


"""
    Error Handlers
    ~~~~~~~~~~~~~~
"""


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

