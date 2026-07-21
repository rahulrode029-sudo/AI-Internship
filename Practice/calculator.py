
def add(a,b):
    return a + b

def subtract(a,b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b ==   0 :
        return "cannot devide by zero"
    return a / b


while True:

    print("Calculator")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "5":
        break

    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))

    if choice == "1":
        print("Answer =", add(num1, num2))

    elif choice == "2":
        print("Answer =", subtract(num1, num2))

    elif choice == "3":
        print("Answer =", multiply(num1, num2))

    elif choice == "4":
        print("Answer =", divide(num1, num2))
        
    else:
        print("invalid choise")
        break
    
    

