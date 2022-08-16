from ctypes.wintypes import DWORD
from datetime import datetime
from this import d
from flask import Flask, flash, render_template, request
from flask_pymongo import PyMongo
from gridfs import Database
from pymongo import MongoClient

app = Flask(__name__)

# client = MongoClient(host='mongo-mongodb-headless', port=27017, database='customer', username='admin', password='admin', authSource='admin')
client = MongoClient("mongodb://admin:admin@mongo-mongodb-headless:27017/customer")


@app.route("/")
def form():
   return render_template('form.html')


@app.route("/read")
def read_data():
    db = client.customer
    feedback_coll = db.customer
    customer = (feedback_coll.find({}))
    return render_template('index.html', customer=customer)


@app.route("/data", methods=['GET'])
def show_data():
    if request.method == 'GET':
        name = request.args.get("x")
        phone = request.args.get("y")
        feed = request.args.get("z")
    if name != "" and phone != "" and feed != "":
        var = {"name": name, "phone": phone, "feedback": feed}
        db = client.customer
        feedback_coll = db.customer
        feedback_coll.insert_one(var)
        return render_template('retind.html')
    else:
        return ("Kindly fill the form")


@app.route("/delete")
def delete():
    return render_template('delone.html')


@app.route("/delete_one")
def del_one():
    destroy = request.args.get("x")
    db = client.customer
    feedback_coll = db.customer
    try:
        feedback_coll.delete_one({"name":destroy})
    except TypeError:
        return ("No such name!")
    return ("Deleted")


@app.route("/delete_all")
def delete_all():
    db = client.customer
    feedback_coll = db.customer
    feedback_coll.delete_many({})
    return "All data deleted"


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8000)