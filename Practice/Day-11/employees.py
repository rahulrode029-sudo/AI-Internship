from flask import Flask, request

app = Flask(__name__)

employees = [
    {"id": 1, "name": "Rahul", "role": "IT"},
    {"id": 2, "name": "Amit", "role": "HR"},
    {"id": 3, "name": "sahil", "role": "Devloper"}
]

@app.route("/employees", methods=["GET"])
def get_employees():
    return {"employees": employees}

@app.route("/employees/<int:emp_id>", methods=["GET"])
def get_employee(emp_id):
    employee = next((e for e in employees if e["id"] == emp_id), None)
    if not employee:
        return {"error": "Employee not found"}, 404
    return {"employee": employee}

@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.get_json(silent=True)
    if not data or "name" not in data or "role" not in data:
        return {"error": "Invalid payload, 'name' and 'role' are required"}, 400

    new_id = max((e["id"] for e in employees), default=0) + 1
    new_employee = {"id": new_id, "name": data["name"], "role": data["role"]}
    employees.append(new_employee)

    return {"message": "Employee Added", "employee": new_employee}, 201

@app.route("/employees/<int:emp_id>", methods=["PUT"])
def update_employee(emp_id):
    data = request.get_json(silent=True)
    if not data:
        return {"error": "Invalid payload"}, 400

    employee = next((e for e in employees if e["id"] == emp_id), None)
    if not employee:
        return {"error": "Employee not found"}, 404

    employee["name"] = data.get("name", employee["name"])
    employee["role"] = data.get("role", employee["role"])

    return {"message": "Employee Updated", "employee": employee}

@app.route("/employees/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    employee = next((e for e in employees if e["id"] == emp_id), None)
    if not employee:
        return {"error": "Employee not found"}, 404

    employees.remove(employee)
    return {"message": "Employee Deleted", "employee": employee}

if __name__ == "__main__":
    app.run(debug=True)