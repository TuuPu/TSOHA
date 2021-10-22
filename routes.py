from app import app
from flask import render_template, request, redirect, session
import users, restaurants
from geopy.geocoders import Nominatim
from secrets import token_hex
from time import sleep

#TO DO
#Funtsi ulkonäkö sivuille kuntoon. Tää vasta vikaks, kunhan kaikki muu toimii hyvin.
#Etusivulle käyttäjän nimi, jolla logattu sisään.

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        name = users.get_username(int(session.get("user_id")))
        existing_tags = restaurants.select_tags()
        return render_template("index.html", existing_tags=existing_tags, name=name)

#Valmis
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        session["csrf_token"] = token_hex(16)
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

#Valmis
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

#Valmis
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        if len(username)>15 or len(username)<5:
            return render_template("error.html", message="Username too long or short")
        password1 = request.form["password1"]
        if len(password1)>20 or len(password1)<8:
            return render_template("error.html", message="Password too long or short")
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Passwords differ")
        admin = request.form["user"]
        if users.register(username, password1, admin):
            return redirect("/")
        else:
            return render_template("error.html", message="Couldn't register a new account, you could try a different username")

#Valmis (voi vielä kattoa onko aukeeminen > sulkeminen)
@app.route("/addrestaurant", methods=["GET", "POST"])
def addrestaurant():
    geolocator = Nominatim(user_agent="app.py")
    weekdaylists = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if request.method == "GET":
        return render_template("addrestaurant.html", weekdaylists=weekdaylists)
    if request.method == "POST":
        name = request.form["name"]
        type = request.form["description"]
        address = request.form["address"]
        location_variable = geolocator.geocode(address)
        values = location_variable.latitude, location_variable.longitude
        delimiter = ', '
        location = delimiter.join([str(value) for value in values])
        if len(name)>20 or len(name)<5:
            return render_template("error.html", message="Restaurant name too long or short")
        if len(type)>200:
            return render_template("error.html", message="Description too long")
        if len(address)>50 or len(address)<10:
            return render_template("error.html", message="Address too long or short")
        else:
            if restaurants.addrestaurant(name, location, type):
                id = restaurants.restaurant_id(name)
                for wday in weekdaylists:
                    if request.form["closed_" + wday] == "open":
                        open = request.form["opening_" + wday]
                        close = request.form["closing_" + wday]
                        restaurants.save_opening(wday, open, close, "open", id)
                    else:
                        restaurants.save_opening(wday, "-", "-", "closed", id)
                return redirect("/")
            else:
                return render_template("error.html", message="Adding a restaurant failed")

#Valmis
@app.route("/restaurantlist", methods=["GET", "POST"])
def restaurantlist():
    if request.method == "GET":
        restaurantlists = restaurants.restaurantlist()
        return render_template("restaurantlist.html", restaurantlists=restaurantlists)
    if request.method == "POST":
        type = request.form["query"]
        if type == '':
            tag = request.form["existing_tag"]
            restaurantlists = restaurants.search_by_tag(tag)
            return render_template("restaurantlist.html", restaurantlists=restaurantlists)
        else:
            if len(type)>20:
                return render_template("error.html", message="Query too long")
            restaurantlists = restaurants.search_by_type(type)
            return render_template("restaurantlist.html", restaurantlists=restaurantlists)

#Valmis
@app.route("/restaurant/<int:id>", methods=["GET", "POST"])
def restaurant(id):
    geolocator = Nominatim(user_agent="app.py")
    gradelists = [1, 2, 3, 4, 5]
    restaurant = restaurants.get_name(id)
    messages = restaurants.get_messages(id)
    description = restaurants.description(id)
    opening = restaurants.get_openings(id)
    address_loc = geolocator.reverse(restaurants.address(id))
    location = geolocator.geocode(address_loc, addressdetails=True)
    loc_raw = location.raw['address']
    address = loc_raw['road'] + ' ' + loc_raw['house_number']
    if request.method == "GET":
        #gradelists = [1, 2, 3, 4, 5]
        #restaurant = restaurants.get_name(id)
        #messages = restaurants.get_messages(id)
        #description = restaurants.description(id)
        #address_loc = geolocator.reverse(restaurants.address(id))
        #location = geolocator.geocode(address_loc, addressdetails=True) #TÄSSÄ OLI SLEEPIT JOS EI TOIMI HEROKUSSA
        #opening = restaurants.get_openings(id)
        #loc_raw = location.raw['address']
        #address = loc_raw['road'] + ' ' + loc_raw['house_number']
        return render_template("restaurant.html", id=id, description=description, address=address, messages=messages, gradelists=gradelists, opening=opening, restaurant=restaurant)
    if request.method == "POST":
        if not session.get("csrf_token") and not session.get("user_id"):
            return render_template("login.html")
        if session["csrf_token"] != request.form["csrf_token"]:
            return render_template("error.html", message="csrf token invalid")
        #restaurant = restaurants.get_name(id)
        #gradelists = [1, 2, 3, 4, 5]
        #description = restaurants.description(id)
        #opening = restaurants.get_openings(id)
        #address_loc = geolocator.reverse(restaurants.address(id))
        #sleep(1)
        #location = geolocator.geocode(address_loc, addressdetails=True)
        #sleep(1)
        #loc_raw = location.raw['address']
        #address = loc_raw['road'] + ' ' + loc_raw['house_number']
        save_message = request.form["message"]
        grade = request.form["gradelist"]
        savemessages = restaurants.save_message(id, save_message, grade, session.get("user_id", 0))
        #messages=restaurants.get_messages(id)
        if len(save_message)>5000:
            return render_template("error.html", message="Message too long")
        else:
            return render_template("restaurant.html", id=id, description=description, address=address, savemessages=savemessages, messages=messages, gradelists=gradelists, opening=opening, restaurant=restaurant)

#Valmis
@app.route("/deleterestaurant", methods=["GET", "POST"])
def deleterestaurant():
    if request.method == "GET":
        return render_template("deleterestaurant.html")
    if request.method == "POST":
        name = request.form["name"]
        if restaurants.deleterestaurant(name):
            return redirect("/")
        else:
            return render_template("error.html", message="Could not delete restaurant")

#Valmis
@app.route("/tags", methods=["GET", "POST"])
def tags():
    if request.method == "GET":
        restaurantlists = restaurants.restaurantlist()
        existing_tags = restaurants.select_tags()
        return render_template("tags.html", restaurantlists=restaurantlists, existing_tags=existing_tags)
    if request.method == "POST":
        names = request.form.getlist("selected_restaurants")
        tag = request.form["tag"]
        for name in names:
            if(tag == ''):
                tag = request.form["existing_tag"]
                restaurants.add_tag(name, tag)
            else:
                if len(tag)>15 or len(tag)<3:
                    return render_template("error.html", message="The tag you tried to give is too long or too short")
                else:
                    restaurants.add_tag(name, tag)
                    return redirect("/")


#valmis
@app.route("/map")
def map():
    info = restaurants.all_info()
    return render_template("map.html", info=info)