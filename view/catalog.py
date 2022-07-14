from distutils.log import error
from flask import Flask,Blueprint, render_template, request, jsonify ,url_for, flash, redirect
import sqlite3 


catalog=Blueprint('catalog',__name__)

#FUNCATION
def connect_to_db():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn 

def insert_book(book):
    inserted_book = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO book(title, topic, quantity,price) VALUES (?, ?,?, ?)",
        (book['title'],book['topic'], book['quantity'], book['price']) )
        conn.commit()
        inserted_book = get_book_by_id(cur.lastrowid)
    except:
        conn().rollback()

    finally:
        conn.close()

    return inserted_book

def get_books():
    books = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM book")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            books = {}
            books["id"] = i["id"]
            books["title"] = i["title"]
            books["topic"] = i["topic"]
            books["quantity"] = i["quantity"]
            books["price"] = i["price"]
            books.append(books)

    except:
        books = ["error to get books"]

    return books


def get_book_by_id(id):
    book = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM book WHERE id = ?",(id,))
        row = cur.fetchone()

        # convert row object to dictionary
        book["title"] = row["title"]
        book["quantity"] = row["quantity"]
        book["price"] = row["price"]
    except:
        book = {"error to get book"}

    return book 


def update_book(book):
    updated_book = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE book SET quantity = ?, price =? WHERE id =?",  
                     (book["quantity"], book["price"], book["id"],))
        conn.commit()
        #return the user
        updated_book = get_book_by_id(book["id"])

    except:
        conn.rollback()
        updated_book = {}
    finally:
        conn.close()

    return updated_book

def delete_book(id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from book WHERE id = ?",(id,))
        conn.commit()
        message["status"] = "book deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete book"
    finally:
        conn.close()

    return message

@catalog.route('/')
def home_page():
    return "<h1>hello</h1>"

@catalog.route("/CATALOG_WEBSERVICE_IP/infoo", methods=['GET'])
def books_api():
    return jsonify(get_books()) 

@catalog.route('/CATALOG_WEBSERVICE_IP/info/<id>', methods=['GET'])
def get_api(id):
    return jsonify(get_book_by_id(id)) 

@catalog.route('/CATALOG_WEBSERVICE_IP/info', methods=['POST'])
def add_api():
    book = request.get_json()
    return jsonify(insert_book(book))          

@catalog.route('/CATALOG_WEBSERVICE_IP/info', methods=['PUT'])
def update_api():
    book = request.get_json()
    return jsonify(update_book(book))

@catalog.route('/CATALOG_WEBSERVICE_IP/info/<id>', methods=['DELETE'])
def delete_api(id):
    return jsonify(delete_book(id)) 
