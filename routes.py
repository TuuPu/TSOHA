from app import app
from flask import render_template, request, redirect
import users, restaurants

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
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        admin = request.form["user"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1, admin):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

#Valmis
@app.route("/addrestaurant", methods=["GET", "POST"])
def addrestaurant():
    if request.method == "GET":
        return render_template("addrestaurant.html")
    if request.method == "POST":
        name = request.form["name"]
        type = request.form["description"]
        address = request.form["address"]
        if restaurants.addrestaurant(name, address, type):
            return redirect("/")
        else:
            return render_template("error.html", message="Adding a restaurant failed")

#Valmis
@app.route("/restaurantlist")
def restaurantlist():
    restaurantlists = restaurants.restaurantlist()
    return render_template("restaurantlist.html", restaurantlists=restaurantlists)

#Perustoiminnoiltaan valmis, pitää lisätä vielä lisää informaatiota ravintoloille kuvauksen lisäksi
@app.route("/restaurant/<int:id>")
def restaurant(id):
    description = restaurants.description(id)
    return render_template("restaurant.html", id=id, description=description)

#Ei toimintoja vielä, korjaa
@app.route("/deleterestaurant")
def deleterestaurant():
    return render_template("error.html", message="This functionality is not in use yet")

#Ei toimintoja vielä, korjaa
@app.route("/tags")
def tags():
    return render_template("error.html", message="This functionality is not in use yet")

#Ei toimintoja vielä, korjaa
@app.route("/map")
def map():
    return render_template("error.html", message="This functionality is not in use yet")

#Ei toimintoja vielä, korjaa
@app.route("/search")
def search():
    return render_template("error.html", message="This functionality is not in use yet")