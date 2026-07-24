# todo_app.py

tasks = []

while True:

    print("1. view task")
    print("2. add tasks")
    print("3. remove task")
    print("enter any number for exit")

    choice = input("enter your choice: ")
    
    if choice == "1":
        print("tasks:")
        for task in tasks:
            print(task)

    elif choice == "2":
        task = input("enter task: ")
        tasks.append(task)
        print("task added!")

    elif choice == "3":
        task = input("enter task to remove: ")

        if task in tasks:
            tasks.remove(task)
            print("task removed!")
        else:
            print("task not found.")

    else:
        print("thanks you !")
        break