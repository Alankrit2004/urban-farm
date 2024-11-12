from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "alankrit_321#"
app.config["MYSQL_DB"] = "user_auth_db"

mysql = MySQL(app)

app.secret_key = "your_secret_key"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mobile = request.form["mobile_number"]
        password = request.form["password"]

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE mobile_number = %s", (mobile,))
        user = cursor.fetchone()
        cursor.close()

        # Debugging: Log the user fetched from the database
        print("Fetched user:", user)

        if user:
            if user[4] == password:  # Assuming password is the 5th column
                flash("Login Successful!", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Incorrect password. Please try again.", "danger")
        else:
            flash("Invalid mobile number. Please try again.", "danger")
        
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        mobile_number = request.form["mobile_number"]
        email = request.form["email"]
        password = request.form["password"]

        if not (first_name and last_name and mobile_number and password):
            return render_template("register.html", message="All fields are required.")

        # Insert user data into the database
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO users VALUES(%s, %s, %s, %s, %s)", 
            (first_name, last_name, email, mobile_number, password)
        )
        mysql.connection.commit()
        cursor.close()

        flash("Registration Successful! You can now log in.", "success")
        return redirect("/")

    return render_template("register.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return "<h1>You have successfully logged in</h1>"

if __name__ == "__main__":
    app.run(debug=True)
