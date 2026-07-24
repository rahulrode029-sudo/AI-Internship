import numpy as np


marks = np.array([78, 88, 39, 92, 67, 85, 40, 95, 73, 81, 39, 41])

print("student marks", marks)

print("highest marks :", np.max(marks))

print("lowest marks :", np.min(marks))

print(" avrage marks :", np.mean(marks))

print("median marks :", np.median(marks))

print("standerd deviation :", np.std(marks))

print(marks[marks> 80])

print(np.sort(marks))

print("Check student Pass OR Fail :")

for mark in marks : 
    if mark > 40:
        print(mark, ": Pass")
    else:
        print( mark,": fail")


 