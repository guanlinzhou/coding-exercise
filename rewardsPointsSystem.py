from collections import defaultdict

"""

PROBLEM: Management needs to know how many of each item they are selling each 
day and what each customer’s current reward points balance is.

Design a system that parses the log file and:
1) Calculates the reward points for each customer
2) Generates purchase counts for each item sold during the day

Here are some considerations for the rewards system you want to create:

- For each purchase, a customer can spend a certain amount of reward points for 
  their purchase.
- Some customers come to the store multiple times per day.
- Customers earn 1 reward point for every 18 dollars spent, unless they spend 
  more than $250 per day, in which case they earn 1 reward point for every 17 
  dollars spent. These reward points are given to the customers at the **end** 
  of each day, not immediately after the purchase.
- For each LogEntry, we want to keep track of:
    - Customer ID
    - Number of reward points used for that purchase
    - List of items purchased and their prices

There can also be malformed logs in which any of the three properties in the 
LogEntry are 'None'.
If this is the case, please address them in the following ways:
- If there is no customer ID, do not count the rewards points. Instead, only 
  calculate the purchase counts for the items
- If there is no rewards points specified, assume rewards points = 0
- If there is no list of items purchased, then this is an error in the system. 
  Please add this LogEntry to a error log (a list of LogEntry called 'error')

Example- this is written in casual terms, and must be modified to actual data structures
	Items:
		- Banana- $50
		- Apple- $100
	Log Entries:
		- Customer 1 purchased 2 bananas and 1 apple; he used 100 rewards points
		- Customer 2 purchased 1 banana and 1 apple; she used 0 rewards points
		- Customer 1 purchased 1 banana; he used 0 rewards points

"""

class Item:
  def __init__(self, item_id, price):
    self.item_id = item_id
    self.price = price

class RewardsSystem:

  # The amount spent to points recieved ratios.
  # Use depending whether the customer spends ABOVE or BELOW REWARDS_CUTOFF.
  REWARDS_RATIO_ABOVE = 17
  REWARDS_RATIO_BELOW = 18
  REWARDS_CUTOFF = 250

  # Initializes field variables to a default 0 dictionary.
  def __init__(self):
    self.rewards_points = defaultdict(int)
    self.items_purchased = defaultdict(int)

  # Processes a single log and all of its entries.
  def process_log(self, log):
    amount_spent = defaultdict(int)

    # For each entry in this log, modify points based on the items purchased.
    for entry in log:
      customer_id, points_used, items_purchased = entry[:3]

      # Calculate the total amount spent
      # Increment the number items purchased for each item
      total_spent = 0
      for item in items_purchased:
        total_spent += item.item_id * item.price
        self.items_purchased[item.item_id] += 1

      # If a customer is using points, subtract the number of points used.
      # Print the total number of points remaining.
      if customer_id:
        self.rewards_points[customer_id] -= points_used
        amount_spent[customer_id] += total_spent
        print(self.rewards_points)
      elif len(items_purchased) == 0:
        raise ValueError('Items purchased were not recorded.')
        
    # At end of day, award reward points back to customers based on how much they spent
    for customer_id, amount in amount_spent.items():

      # Calculate rewards points received
      rewards_points = amount // RewardsSystem.REWARDS_RATIO_BELOW
      if amount_spent > RewardsSystem.REWARDS_CUTOFF:
        rewards_points =  amount // RewardsSystem.REWARDS_RATIO_ABOVE

      # Update customer rewards points
      self.rewards_points[customer_id] += rewards_points

  # Getter method to recieve the number of a certain item purchased
  def get_items_purchased(self, item_id):
    return self.items_purchased[item_id]
