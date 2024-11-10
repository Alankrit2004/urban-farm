from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "your_secret_key"


@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        mobile_number = request.form.get("mobile_number")
        email = request.form.get("email")
        password = request.form.get("password")

        if not (first_name and last_name and mobile_number and password):
            return render_template("register.html", message="All fields are required.")
        
        # Here you would typically save the user data to a database

        return redirect("/login")

    return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "password123":
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return "<h1>You have successfully logged in</h1>"

if __name__ == "__main__":
    app.run(debug=True)
