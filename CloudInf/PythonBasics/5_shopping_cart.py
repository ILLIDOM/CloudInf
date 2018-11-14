shopping_cart = {'banana': 3,
                 'apple': 5,
                 'milk': 10,
                 'beer': 12
}

prices = {
    'banana': 0.6,
    'beer': 1.1,
    'milk': 1.7,
    'apple': 0.6,
    'coca cola': 1.2,
    'kiwi': 0.7
}

def sum_all_prices(cart):
    sum = 0;
    for items in cart:
        sum += prices[items] * cart[items]
    return sum

print("Total price is: " + str(sum_all_prices(shopping_cart)))

