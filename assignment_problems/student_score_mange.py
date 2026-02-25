#Using File_Handling 

with open("student.txt",'w') as write_file:
    write_file.write("Alice,85\nBob,92\nCharlie,78\nDiana,95") 
    write_file.close()

try:
    with open("student.txt","r") as read_file:
        for line in read_file:
            line = line.strip()
            name, score = line.split(",")
            print(f"Student: {name}, Score: {score}")
except FileNotFoundError:
    print("File not Exist")

    
with open("student.txt", "a") as add_file:
    add_file.write("\nEve,88")

with open("activity.log", "w") as log_file:
    log_file.write("Added new student: Eve")







