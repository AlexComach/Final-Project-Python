from bs4 import BeautifulSoup
import requests
from tabulate import tabulate
import csv

cart = []

def parsing():
    while True:
        try:
            item = input("Please Input OSRS item to add to cart: ").lower()
            url_item = item.replace(" ", "_").capitalize() 
            url = f"https://oldschool.runescape.wiki/w/{url_item}"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"
            }
            result = requests.get(url, headers=headers)
            doc = BeautifulSoup(result.text, "html.parser")
    
            price = doc.find("span", class_="infobox-quantity-replace").text
            int_price = int(price.strip().replace(",", ""))
            print(f"{price} coins")
            return item, int_price
            
        except (AttributeError, ValueError):
            print("Item is not on the GE")
            return None, None

def calculate(item, int_price):
    while True:
        try:    
            quantity = int(input("Input how many would you like to add to cart: "))
            
            if quantity > 0:
                total = int_price * quantity
                item_description = {
                                    "Item" : item,
                                    "Price" : f"{int_price:,} coins",
                                    "Quantity" : quantity,
                                    "Total" : f"{total:,} coins"
                                    }
                cart.append(item_description)
                return cart
                
            else:
                print("Invalid Input")
                return False

        except ValueError:
            print("Not a valid input.")
            return False

def end():
    final_total = 0
    for item_description in cart:
        final_total += int((item_description["Total"]).strip().replace(",", "").replace(" coins", ""))
    receipt = tabulate(cart, headers="keys", tablefmt="mixed_outline")
    receipt += f"\n\n                       Final Total: {final_total:,} coins\n"
    print(receipt)
    
    return cart, final_total

def store():
    cart, final_total = end()
    headers=["Item","Price","Quantity","Total","Final Total"]
    
    final_receipt = {        "Item" : "",
                                    "Price" : "",
                                    "Quantity" : "",
                                    "Total" : "",
                                    "Final Total":final_total
                                    }
    cart.append(final_receipt)
        
    separator = {"Item": "---------------------------------------------------", "Price": "", "Quantity": "", "Final Total":""} 

    try:
        with open("storage.csv", mode="x", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerow(separator)
            
    except FileExistsError:
        pass


    with open("storage.csv", mode="a", newline='') as file:

        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writerows(cart)
        writer.writerow(separator)
        return cart

def backup():       
    with open("storage.csv", "r") as infile:
        reader = csv.reader(infile)

        with open("backup_storage.csv", "w", newline='') as outfile:
            writer = csv.writer(outfile)
            for row in reader:
                writer.writerow(row)

def main():
    while True:
        item, price = parsing()  
        
        if item and price:
            calculate(item, price)
            end()  
            
        choice = input("Would you like to add another item? (Y/N): ").strip().upper()
        if choice == "N":
            break
        elif choice == "Y":
            continue
        else:
            print("Invalid Input")
            break

    store()
    backup()

if __name__ == "__main__":
    main()

    
    
    
