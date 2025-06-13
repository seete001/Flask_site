from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.secret_key = '123456'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///submissions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#---------------------------------------------------------------
@app.route("/")
def home():
    return render_template('home.html')
    
#---------------------------------------------------------------
@app.route("/form")
def form():
    return render_template("form.html")

#---------------------------------------------------------------

@app.route("/api/submission", methods = ['GET'])
def api_submission():
    data = []
    if os.path.exists('submissions.txt'):
        with open('submissions.txt', 'r') as f:
            data = [line.strip() for line in f.readlines() if line.strip()]
            return jsonify({'submissions' : data})

#---------------------------------------------------------------
@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username")
    
    if not username:
        flash("❌ Name cannot be empty.", "error")
        return redirect(url_for("form"))

    # Check for duplicates
    with open("submissions.txt", "r") as f:
        existing = [line.strip() for line in f.readlines()]
    
    if username in existing:
        flash("⚠️ That name has already been submitted.", "warning")
        return redirect(url_for('form'))
        
    else:
        with open("submissions.txt", "a") as f:
            f.write(f"{username}\n")
        flash("✅ Name submitted successfully!", "success")
        
    
    return redirect(url_for("form"))  # ✅ make sure this return exists!
#---------------------------------------------------------------
@app.route("/submissions")
def submissions():
    try:
        with open("submissions.txt", "r") as f:
            names = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        names = []
    return render_template("submissions.html", names=names)


#---------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
