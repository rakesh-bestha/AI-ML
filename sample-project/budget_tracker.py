
'''To print the welcome statement'''
def show_welcome():
    print("💰 Welcome to Budget Tracker 💰")
    print("-" * 31)

#show_welcome()

'''To show budget and return remianing'''
def get_budget_status(budget, spent):
    remaining = budget - spent
    percentage = (spent/budget) * 100
    print("---Your Budget Status---")
    print("-" * 40)
    print(f"Your Budget: ${budget:.2f}")
    print(f"Total Spend: ${spent:.2f}")
    print(f"Spent Percentage: {percentage:.2f}%")
    print(f"Remaining Budget: ${remaining} ({100-percentage:.1f}% of your Budget left)")
    

    if remaining >= budget * 0.5:
        print("✅ Your Good to Spend More")
    elif remaining < 0:
        print("❌ Be Careful with your spendings")
    else:
        print("❗️ You are Crossing your Budget ")
    print("-    " * 40)
    return remaining
    
#get_budget_status(150, 60)

'''To cross check if we can purchas the item or not?'''
def can_buy(item_price, remaining):
    if item_price > 0 and item_price <= remaining:
        return True
    else:
        return False
    
'''To calculate discount price'''

def calculate_discount(cost, discount):
    discount_price = cost * (discount/100)
    final_prize = cost - discount_price

    print(f"Item Original Cost: ${cost:.2f}")
    print(f"Price After the Discount : ${final_prize:.2f} after {discount}% off")
    
    return final_prize



def main():
    show_welcome()
    budget = float(input("Enter your Budget: "))
    total_spent = 0
    purchase_count = 0

    keep_going = True #to run the loop

    while keep_going:

        remaining = get_budget_status(budget, total_spent)

        print("=" * 40)
        print("MENU")
        print("1.Add an Purchase")
        print("2.Add Multiple Items")
        print("3.Calculate Discount")
        print("4.Exit")
        print("=" * 40)

        choice = int(input("Enter your option (1-4):"))

        if choice == 1:

            print("---Add Purchase Item---")
            item_name = input("Enter the Item Name: ")
            item_price = float(input("Enter Item Price: "))

            if can_buy(item_price, remaining):
                choice = input(f"Want to Buy {item_name} for {item_price:.2f}\nPlease Confirm your Purchase (Yes/No)")
                
                if choice.lower() == "yes":
                    total_spent += item_price
                    purchase_count += 1
                    print(f"Puchased {item_name} ✅")
                else:
                    print("Purchase Cancelled ❌")
            
            else:
                shortage = item_price - budget
                print(f"❌ You can't affford {item_name} need ${shortage:.2f}💵 more.")



        elif choice == 2:
            print("Add Multiple Items to the cart")
            print("Enter Items or Type 'done' to complete the purchase.")
            item_count = 0
            cart_total = 0

            while True:

                item = input(f"Enter {item_count+1} item or done")

                if item.lower() == "done":
                    break
                if item == "":
                    print("Please Enter the Item Name!")
                    continue

                price = float(input(f"Enter {item.capitalize()} Price: "))

                if price <= 0:
                    print("Invalid Price. Try Again!")
                    continue

                cart_total += price
                item_count += 1 
                print("Item Added to the Cart ✅")
            
            if item_count == 0:
                print("No Item Added")
            else:
                print(f"you have added {item_count} and its total is ${cart_total:.2f}")

            '''Checking the Purchase status'''
            affoardable = cart_total <= remaining
            reasonable = cart_total<= remaining * 0.7

            if affoardable and reasonable:
                print("Safe to Purchase")
            elif affoardable and not reasonable:
                print("Your Budget is Tight❗️")
            else:
                print("Can't Afford this Cart")

            '''ask to purchase the cart'''
            if affoardable:
                confirm = input(f"Proceed to Purchase (Yes/No)? ")

                if confirm.lower() == "yes":
                    total_spent = cart_total
                    purchase_count = item_count
                    print(f"Purchasing of {item_count} items Completed ✅") 
            


        elif choice == 3:
            print("--Discount Calculator---")
            original = float(input(f"Enter the Original Price: "))
            discount = float(input(f"Enter the Discount percentage given: "))

            if discount < 0 and discount > 100:
                print("Invalid Discount")
                continue


            final = calculate_discount(original, discount)

            if can_buy(final, remaining):
                print("✅ Can Afford to Buy")
            else:
                print("❌ Cant Buy, Out of Budget")

        elif choice == 4:
            keep_going = False
            print("\n-" * 20)
            print("Exiting Application")
            print("-" * 20)
        else:
            print("❌ Invalid Input ❌")
    


main()


