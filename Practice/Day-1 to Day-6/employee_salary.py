employees = []

def add_employee():
    
    emp = {}
    emp["ID"] = input("enter employee ID :")
    emp["name"] = input("enter employee name :")
    emp["salary"] = float(input("enter your salary"))
    
    emp["total_salary"] = None
    
    employees.append(emp)
    
def calculate_salary():
    for emp in employees:
        hra = emp["salary"]*0.20
        total = emp["salary"] + hra
        
        emp["total_salary"] = total    

def display_employees():

    if len(employees) == 0:
        print("No Employees Found")

    else:

        for emp in employees:

            print("Employee ID:", emp["ID"])
            print("Name:", emp["name"])
            print("Salary:", emp["salary"])
            print("Total Salary:", emp["total_salary"])


while True:

    print("employee salary system")
    print("1. add employee")
    print("2. calculate salary")
    print("3. display employees")
    print("enter any number for exit")

    choice = input("enter choice: ")

    if choice == "1":
        add_employee()

    elif choice == "2":
        calculate_salary()
        print("salary calculated")

    elif choice == "3":
        display_employees()

    else:
        print("thanks you !")
        break