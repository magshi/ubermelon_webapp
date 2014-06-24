from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2


app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site""" 
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html", melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    print melon
    return render_template("melon_details.html", display_melon = melon)

@app.route("/cart")
def shopping_cart():
    if session.get('cart'):
        cart_list = session['cart']
        melindex = {}
        for item in cart_list:
            if melindex.get(item):
                melindex[item] += 1
            else:
                melindex[item] = 1
        print cart_list
        print melindex
    else:
        pass

    cart_contents = {}    
    for melon_id in melindex:
        cart_contents[melon_id] = [model.get_melon_by_id(melon_id).common_name, model.get_melon_by_id(melon_id).price]
    print cart_contents

    """TODO: Display the contents of the shopping cart. The shopping cart is a
    list held in the session that contains all the melons to be added. Check
    accompanying screenshots for details."""
    return render_template("cart.html", cart = cart_contents)
    
@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    if session.get('cart'):
        session['cart'].append(id)
    else:
        session['cart'] = [id]

    flash("Successfully added [THE MELON YOU CHOSE] to cart!")
    return redirect("/cart")

    """TODO: Finish shopping ca
    rt functionality using session variables to hold
    cart list.
    Intended behavior: when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """

@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""
    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

if __name__ == "__main__":
    app.run(debug=True)
