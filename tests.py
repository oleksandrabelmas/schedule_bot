import json


with open('data.json', 'r') as f:
    schdl = json.load(f)

class_numbers = []

for class_number, class_schedule in schdl.items():
    class_numbers.append(class_number)
print(class_numbers)


