employees = []

def add_employee():
    
    emp = {}
    emp["ID"] = input("enter employee ID :")
    emp["name"] = input("enter employee name :")
    emp["sallary"] = float(input("enter your sallary"))
    
    employees.append(emp)
    
def calculate_salary():
    for epm in employees:
        hr = epm["sallary"]*0.20
        da = epm["sallary"]*0.10

def display_employees():

    if len(employees) == 0:
        print("No Employees Found")

    else:

        for emp in employees:

            print("Employee ID:", emp["ID"])
            print("Name:", emp["name"])
            print("Salary:", emp["sallary"])
            #print("Total Salary:", emp["total sallary"])


while True:

    print("employee salary system")
    print("1. add employee")
    print("2. calculate salary")
    print("3. display employees")
    print("4. exit")

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