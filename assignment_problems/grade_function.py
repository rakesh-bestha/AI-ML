def calculate_grade(*score, **adjustment):
    average = sum(score)/len(score)
    bonus = sum(adjustment.values())
    return average + bonus

grade1 = calculate_grade(85, 90,78)
print(f"Final Grade: {grade1:.2f}%")
grade2 = calculate_grade(70,65,80,attandnance = 5, project = 10)
print(f"Final Grade: {grade2:.2f}%")
