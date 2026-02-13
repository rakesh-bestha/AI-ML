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
    print(f"Percentage: {percentage}")
    print(f"Status: {status}")
    if status == "PASS":
        if percentage >= 75:
            grade = "A"
        elif percentage >= 60 and percentage < 75:
            grade = "B"
        elif percentage >= 40 and percentage < 60:
            grade = "C"
        
        print(f"Grade: {grade}")
