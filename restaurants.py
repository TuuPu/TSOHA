from db import db
from flask import session

def addrestaurant(name, address, type):
    try:
        sql = "INSERT INTO restaurants (name, address) VALUES (:name, :address) RETURNING id"
        result = db.session.execute(sql, {"name":name, "address":address})
        restaurant_id = result.fetchone()[0]
        sql = "INSERT INTO restaurant_info (restaurant_id, type) VALUES (:restaurant_id, :type)"
        db.session.execute(sql, {"restaurant_id":restaurant_id, "type":type})
        db.session.commit()
        return True
    except Exception as error:
        print(error)
        return False


def description(id):
    try:
        sql = ("SELECT type FROM restaurant_info WHERE restaurant_id=:id")
        result = db.session.execute(sql, {"id":id})
        description = result.fetchone()
        return description
    except Exception as error:
        print(error)
        return False


def restaurantlist():
    try:
        result = db.session.execute("SELECT id, name FROM restaurants")
        restaurantlist = result.fetchall()
        return restaurantlist
    except Exception as error:
        print(error)
        return False