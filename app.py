import os

from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_sqlalchemy import SQLAlchemy

import requests
import json

from sqlalchemy.exc import IntegrityError
from forms import UserAddForm, UserEditForm, LoginForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgres:///charge'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'DONOTTELL'

db = SQLAlchemy(app)

from models import db, connect_db, User, Station

connect_db(app)

#db.drop_all()
db.create_all()
db.session.commit()

CURR_USER_KEY = "curr_user"

@app.before_request
def add_user_to_g():
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    session[CURR_USER_KEY] = user.id

def do_logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")


@app.route("/")
def home():
    return render_template("base.html", searchbar=True, homemessage=True, homedesign=True)
    

@app.route("/stations")
def list_stations():
    city = request.args.get('q') 
    MAPQUEST_API_KEY = "TEAEavBJK5sRmqikzjPOQHPLLxGQG02d"

    geo = requests.get(f"http://www.mapquestapi.com/geocoding/v1/address?key={MAPQUEST_API_KEY}&location={city}")
    geo_resp = geo.json()

    lat = geo_resp["results"][0]["locations"][0]["latLng"]["lat"]
    lng = geo_resp["results"][0]["locations"][0]["latLng"]["lng"]

    OPEN_CHARGE_API_KEY = "6e256d5b-964d-4406-b532-068a5c28f68b"

    stations = requests.get("https://api.openchargemap.io/v3/poi/", 
                            params={'key': OPEN_CHARGE_API_KEY, 'maxresults': 10, 'latitude': lat, 'longitude': lng, 'distance': 250})

    stations_resp = stations.json()

    titles = []
    address = []
    city = []
    state = []
    usage = []
    ids = []
    
    i = 0
    while i < 10:
        titles.append(stations_resp[i]["AddressInfo"]["Title"])
        ids.append(stations_resp[i]["ID"])
        try:
            usage.append(stations_resp[i]["UsageType"]["Title"])
        except:
            usage.append("Not Available")
        address.append(stations_resp[i]["AddressInfo"]["AddressLine1"])
        city.append(stations_resp[i]["AddressInfo"]["Town"])
        state.append(stations_resp[i]["AddressInfo"]["StateOrProvince"])

        i += 1    

    return render_template('chargers/stations.html', titles=titles, ids=ids, address=address, city=city, state=state, usage=usage, searchbar=True)


@app.route('/stations/<int:charger_id>')
def detail_station(charger_id):
    OPEN_CHARGE_API_KEY = "6e256d5b-964d-4406-b532-068a5c28f68b"

    station_resp = requests.get("https://api.openchargemap.io/v3/poi/", 
                            params={'key': OPEN_CHARGE_API_KEY, 'maxresults': 1, 'chargepointid': charger_id})
    
    station_info = station_resp.json()

    try:
        station_operate = station_info[0]["StatusType"]["Title"]
    except:
        station_operate = "Not Available"
    try:
        station_type = station_info[0]["UsageType"]["Title"]
    except:
        station_type = "Not Available"
    try:
        station_title = station_info[0]["AddressInfo"]["Title"] 
    except:
        station_title = "Not Available"
    try:
        station_address = station_info[0]["AddressInfo"]["AddressLine1"]
    except:
        station_address = "Not Available"
    try:
        station_city = station_info[0]["AddressInfo"]["Town"]
    except:
        station_city = "Not Available"
    try:
        station_state = station_info[0]["AddressInfo"]["StateOrProvince"]
    except:
        station_state = "Not Available"
    try:
        station_country = station_info[0]["AddressInfo"]["Country"]["Title"]
    except:
        station_country = "Not Available"
    try:        
        station_lat = station_info[0]["AddressInfo"]["Latitude"]
    except:
        station_lat = "Not Available"
    try:
        station_long = station_info[0]["AddressInfo"]["Longitude"]
    except:
        station_long = "Not Available"
    try:
        station_phone = station_info[0]["AddressInfo"]["ContactTelephone1"]
    except:
        station_phone = "Not Available"
    try:
        station_connection_title = station_info[0]["Connections"][0]["ConnectionType"]["Title"]
    except:
        station_connection_title = "Not Available"
    try:
        station_connection_level = station_info[0]["Connections"][0]["Level"]["Title"]
    except:
        station_connection_level = "Not Available"
    try:
        station_current_type = station_info[0]["Connections"][0]["CurrentType"]["Title"]
    except:
        station_current_type = "Not Available"
    try:
        station_num = station_info[0]["Connections"][0]["Quantity"]
    except:
        station_num = "Not Available"

    favorites = Station.query.filter(Station.user_id == g.user.id).all()
    favorite_ids = [int(favorite.name) for favorite in favorites]

    if charger_id in favorite_ids:
        star = True
        
    else:
        star = False


    return render_template('chargers/station_info.html', charger_id=charger_id, station_operate=station_operate, station_type=station_type, station_title=station_title,
        station_address=station_address, station_city=station_city, station_state=station_state, station_country=station_country,
        station_lat=station_lat, station_long=station_long, station_phone=station_phone, station_connection_title=station_connection_title,
        station_connection_level=station_connection_level, station_current_type=station_current_type, station_num=station_num, star=star)


@app.route('/stations/<int:charger_id>/like', methods=['POST'])
def add_like(charger_id):
    favorites = Station.query.filter(Station.user_id == g.user.id).all()
    favorite_ids = [int(favorite.name) for favorite in favorites]

    if charger_id in favorite_ids:
        dele = Station.query.filter(Station.user_id == g.user.id, Station.name == str(charger_id)).delete()
        db.session.commit()
        
    else:
        charger = Station.charger(
        name=charger_id,
        user_id=g.user.id
        )
   
        db.session.commit()
    
    return redirect("/")


@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    favorites = Station.query.filter(Station.user_id == user_id).all()
    favorite_ids = [favorite.name for favorite in favorites]

    OPEN_CHARGE_API_KEY = "6e256d5b-964d-4406-b532-068a5c28f68b"

    station_resp = requests.get("https://api.openchargemap.io/v3/poi/", 
                            params={'key': OPEN_CHARGE_API_KEY, 'chargepointid': favorite_ids})
    
    station_info = station_resp.json()
    
    titles = []
    address = []
    city = []
    state = []
    usage = []
    ids = []
    
    i = 0
    while i < len(favorite_ids):
        titles.append(station_info[i]["AddressInfo"]["Title"])
        ids.append(station_info[i]["ID"])
        try:
            usage.append(station_info[i]["UsageType"]["Title"])
        except:
            usage.append("Not Available")
        address.append(station_info[i]["AddressInfo"]["AddressLine1"])
        city.append(station_info[i]["AddressInfo"]["Town"])
        state.append(station_info[i]["AddressInfo"]["StateOrProvince"])

        i += 1
  
    return render_template('users/home.html', user=user, titles=titles, ids=ids, address=address, city=city, state=state, usage=usage)


@app.route('/users/profile', methods=["GET", "POST"])
def edit_profile():
    if not g.user:
        flash("Access Unauthorized.", "danger")
        return redirect("/")

    user = g.user
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.image_url = form.image_url.data or "/static/images/default-pic.png"

            db.session.commit()
            return redirect(f"/users/{user.id}")

        flash("Wrong password, please try again.", 'danger')

    return render_template('users/edit_user.html', form=form, user_id=user.id)

@app.errorhandler(404)
def page_not_found(e):
    """404 page."""

    return render_template('404.html'), 404