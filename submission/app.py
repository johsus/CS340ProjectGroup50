from flask import Flask, render_template, url_for, json, request, redirect
from flask_mysqldb import MySQL
import os
# import database.db_connector as db

# Configuration

app = Flask(__name__)

# database connection
app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_wubr'
app.config['MYSQL_PASSWORD'] = '9544' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_wubr'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

# db_connection = db.connect_to_database()

mysql = MySQL(app)

# Routes 

def connect(command, values=None):
    mycursor = mysql.connection.cursor()
    if values:
        mycursor.execute(command, values)
        mysql.connection.commit()
    else:
        mycursor.execute(command)

    if 'SELECT' in command:
        return mycursor.fetchall



# index
@app.route("/")
def index():
    return render_template("index.html")

# orders
@app.route('/orders', methods = ["POST", "GET"])
def orders():
    # READ
    if request.method == "GET":

        query = "SELECT order_id AS 'ID', time, customer_id AS 'customerID', dish_quantity AS 'dishQuantity' FROM Orders;"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        # render edit_customer page passing query data to the edit_customers template
        return render_template("orders.j2", data = data)

    # ADD NEW
    if request.method == "POST":
        if request.form.get("add_order"):
            time = request.form["time"]
            customer_id = request.form["customer_id"]
            dish_quantity = request.form["dish_quantity"]

            query = "INSERT INTO Orders (time, customer_id, dish_quantity) VALUES (%s, %s, %s);"
            cursor = mysql.connection.cursor()
            cursor.execute(query, (time, customer_id, dish_quantity))
            mysql.connection.commit()

            return redirect("/orders")

@app.route('/delete_orders/<int:id>')
def delete_orders(id):
    query = "DELETE FROM Orders WHERE order_id = %s;"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/orders")

@app.route('/edit_orders/<int:id>', methods = ['GET', 'POST'])
def edit_orders(id):

    if request.method == "POST":
        time = request.form["time"]
        customer_id = request.form["customer_id"]
        dish_quantity = request.form["dish_quantity"]

        query = "UPDATE Orders SET time = %s, customer_id = %s , dish_quantity = %s WHERE order_id = %s;"
        values = (time, customer_id, dish_quantity, id)
        cursor = mysql.connection.cursor()
        cursor.execute(query, values)
        mysql.connection.commit()

        return redirect("/orders")

    if request.method == "GET":
        query1 = "SELECT order_id AS 'ID', time, customer_id AS 'customerID', dish_quantity AS 'dishQuantity' FROM Orders WHERE order_id = %s;" % (id)
        cursor = mysql.connection.cursor()
        cursor.execute(query1)
        data = cursor.fetchall()
        return render_template("edit_orders.j2", data = data)

# customers
@app.route('/customers', methods = ["POST", "GET"])
def customers():
    # READ
    if request.method == "GET":

        query = "SELECT customer_id AS 'ID', customer_name AS 'Customer Name', phone_number AS 'Phone Number' FROM Customers;"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        # render edit_customer page passing query data to the edit_customers template
        return render_template("customers.j2", data = data)

    # ADD NEW
    if request.method == "POST":
        if request.form.get("add_customer"):
            customer_name = request.form["customer_name"]
            phone_number = request.form["phone_number"]

            query = "INSERT INTO Customers (customer_name, phone_number) VALUES (%s, %s);"
            cursor = mysql.connection.cursor()
            cursor.execute(query, (customer_name, phone_number))
            mysql.connection.commit()

            return redirect("/customers")



@app.route('/delete_customers/<int:id>')
def delete_customers(id):
    query = "DELETE FROM Customers WHERE customer_id = %s;"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/customers")

@app.route('/edit_customers/<int:id>', methods = ['GET', 'POST'])
def edit_customers(id):

    if request.method == "POST":
        customer_name = request.form["customer_name"]
        phone_number = request.form["phone_number"]

        query = "UPDATE Customers SET customer_name = %s, phone_number = %s WHERE customer_id = %s;"
        values = (customer_name, phone_number, id)
        cursor = mysql.connection.cursor()
        cursor.execute(query, values)
        mysql.connection.commit()

        return redirect("/customers")

    if request.method == "GET":
        query1 = "SELECT customer_id AS customerID, customer_name AS customerName, phone_number AS phoneNumber FROM Customers WHERE customer_id = %s;" % (id)
        cursor = mysql.connection.cursor()
        cursor.execute(query1)
        data = cursor.fetchall()
        return render_template("edit_customers.j2", data = data)

# dishes
@app.route('/dishes', methods = ["POST", "GET"])
def dishes():
    # READ
    if request.method == "GET":

        query = "SELECT dish_id AS 'ID', dish_name AS 'dishName', price AS 'Price' FROM Dishes;"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        # render edit_customer page passing query data to the edit_customers template
        return render_template("dishes.j2", data = data)

    # ADD NEW
    if request.method == "POST":
        if request.form.get("add_dish"):
            dish_name = request.form["dish_name"]
            price = request.form["price"]

            query = "INSERT INTO Dishes (dish_name, price) VALUES (%s, %s);"
            cursor = mysql.connection.cursor()
            cursor.execute(query, (dish_name, price))
            mysql.connection.commit()

            return redirect("/dishes")



@app.route('/delete_dishes/<int:id>')
def delete_dishes(id):
    query = "DELETE FROM Dishes WHERE dish_id = %s;"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/dishes")

@app.route('/edit_dishes/<int:id>', methods = ['GET', 'POST'])
def edit_dishes(id):

    if request.method == "POST":
        dish_name = request.form["dish_name"]
        price = request.form["price"]

        query = "UPDATE Dishes SET dish_name = %s, price = %s WHERE dish_id = %s;"
        values = (dish_name, price, id)
        cursor = mysql.connection.cursor()
        cursor.execute(query, values)
        mysql.connection.commit()

        return redirect("/dishes")

    if request.method == "GET":
        query1 = "SELECT dish_id AS ID, dish_name AS dishName, price FROM Dishes WHERE dish_id = %s;" % (id)
        cursor = mysql.connection.cursor()
        cursor.execute(query1)
        data = cursor.fetchall()
        return render_template("edit_dishes.j2", data = data)

# orders_has_dishes intersection
@app.route('/order_dishes', methods = ["POST", "GET"])
def order_dishes():
    # READ
    if request.method == "GET":

        query = "SELECT order_id AS 'orderID', dish_id AS 'dishID' FROM Orders_has_Dishes;"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        # render edit_order_dishes page passing query data to the edit_order_dishes template
        return render_template("order_dishes.j2", data = data)

    # ADD NEW
    if request.method == "POST":
        if request.form.get("add_order_dishes"):
            order_id = request.form["order_id"]
            dish_id = request.form["dish_id"]

            query = "INSERT INTO Orders_has_Dishes (order_id, dish_id) VALUES (%s, %s);"
            cursor = mysql.connection.cursor()
            cursor.execute(query, (order_id, dish_id))
            mysql.connection.commit()

            return redirect("/order_dishes")

@app.route('/delete_order_dishes/<int:id>')
def delete_order_dishes(id):
    query = "DELETE FROM Orders_has_Dishes WHERE order_id = %s;"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/order_dishes")

@app.route('/edit_order_dishes/<int:id>', methods = ['GET', 'POST'])
def edit_order_dishes(id):

    if request.method == "POST":
        order_id = request.form["order_id"]
        dish_id = request.form["dish_id"]

        query = "UPDATE Orders_has_Dishes SET order_id = %s, dish_id = %s WHERE order_id = %s;"
        values = (order_id, dish_id, id)
        cursor = mysql.connection.cursor()
        cursor.execute(query, values)
        mysql.connection.commit()

        return redirect("/order_dishes")

    if request.method == "GET":
        query1 = "SELECT dish_id AS ID, order_id AS dishName, dish_id FROM Orders_has_Dishes WHERE dish_id = %s;" % (id)
        cursor = mysql.connection.cursor()
        cursor.execute(query1)
        data = cursor.fetchall()
        return render_template("edit_order_dishes.j2", data = data)

# ratings
@app.route('/ratings', methods = ["POST", "GET"])
def ratings():
    # READ
    if request.method == "GET":

        query = "SELECT rating_id AS 'ID', rating AS 'Rating', customer_id AS 'Customer ID', dish_id AS 'Dish ID' FROM Ratings;"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        # render rating page passing query data to the ratings template
        return render_template("ratings.j2", data = data)

    # ADD NEW
    if request.method == "POST":
        if request.form.get("add_rating"):
            rating = request.form["rating"]
            customer_id = request.form["customer_id"]
            dish_id = request.form["dish_id"]

            query = "INSERT INTO Ratings (rating, customer_id, dish_id) VALUES (%s, %s, %s);"
            cursor = mysql.connection.cursor()
            cursor.execute(query, (rating, customer_id, dish_id))
            mysql.connection.commit()

            return redirect("/ratings")

@app.route('/delete_rating/<int:id>')
def delete_rating(id):
    query = "DELETE FROM Ratings WHERE rating_id = %s;"
    cursor = mysql.connection.cursor()
    cursor.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/ratings")

@app.route('/edit_rating/<int:id>', methods = ['GET', 'POST'])
def edit_rating(id):

    if request.method == "POST":
        rating = request.form["rating"]
        customer_id = request.form["customer_id"]
        dish_id = request.form["dish_id"]

        query = "UPDATE Ratings SET rating = %s, customer_id = %s, dish_id = %s WHERE rating_id = %s;"
        values = (rating, customer_id, dish_id, id)
        cursor = mysql.connection.cursor()
        cursor.execute(query, values)
        mysql.connection.commit()

        return redirect("/ratings")

    if request.method == "GET":
        query1 = "SELECT rating_id AS ID, rating, customer_id AS customerID, dish_id AS dishID FROM Ratings WHERE rating_id = %s;" % (id)
        cursor = mysql.connection.cursor()
        cursor.execute(query1)
        data = cursor.fetchall()
        return render_template("edit_rating.j2", data = data)

# dietary_restrictions

#customer_dietary_restrictions

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9549)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True)