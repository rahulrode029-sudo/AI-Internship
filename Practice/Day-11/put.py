from flask import Flask, request

app = Flask(__name__)

employees = [
    {"id": 1, "name": "Rahul", "role": "Developer"},
    {"id": 2, "name": "Amit", "role": "Tester"}
]

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

if __name__ == "__main__":
    app.run(debug=True, port=5002)