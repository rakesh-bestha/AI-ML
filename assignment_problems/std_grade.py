
std_list = ["Rakesh", "Rajesh", "Bharath", "Prudhvi", "Sai", "Manoj"]

std_marks = {
    "Rakesh" :{
            'Maths': 89,
            'Science': 81,
            'English' : 95,
},
    "Rajesh" :{
            'Maths': 84,
            'Science': 72,
            'English' : 69,
},
    "Bharath" :{
            'Maths': 78,
            'Science': 87,
            'English' : 64,
},
    "Prudhvi" :{
            'Maths': 84,
            'Science': 75,
            'English' : 69,
},
    "Sai" :{
            'Maths': 76,
            'Science': 58,
            'English' : 62,
},
    "Manoj" :{
            'Maths': 70,
            'Science': 82,
            'English' : 79,
},

}
#print(std_marks)

sub = ('Maths','Science','English')

unique_grade = set()

print(f"All Student: {std_list}")
#print("All Students:", ", ".join(std_list))
print(f"First 3 Students: {std_list[0:3]}")

top_std = ""
high_avg = 0

for student in std_list:
    total_marks = sum(std_marks[student].values())
    average = total_marks/len(sub)

    if average >= 85:
        grade = 'A'
    elif average >= 70 and average < 85:
        grade = 'B'
    else:
        grade = 'C'
    
    unique_grade.add(grade)

    print(f"{student} - Average: {average:.2f} - Grade: {grade}")
    if average > high_avg:
        high_avg = average
        top_std = student

print(f"Top Student: {top_std}")
print(f"Unique Grades: {sorted(unique_grade)}")
