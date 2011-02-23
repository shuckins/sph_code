#!/usr/bin/env python
overhead = 1.50
shipping_price_per_pound = .86
coffee_price = 10.50

def order_cost(pounds):
    """
    Calculates the price of an order based on the cost per pound, shipping per
    pound, and constant overhead.
    
    pounds -- Pounds of coffee in order.
    """
    order_cost = (coffee_price * pounds) + overhead + \
        (shipping_price_per_pound * pounds)
    return order_cost

def main():
    """
    Provides main program control.
    """
    pounds = float(raw_input("Number of pounds to order: "))
    cost = order_cost(pounds)
    print "Cost of coffee per pound: $%0.2f" % coffee_price
    print "Shipping per pound:       $%0.2f" % shipping_price_per_pound
    print "Overhead:                 $%0.2f" % overhead
    print "-------------------------------"
    print "Total due:                $%0.2f" % cost

if __name__ == '__main__':
    main()
