from flask import Flask

app = Flask(__name__)

employees = [
    {"id": 1, "name": "Rahul", "role": "Developer"},
    {"id": 2, "name": "Amit", "role": "Tester"}
]

@app.route("/employees/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    employee = next((e for e in employees if e["id"] == emp_id), None)
    if not employee:
        return {"error": "Employee not found"}, 404

    employees.remove(employee)
    return {"message": "Employee Deleted", "employee": employee}

if __name__ == "__main__":
    app.run(debug=True, port=5003)