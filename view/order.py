from flask import Flask,Blueprint, render_template, request, jsonify ,url_for, flash, redirect
import sqlite3

order=Blueprint('order',__name__)

@order.route('/')
def home_page():
    return "<h1>hello</h1>"

def connect_to_db():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn 

def get_topic(topic):
    books = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM book WHERE topic=?",topic)
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            books = {}
            books["id"] = i["id"]
            books["title"] = i["title"]
            books.append(books)

    except:
        books = ["error to get books"]

    return books    

@order.route("/CATALOG_WEBSERVICE_IP/search/<topic>", methods=['GET'])
def topic_api(topic):
    return jsonify(get_topic(topic)) 