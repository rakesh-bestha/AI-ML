'''
Problem Statement:
Write a simple Python program to evaluate a student's result using conditional statements.

Requirements:
Ask the user to enter:Student name, Marks in Maths, Science, and English

Validate the marks:
If any mark is less than 0 or greater than 100, print Invalid marks entered and stop the program.

Calculate:
Total marks
Average percentage
Determine Pass / Fail:

If any subject mark is below 40, the student fails
Otherwise, the student passes
If the student passes, assign a grade:

A → Average ≥ 75
B → Average ≥ 60 and < 75
C → Average ≥ 40 and < 60
Display:

Student name
Total marks
Average percentage (2 decimal places)
Pass/Fail status
Grade (only if passed)
Expected Interaction:
Enter student name: Rahul

Enter Maths marks: 78

Enter Science marks: 65

Enter English marks: 82

Student Name: Rahul

Total Marks: 225

Percentage: 75.00

Status: PASS

Grade: A

'''

std_name = input("Enter Student Name: ")
math_marks = int(input("Enter Maths Marks: "))
sci_marks = int(input("Enter Science Marks: "))
eng_marks = int(input("Enter English Marks: "))



if (math_marks < 0 or math_marks>100 or eng_marks < 0 or eng_marks>100 or sci_marks < 0 or sci_marks>100):
    print("Invalid Marks")
else:
    total_marks = math_marks + sci_marks + eng_marks
    percentage = total_marks/3

    if math_marks < 40 or eng_marks < 40 or sci_marks < 40:
        status = "FAIL"
    else:
        status = "PASS"

    print(f"Student Name: {std_name}")
    print(f"Total Marks: {total_marks}")
    print(f"Percentage: {percentage:.2f}")
    print(f"Status: {status}")
    if status == "PASS":
        if percentage >= 75:
            grade = "A"
        elif percentage >= 60 and percentage < 75:
            grade = "B"
        elif percentage >= 40 and percentage < 60:
            grade = "C"
        
        print(f"Grade: {grade}")
