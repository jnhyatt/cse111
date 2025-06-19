import csv
from itertools import islice
from datetime import datetime


def read_dictionary(filename, key_column_index=0):
    with open(filename, "r") as file:
        return {
            row[key_column_index]: [
                *row[:key_column_index],
                *row[key_column_index + 1 :],
            ]
            for row in islice(csv.reader(file), 1, None)
        }


def main():
    products_dict = read_dictionary("products.csv")
    total_items = 0
    subtotal = 0

    print("StoreCo")

    with open("request.csv", "r") as file:
        for item in islice(csv.reader(file), 1, None):
            prod_id = item[0]
            quantity = int(item[1])

            product = products_dict[prod_id]
            name = product[0]
            price = float(product[1])

            print(f"{name}: {quantity} @ {price:.2f}")
            total_items += quantity
            subtotal += price * quantity

    tax = subtotal * 0.06
    total = subtotal + tax

    print(f"Number of Items: {total_items}")
    print(f"Subtotal: {subtotal:.2f}")
    print(f"Sales Tax: {tax:.2f}")
    print(f"Total: {total:.2f}")
    print("Thank you for shopping at StoreCo.")
    print(datetime.now().strftime("%a %b %e %H:%M:%S %Y"))


if __name__ == "__main__":
    main()
