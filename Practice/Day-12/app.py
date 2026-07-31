from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Replace PASSWORD and DATABASE_NAME with your actual values
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:7666090859%40@localhost:5432/AI-Interns"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Intern(db.Model):
    __tablename__ = "employee"

    emp_id = db.Column(db.Integer, primary_key=True)
    emp_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    department = db.Column(db.String(59))
    salary = db.Column(db.Numeric(10, 2))


@app.route("/")
def home():
    interns = Intern.query.all()

    result = ""

    for i in interns:
        result += f"{i.emp_id} | {i.emp_name} | {i.age} | {i.department} | {i.salary}<br>"

    return result


if __name__ == "__main__":
    app.run(debug=True)