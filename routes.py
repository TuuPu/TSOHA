from app import app
from flask import render_template, request, redirect
import users, restaurants
from geopy.geocoders import Nominatim

#TO DO
#Funtsi ulkonäkö sivuille kuntoon. Tää vasta vikaks, kunhan kaikki muu toimii hyvin.
#Admin/User checki
#Keskustelupalsta rafloille (osittain valmis) -> puuttu timestamp (ja järjestys timestampin mukaan), keskustelijan nimi
#Arvostelumahis
#Raflasivuille aukioloaikatiedot
#Tagihaku dropdown valikolla vaan (kesken)

@app.route("/")
def index():
    return render_template("index.html")

#Korjaa vielä redirect niin, että tarkistaa onko kyseessä admin vai käyttäjä
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
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
        if len(username)>15:
            return render_template("error.html", message="Username too long")
        password1 = request.form["password1"]
        if len(password1)>20:
            return render_template("error.html", message="Password too long")
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        admin = request.form["user"]
        if users.register(username, password1, admin):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

#Valmis
@app.route("/addrestaurant", methods=["GET", "POST"])
def addrestaurant():
    geolocator = Nominatim(user_agent="app.py")
    if request.method == "GET":
        return render_template("addrestaurant.html")
    if request.method == "POST":
        name = request.form["name"]
        type = request.form["description"]
        address = request.form["address"]
        location_variable = geolocator.geocode(address)
        values = location_variable.latitude, location_variable.longitude
        delimiter = ', '
        location = delimiter.join([str(value) for value in values])
        print(location)
        if len(name)>20:
            return render_template("error.html", message="Restaurant name too long")
        if len(type)>200:
            return render_template("error.html", message="Description too long")
        if len(address)>50:
            return render_template("error.html", message="Address too long")
        else:
            if restaurants.addrestaurant(name, location, type):
                return redirect("/")
            else:
                return render_template("error.html", message="Adding a restaurant failed")

#Tagit vielä etusivulle
@app.route("/restaurantlist", methods=["GET", "POST"])
def restaurantlist():
    if request.method == "GET":
        print(restaurants.address(1))
        restaurantlists = restaurants.restaurantlist()
        return render_template("restaurantlist.html", restaurantlists=restaurantlists)
    if request.method == "POST":
        type = request.form["query"]
        if len(type)>20:
            return render_template("error.html", message="Query too long")
        restaurantlists = restaurants.search_by_type(type)
        return render_template("restaurantlist.html", restaurantlists=restaurantlists)

#Perustoiminnoiltaan valmis, pitää lisätä vielä lisää informaatiota ravintoloille kuvauksen lisäksi
@app.route("/restaurant/<int:id>", methods=["GET", "POST"])
def restaurant(id):
    geolocator = Nominatim(user_agent="app.py")
    if request.method == "GET":
        messages = restaurants.get_messages(id)
        description = restaurants.description(id)
        address_loc = geolocator.reverse(restaurants.address(id))
        location = geolocator.geocode(address_loc, addressdetails=True)
        loc_raw = location.raw['address']
        address = loc_raw['road'] + ' ' + loc_raw['house_number']
        return render_template("restaurant.html", id=id, description=description, address=address, messages=messages)
    if request.method == "POST":
        description = restaurants.description(id)
        address_loc = geolocator.reverse(restaurants.address(id))
        location = geolocator.geocode(address_loc, addressdetails=True)
        loc_raw = location.raw['address']
        address = loc_raw['road'] + ' ' + loc_raw['house_number']
        save_message = request.form["message"]
        savemessages = restaurants.save_message(id, save_message)
        messages=restaurants.get_messages(id)
        if len(save_message)>5000:
            return render_template("error.html", message="Message too long")
        else:
            return render_template("restaurant.html", id=id, description=description, address=address, savemessages=savemessages, messages=messages)

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

#Valmis tagin pituutta lukuunottamatta
@app.route("/tags", methods=["GET", "POST"])
def tags():
    if request.method == "GET":
        restaurantlists = restaurants.restaurantlist()
        existing_tags = restaurants.select_tags()
        return render_template("tags.html", restaurantlists=restaurantlists, existing_tags=existing_tags)
    if request.method == "POST":
        names = request.form.getlist("selected_restaurants")
        tag = request.form["tag"]
        #tarkista pituus tagille
        for name in names:
            if(tag == ''):
                tag = request.form["existing_tag"]
                print(tag)
                restaurants.add_tag(name, tag)
            else:
                print("EI TÄNNE")
                restaurants.add_tag(name, tag)
        return redirect("/")


#valmis
@app.route("/map")
def map():
    info = restaurants.all_info()
    return render_template("map.html", info=info)