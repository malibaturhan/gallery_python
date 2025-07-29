import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from forms import *
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from utility import *

from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user

UPLOAD_FOLDER = "./static/uploads"


upload_folder_exists = check_upload_file_folder()
if not upload_folder_exists:
    create_upload_file_folder(UPLOAD_FOLDER)



def create_images_path_list():
    uploaded_list = os.listdir(UPLOAD_FOLDER)
    paths = build_paths(uploaded_list, "static/uploads")
    return paths


def build_paths(image_list, folder_path):
    paths = []
    for image in image_list:
        path = os.path.join(folder_path, image)
        paths.append(path)
    return paths


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "1234q324234234"

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id_, username, password):
        self.id = id_
        self.username = username
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect("gallery.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password FROM users"
                   "WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(*user_data)
    return None

@app.route("/login", methods = ["GET", "POST"])
def login():
    username = request.form.get("user-name")
    password = request.form.get("password")

    conn = sqlite3.connect("gallery.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, username, password_hash FROM users WHERE username = ?
                   """, (username,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        user_id, username, hashed_password = user_data
        if check_password_hash(hashed_password, password):
            user = User(user_id, username, hashed_password)
            login_user(user)
            flash("Logged in successfully", category="success")
            return redirect(url_for("index"))
        else:
            flash("password or username is faulty", category = "error")
    else:
        flash("there is no such a user")
    return redirect(url_for("index"))

@app.route("/signup", methods = ["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form.get("user-name")
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("gallery.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM users WHERE username = ? or email = ?
    """, (username, email) )
        user_date = cursor.fetchone()
        if user_date:
            flash("This user already exists")
            return redirect(url_for("index"))
        else:
            cursor.execute("""
            INSERT INTO users (username, email, password_hash) VALUES (?,?,?)
""", (username, email, hashed_password))
            conn.commit()
            conn.close()
            flash("user created", category="success")
            return redirect(url_for("index"))
    
    else:
        return render_template("signup.html")


    


@app.route("/profile")
@login_required
def profile():
    return "This is profile page for {current_user.username}"

@app.route("/logout")
@login_required
def logout():
    images = create_images_path_list()
    flash("Successfully logged out")
    return render_template("index.html", images = images)


@app.route("/")
def index():
    images = create_images_path_list()
    return render_template("index.html", images = images)

@app.route("/upload", methods = ["POST"])
def upload_image():
    if 'image' not in request.files:
        flash("no file selected", category="user_error")
        images = create_images_path_list()
        return render_template("index.html", images = images)
    file = request.files["image"]

    if file.filename == "":
        # if user did not select a file then browser submits an empty file name
        # so we have a precaution about it
        flash("no file selected", category="user_error")
        return redirect(url_for("index"))
    
    if file and is_file_allowed(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        flash("image uploaded succesfully", category="success")
        images = create_images_path_list()
        return render_template("index.html", images = images)
    
    flash("user error", category="user_error")
    # turning back to index html
    images = create_images_path_list()
    return render_template("index.html", images = images)

app.run(debug=True)

