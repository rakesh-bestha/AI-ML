import numpy as np

np.random.seed(42)
print(np.random.randint(1,5,6))

score = np.random.randint(50,101, size=(5,4))
print("Score:\n", score)

print(f"3rd Student 2nd Subject Score: {score[2,1]}")
print(f"last 2 students all subject marks:\n {score[-2:]}")
print(f"First 3 students 2&3 Subjects:\n {score[:3, 1:3]}")

#Task - 2

column_mean = np.round(score.mean(axis=0), 2)
print(f"Column Mean: {column_mean}")

curve = [5,3,7,2]
curve_score = score + curve
curve_score = np.clip(curve_score, 1,100)
print(f"Curve Score:\n {curve_score}")

row_max = curve_score.max(axis=1, keepdims=True)
print(f"Row wise max value: {row_max}")

#Task -3

row_min = curve_score.min(axis=1 , keepdims=True)

normalize = (curve_score-row_min)/(row_max-row_min)
print(f"Normalized Score:\n {normalize}")

max_index = np.unravel_index(np.argmax(normalize), normalize.shape)

print("Student index:", max_index[0])
print("Subject index:", max_index[1])

above_90 = curve_score [curve_score > 90]
print("Scores above 90:", above_90)