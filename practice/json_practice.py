import json

json_string = '''{
                "student":{
                    "name" : "Rakesh",
                    "marks" : [85,90,88]
                }
                }'''

#print name of the student

data = json.loads(json_string) #converting/parsing/loading from python to JSON format

name = data["student"]["name"]
print(f"Name of the Student: {name}")

#second marks

s_mark = data["student"]["marks"][1]

print(f"Secong mark from the list: {s_mark}")

#average of marks

avg = sum(data["student"]["marks"])/ len(data["student"]["marks"])
print(f"Average of marks: {avg:.2f}")

