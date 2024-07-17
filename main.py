from flask import Flask, request, render_template, jsonify

import db
from mapwithlist import generate_mapwithlist
from fastapi import FastAPI

import json
import pymongo
from fastapi.middleware.cors import CORSMiddleware

from mapwithlist2 import generate_mapwithlist2

app=FastAPI()

app = Flask(__name__)

# first page   login
@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template("signin.html")
#second page signup
@app.route('/templates/signup', methods = ['GET', 'POST'])
def signup():
    return render_template("signup.html")

@app.route('/signin', methods = ['GET', 'POST'])
def signin():
    status, username = db.check_user()

    data = {
        "username": username,
        "status": status
    }

    return json.dumps(data)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    status = db.insert_data()
    return json.dumps(status)

# main home page
@app.route("/templates/index1.html")
def index1():
    return render_template("index1.html")


@app.route('/map')
def generate():
    generate_mapwithlist()
    return ""

@app.route("/templates/info.html")
def info():
    return render_template("info.html")

@app.route("/templates/hos1map.html")
def hos1map():
    return render_template("hos1map.html")



@app.route('/map2')
def generate2():
    generate_mapwithlist2()
    return ""
@app.route("/templates/info2.html")
def info2():
    return render_template("info2.html")

@app.route("/templates/hos2map.html")
def hos2map():
    return render_template("hos2map.html")


@app.route('/get_data', methods=['GET'])
def get_data():
    # Retrieve the 'name' parameter from the query string
    name = request.args.get('name')

    # Perform any necessary processing to fetch data based on the provided name
    # Replace this with your actual data retrieval logic
    data = {
        'name': name,
        'other_property': 'other_value'
    }

    # Return the data as JSON
    return jsonify(data)



@app.route("/templates/payment.html")
def payment():
    return render_template("payment.html")

@app.route("/templates/confirmation.html")
def confirmation():
    return render_template("confirmation.html")
@app.route("/templates/payment_con.html")
def payment_confirmation():
    return render_template("payment_con.html")





#if __name__=='__main__':
    #app.debug=True
    #app.run()
