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
    # if there's nothing in the cart, redirect to melons page
    if 'cart' not in session:
        return redirect("/melons")

    # initialize empty dictionary for the melon count
    melon_count = {}

    # this block iterates through a list of melon IDs and generates a dictionary with key: melon id, value: # of occurrences
    for melon_id in session['cart']:
        if melon_count.get(melon_id):
            melon_count[melon_id] += 1
        else:
            melon_count[melon_id] = 1

    print melon_count
    melon_dict = {}
    cart_total = 0

    #for each melon id, and the quantity for that melon type, in the melon_count dict, get the melon object associated with that melon id from the db using the model. Also calculates the total cost for the cart.
    for melon_id, qty in melon_count.iteritems():
        melon = model.get_melon_by_id(melon_id)
        melon_dict[melon] = qty
        cart_total += (qty * melon.price)

    print melon_dict

    #convert the cart total price to a two-digit float string
    cart_total_float = "%0.2f" % cart_total

    #re-cast variables as variables we can pass into cart.html to use with jinja
    return render_template("cart.html", cart = melon_dict, total = cart_total_float)
    
@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    # if the cart already has stuff in it, add to it. if not, create a new list named 'cart' in the session dictionary
    if session.get('cart'):
        session['cart'].append(id)
    else:
        session['cart'] = [id]

    flash("Great choice! That's the best melon!")
    return redirect("/melons")

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

    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

if __name__ == "__main__":
    app.run(debug=True)
