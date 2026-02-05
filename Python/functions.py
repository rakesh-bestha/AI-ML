# Functions

Function let you create a task once and you can use it more than once in your code.
"""

def greet():
  print("Hello, Everyone!")

greet()



"""Parameter is the variable defined in a function, and an argument is the actual value passed to the function"""

def greeting(name):
  print("Hello", name)

greeting("Rakesh")

def add_num(num1, num2):
  print(f"{num1} + {num2} = {num1 + num2}")

add_num(10, 2)

"""# Defalt Parameters"""

def create_profile(name, age, city):
  print(f"Name: {name}\nAge: {age}\nCity: {city}")

create_profile("Rakesh", 22, "BLR")

"""When you dont know arguments number in you function just use * in it"""

def cal(*num):
  total = 0
  for n in num:
    total += n
  print(total)

cal(1, 2, 3)
cal(64,73,23,92,18,23)
cal(100)

"""Return"""

def cal_area(length, width):
  print(length * width)

area = cal_area(10, 20)
print(area)

# 200
# None

def cal_area(length, width):
  print(length * width)
  return length * width
  print(length * width) #this line skips

area = cal_area(10, 20)
print(area)

def square(num):
  return num * num

square(10)

def check_num(num):
  if num > 0:
    return "Positive Number"
  elif num < 0:
    return "Negative Number"
  else:
    return "Zero"

check_num(10)
check_num(-10)
check_num(0)
check_num(100)

"""# Calculator"""

def add(num1, num2):
  return num1 + num2

def sub(num1, num2):
  return num1 - num2

def mul(num1, num2):
  return num1 * num2

def div(num1, num2):
  if num2 == 0:
    return "Cannot divide by zero"
  else:
    return num1 / num2

def calculate(a, b , operation):
  if operation == "add":
    return add(a, b)

  elif operation == "sub":
    return sub(a, b)

  elif operation == "mul":
    return mul(a, b)

  elif operation == "sub":
    return sub(a, b)

calculate(10, 20, "add") # 30
calculate(10, 20, "sub") # -10
