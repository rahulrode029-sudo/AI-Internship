from flask import Flask, request

app = Flask(__name__)

employees = [
    {"Id": 1, "name" : "Rahul", "Role" : "Developer"},
    {"Id": 2, "name" : "Amit", "Role" : "Tester"}
    
]

@app.route("/employees", methods=["GET"])
def get_employees():
    return {"employees": employees}

if __name__ == "__main__":
    app.run(debug=True, port =5000)