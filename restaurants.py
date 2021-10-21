from db import db
from flask import session
from geopy.geocoders import Nominatim

def addrestaurant(name, address, type):
    try:
        sql = "INSERT INTO restaurants (name, address, visible) VALUES (:name, :address, TRUE) RETURNING id"
        result = db.session.execute(sql, {"name":name, "address":address})
        restaurant_id = result.fetchone()[0]
        sql = "INSERT INTO restaurant_info (restaurant_id, type) VALUES (:restaurant_id, :type)"
        db.session.execute(sql, {"restaurant_id":restaurant_id, "type":type})
        db.session.commit()
        return True
    except Exception as error:
        print(error)
        return False

def search_by_type(type):
    try:
        sql = "SELECT r.id, r.name FROM restaurants as r, restaurant_info as i WHERE r.id=i.restaurant_id AND i.type ILIKE :type"
        result = db.session.execute(sql, {"type":"%"+type+"%"})
        restaurantlists = result.fetchall()
        return restaurantlists
    except Exception as error:
        print(error)
        return False

def search_by_tag(tag):
    try:
        sql = "SELECT r.id, r.name FROM restaurants as r, restaurant_tags as t WHERE r.id=t.restaurant_id AND t.tag=:tag"
        result = db.session.execute(sql, {"tag":tag})
        restaurantlists = result.fetchall()
        return restaurantlists
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

def address(id):
    try:
        sql = ("SELECT address FROM restaurants WHERE id=:id")
        result = db.session.execute(sql, {"id":id})
        address = result.fetchone()[0]
        return address
    except Exception as error:
        print(error)
        return False

def deleterestaurant(name):
    try:
        sql = ("UPDATE restaurants SET visible=FALSE WHERE name=:name")
        db.session.execute(sql, {"name":name})
        db.session.commit()
        return True
    except Exception as error:
        print(error)
        return False

def get_openings(restaurant_id):
    try:
        sql = "SELECT day, opening_time, closing_time, open FROM opening_times WHERE restaurant_id=:restaurant_id"
        result = db.session.execute(sql, {"restaurant_id":restaurant_id})
        openinglist = result.fetchall()
        return openinglist
    except Exception as error:
        print(error)
        return False


def restaurantlist():
    try:
        result = db.session.execute("SELECT id, name FROM restaurants WHERE visible=TRUE")
        restaurantlist = result.fetchall()
        return restaurantlist
    except Exception as error:
        print(error)
        return False

def restaurant_id(name):
    try:
        sql = ("SELECT id FROM restaurants WHERE name=:name")
        result = db.session.execute(sql, {"name":name})
        id_list = result.fetchone()[0]
        return id_list
    except Exception as error:
        print(error)
        return False

def get_name(id):
    try:
        sql = "SELECT name FROM restaurants WHERE id=:id"
        result = db.session.execute(sql, {"id":id})
        name = result.fetchone()[0]
        return name
    except Exception as error:
        print(error)
        return False

def add_tag(id, tag):
    try:
        sql = ("INSERT INTO restaurant_tags (tag, restaurant_id) VALUES (:tag, :id)")
        db.session.execute(sql, {"tag":tag, "id":id})
        db.session.commit()
        return True
    except Exception as error:
        print(error)
        return False

def all_info():
    try:
        result = db.session.execute("SELECT r.id, r.name, r.address, i.type FROM restaurants as r, restaurant_info as i WHERE r.id=i.restaurant_id")
        infolists = result.fetchall()
        datalists=[]
        for infolist in infolists:
            info_tmp = list(infolist)
            coord = info_tmp.pop(2)
            coord_list = coord.split(",")
            info_tmp.insert(2, coord_list[0])
            info_tmp.insert(3, coord_list[1])
            datalists.append(info_tmp)
        return datalists
    except Exception as error:
        print(error)
        return False

def save_message(restaurant_id, content, grade, user_id):
    try:
        sql = ("INSERT INTO messages (content, restaurant_id, grade, user_id, sent_at) VALUES (:content, :restaurant_id, :grade, :user_id, NOW())")
        db.session.execute(sql, {"content":content, "restaurant_id":restaurant_id, "grade":grade, "user_id":user_id})
        db.session.commit()
        return True
    except Exception as error:
        print(error)
        return False

def save_opening(day, opening_time, closing_time, open, restaurant_id):
    try:
        sql = ("INSERT INTO opening_times (day, opening_time, closing_time, open, restaurant_id) VALUES (:day, :opening_time, "
               ":closing_time, :open, :restaurant_id)")
        db.session.execute(sql, {"day":day, "opening_time":opening_time, "closing_time":closing_time, "open":open, "restaurant_id":restaurant_id})
        db.session.commit()
        return True
    except Exception as error:
        print(error)
        return False


def get_messages(id):
    try: #Tässä ehkä distinct
        sql = ("SELECT DISTINCT m.content, m.grade, u.username, m.sent_at FROM messages as m, users as u WHERE u.id=m.user_id AND restaurant_id=:id ORDER BY sent_at")
        result = db.session.execute(sql, {"id":id})
        messages = result.fetchall()
        list = []
        for message in messages:
            list.append(message)
        return list
    except Exception as error:
        print(error)
        return False

def select_tags():
    try:
        result = db.session.execute("SELECT DISTINCT tag FROM restaurant_tags WHERE tag NOTNULL")
        tag_list = result.fetchall()
        return tag_list
    except Exception as error:
        print(error)
        return False
