
import random

# for every second:
  #      for each future: 
#   calculates ideal execution amount
def find_max_amount_to_liquidate(position_size, price, underlying_ADV, max_liquidation=None):
        order_size = 0.1 * position_size # Set order size to 10% of position size

        order_notional = order_size * price # Bound order notional from below by min($1000, position_size)
        order_notional = max(
            order_notional,
            min(1000, position_size)
        )
        order_size = order_notional/price 

        if max_liquidation is not None:
            order_size = min(order_size, max_liquidation) # Bound order size from above by max liquidation size remaining
        
        order_size = order_size * random.uniform(0.5, 1.5) # Multiply order size by uniform(0.5, 1.5)

        order_size = min(order_size, position_size) # Bound order size from above by position size 

        if max_liquidation is not None: 
            max_liquidation -= order_size # Decrease max liquidation size remaining by order size
            
        send_order(order_size * random.uniform(0.0001, 0.0005), 1) # Send order uniform(1bp, 5bp) through the book, expiring 1 second later???

        # Set max liquidation size remaining to 0.0001 times the underlying ADV (note: this is a global max shared between all accounts):
        if max_liquidation is not None:
            max_liquidation = max(max_liquidation, 0.00001 * underlying_ADV) 
        else:
            max_liquidation = 0.00001 * underlying_ADV

        print("max liquidation size is now {}".format(max_liquidation))

def send_order(order, expiration): 
    # send order through the book, expiring after expiration sec later
    print("send_order order={} expiration={}".format(order, expiration))


find_max_amount_to_liquidate(2000, 1, 1000000, 2000)