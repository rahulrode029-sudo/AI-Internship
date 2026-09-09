from flask import Flask, request

app = Flask(__name__)

employees = [
    {"id": 1, "name": "Rahul", "role": "Developer"},
    {"id": 2, "name": "Amit", "role": "Tester"}
]

@app.route("/employees", methods=["GET"])
def get_employees():
    return {"employees": employees}

@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.get_json()
    employees.append(data)
    return {
        "message":"Employee Added",
        "employee":data
    },201
    
if __name__ == "__main__":
    app.run(debug=True)
    
