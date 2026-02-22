shopping_list = [
    {"item": "Milk", "price": 50},
    {"item": "Bread", "price": 30},
    {"item": "Eggs", "price": 60},
    {"item": "Rice", "price": 120}
]

#Task-1:

shopping_list.append({"item": "Butter", "price": 80})

shopping_list.pop(0)
print(shopping_list)

'''
[{'item': 'Bread', 'price': 30}, 
{'item': 'Eggs', 'price': 60}, 
{'item': 'Rice', 'price': 120}, 
{'item': 'Butter', 'price': 80}]
'''

#Task-2
total_cost = 0
expensive_item = ""
exp_item_price = 0
item_count = 0

'''for items in shopping_list:
    item , cost = items
    total_cost += int(cost)'''

#total_cost = sum(item["price"] for item in shopping_list)
for products in shopping_list:
    item , price = products["item"], products["price"]
    total_cost += price
    item_count += 1

    if price > exp_item_price:
        exp_item_price = price
        expensive_item = item


print()
print(f"Total Cost is: {total_cost}")
print(f"The Expensive Item is {expensive_item} and its cost is {exp_item_price}")


#Task-3

summury = {
    "total_items" : item_count,
    "tot_cost" : total_cost,
    "average_cost" : total_cost/len(shopping_list)
}

print(summury)

'''
[{'item': 'Bread', 'price': 30}, {'item': 'Eggs', 'price': 60}, {'item': 'Rice', 'price': 120}, {'item': 'Butter', 'price': 80}]

Total Cost is: 290
The Expensive Item is Rice and its cost is 120
{'total_items': 4, 'tot_cost': 290, 'average_cost': 72.5}
'''
