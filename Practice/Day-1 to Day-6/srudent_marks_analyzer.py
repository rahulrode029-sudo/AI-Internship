
def get_student_marks():
    students ={ }
    
    n = int(input("enter number of students :"))
    
    for i in range(n):
        name = input("enter student name :")
        marks = float(input("enter marks:"))
        students[name] = marks
        
    return students

def calculate_statistics(students):
    marks = list(students.values())
    
    highest = max(marks)
    lowest = min(marks)
    average = sum(marks)/len(marks)
    
    return highest, lowest, average    

def display_above_average (students, average):
    print("student scoring above average :")
    
    found = False
    
    for name, marks in students.items():
        if marks > average :
            print(name,":", marks)
            found = True
            
    if not found :
        print("no student scored above average")
        
def main():
    students = get_student_marks()

    highest, lowest, average = calculate_statistics(students)

    print("\nHighest Marks:", highest)
    print("Lowest Marks:", lowest)
    print("Average Marks:", round(average, 2))

    display_above_average(students, average)   


main()          