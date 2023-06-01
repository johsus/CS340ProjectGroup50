from flask import Flask, render_template, json, request, redirect
from flask_mysqldb import MySQL
import os
# import database.db_connector as db

# Configuration

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_wubr'
app.config['MYSQL_PASSWORD'] = '9544' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_wubr'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

# db_connection = db.connect_to_database()

mysql = MySQL(app)

# Routes 

@app.route('/')
def root():
    return redirect("/customers")

@app.route('/customers', methods = ["POST", "GET"])
def customers():
    if request.method == "GET":

        query = "SELECT customer_id AS customerID, customer_name AS customerName, phone_number AS phoneNumber FROM Customers;"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

    if request.method == "POST":
        if request.form.get("Add_Customer"):
            customer_name = request.form["customer_name"]
            phone_number = request.form["phone_number"]

            query = "INSERT INTO Customers (customer_name, phone_number) VALUES (%s, %s);"
            cursor = mysql.connection.cursor()
            cursor.execute(query, (customer_name, phone_number))
            mysql.connection.commit()

            return redirect("/customers")

    return render_template("customers.j2", Customers = results)

@app.route('/delete-customers/<int:id>')
def delete_customers(id):
    query = "DELETE FROM Customers WHERE customer_id = %s;"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/customers")

@app.route('/edit-customers/<int:id>', methods=["POST", "GET"])
def edit_customers(id):
    if request.method == "GET":
        query1 = "SELECT * FROM Customers WHERE customer_id = %s;" % (id)
        cursor = mysql.connection.cursor()
        cursor.execute(query1)
        data = cursor.fetchall()

        return render_template("edit_customers.j2", data = data)

    if request.method == "POST":
        if request.form.get("edit_customer"):
            customer_name = request.form["customer_name"]
            phone_number = request.form["phone_number"]

            query = "INSERT INTO Customers (customer_name, phone_number) VALUES (%s, %s);"
            cursor = mysql.connection.cursor()
            cursor.execute(query, (customer_name, phone_number))
            mysql.connection.commit()

    return redirect("/customers")

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9544)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True)