from flask import Flask, render_template, request, redirect, send_file
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import requests

app = Flask(__name__)

FILE = "students.csv"


# -------- OOP CLASS --------
class Student:

    def __init__(self, name, skill):
        self.name = name
        self.skill = skill


# -------- SAVE STUDENT --------
def save_student(student):

    with open(FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([student.name, student.skill])


# -------- READ STUDENTS --------
def read_students():

    students = []

    if os.path.exists(FILE):

        with open(FILE, "r") as file:

            reader = csv.reader(file)

            for row in reader:

                students.append({
                    "name": row[0],
                    "skill": row[1]
                })

    return students


# -------- API CALL --------
@app.route("/skill_api")
def skill_api():

    try:
        url = "https://api.publicapis.org/entries"

        response = requests.get(url)

        data = response.json()

        skills = []

        for entry in data["entries"][:10]:
            skills.append(entry["Category"])

        return render_template("skills.html", skills=skills)

    except Exception as e:
        return f"API Error: {e}"


# -------- HOME --------
@app.route("/")

def home():

    return render_template("index.html")


# -------- ADD STUDENT --------
@app.route("/add", methods=["POST"])

def add_student():

    name = request.form.get("name")
    skill = request.form.get("skill")

    student = Student(name, skill)

    save_student(student)

    return redirect("/students")


# -------- SHOW STUDENTS --------
@app.route("/students")

def students():

    data = read_students()

    return render_template("students.html", students=data)


# -------- SKILL GRAPH --------
@app.route("/graph")

def graph():

    df = pd.read_csv(FILE, names=["Name", "Skill"])

    counts = df["Skill"].value_counts()

    counts.plot(kind="bar")

    plt.title("Skill Popularity")

    plt.savefig("skill_graph.png")

    return send_file("skill_graph.png", mimetype="image/png")


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)