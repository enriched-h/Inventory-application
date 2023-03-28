from tabulate import tabulate
import pickle 

class Shoe:
          # Initialise elements of a shoew
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

        
        # Open and read inventory file to get the shoe cost
    def get_cost(self):
        with open('inventory.txt','r')as inventory_file:
            for line in inventory_file:
                field = line.strip().split(',')
                # If the country the user enters matches the country in the file, then we receve the cost
                if field[0] == self.country:
                   self.cost = float(field[3])
            return self.cost
      
        
        # Open and read inventory file to get the shoe quantity
    def get_quantity(self):
        with open('inventory.txt','r')as inventory_file:
            for line in inventory_file:
                field = line.strip().split(',')
                # If the country the user enters matches the country in the file, then we receve the quantity
                if field[0] == self.country:
                   self.quantity = int(field[4])
            return self.quantity
       
        
        # Return a string representation of a shoe
    def __str__(self):
        return f"Country: {self.country}, Code: {self.code}, Product: {self.product}, Cost: {self.cost}, Quantity: {self.quantity}"
    
# The list will be used to store a list of objects of shoes.

shoe_list = []


def read_shoes_data():
    
    try:
        with open('inventory.txt', 'r') as inventory_file:
            # Skip the first line in the file
            inventory_file.readline()
            for line in inventory_file:
                field = line.strip().split(',')
                new_shoe = Shoe(field[0], field[1], field[2], float(field[3]), int(field[4]))
                shoe_list.append(new_shoe)
                print(new_shoe)
    except FileNotFoundError:
        print("Error: The inventory file is not found!")
    except ValueError:
        print("Error: The cost or quantity of a shoe is not a valid number!")
    return shoe_list
   

def capture_shoes():
    # Add shoe to a shoe list
    
    country = input("Please enter the country of the shoe ")
    code = input("Please enter the code of the shoe ")
    product = input("Please enter the product name of the shoe ")
    cost = float(input("Please enter the cost of the shoe "))
    quantity = int(input("Please enter the quantity of the shoe "))

    add_shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(add_shoe)

    new_shoe = f"\n{country},{code},{product},{cost},{quantity}\n"
    
    with open ('inventory.txt','a+') as inventory_file:
        inventory_file.write(new_shoe)
    print("\nShoe has been added to the shoe list")

    return shoe_list



def view_all():
    for shoe in shoe_list:
        print(shoe.__str__())


def re_stock():
    with open('inventory.txt', 'r') as inventory_file:
        inventory_file.readline()  # Skip header line

        # Find the shoe with the smallest quantity
        fields = (line.strip().split(',') for line in inventory_file)
        small_qnty = min(int(field[4]) for field in fields)

        # Reset file pointer to beginning
        inventory_file.seek(0)
        inventory_file.readline()

        for line in inventory_file:
            field = line.strip().split(',')
            if int(field[4]) == small_qnty:
                shoe = {
                    'Country': field[0],
                    'Code': field[1],
                    'Product': field[2],
                    'Cost': float(field[3]),
                    'Quantity': small_qnty
                }
                shoe_list.append(shoe)
                break

        print("This is the shoe with the lowest quantity on the shoe list: ")
        print(shoe)

        user_restock_option = input("Would you like to enter a new value for the shoe quantity? Enter Y or N: ").lower()
        if user_restock_option == "y":
            # Allow the user to enter a new quantity value
            new_quantity = input("Enter a new quantity value for the shoe: ")
            shoe['Quantity'] = int(new_quantity)

            # Read in the contents of the file
            with open('inventory.txt', 'r') as inventory_file:
                lines = inventory_file.readlines()

            # Modify the relevant line
            for i, line in enumerate(lines[1:]):  # Skip header line
                fields = line.strip().split(',')
                if fields[0] == shoe['Country'] and fields[1] == shoe['Code']:
                    fields[4] = str(shoe['Quantity'])
                    lines[i+1] = ','.join(fields) + '\n'
                    break

            # Write the entire contents of the modified file back to the original file
            with open('inventory.txt', 'w') as inventory_file:
                inventory_file.writelines(lines)

            print("The shoe quantity has been updated.")
        else:
            print("The shoe quantity has not been updated.")

    return shoe


def search_shoe(user_code):
    with open('inventory.txt', 'r') as inventory_file:
        # Skip the first line in the file
        inventory_file.readline()
        for line in inventory_file:
            fields = line.strip().split(',')
            if user_code == fields[1]:  # Check if the shoe code matches the user given code
                # Create a dictionary to store the shoe object
                shoe = {
                    'Country': fields[0],
                    'Code': fields[1],
                    'Product': fields[2],
                    'Cost': fields[3],
                    'Quantity': fields[4]
                }
                print(shoe)  #Return the shoe object if found
                return
        #If the shoe is not found, return None
        return print(f"No shoe with this code found")


def value_per_item():
    # Initialize an empty list to store the data
    data = []
    
    with open('inventory.txt', 'r') as inventory_file:
        # Skip the first line in the file
        inventory_file.readline()
        for line in inventory_file:
            fields = line.strip().split(',')
            
            #Append tuple containing the values for the current item
            data.append([
                fields[0],  
                fields[1], 
                fields[2],  
                float(fields[3]),  
                int(fields[4]),  
                float(fields[3]) * int(fields[4])  # Value
            ])
    
    # Print the data using the tabulate function
    headers = ['Country', 'Code', 'Product', 'Cost', 'Quantity', 'Value']
    print(tabulate(data, headers=headers, floatfmt=".2f"))
        

def highest_qty():
    with open('inventory.txt','r') as inventory_file:
        inventory_file.readline()

        fields = (line.strip().split(',') for line in inventory_file)
        #Same code as re_stock()
        high_qnty = max(int(field[4]) for field in fields)
        
        # Reset file pointer to beginning
        inventory_file.seek(0) 
        #Skip header line 
        inventory_file.readline()  
        for line in inventory_file:
            field = line.strip().split(',')
            if int(field[4]) == high_qnty:
                shoe = {
                    'Country': field[0],
                    'Code': field[1],
                    'Product': field[2],
                    'Cost': float(field[3]),
                    'Quantity': high_qnty
                }
                break

        print("This is the shoe with the highest quantity on the shoe list that is for sale")
        print(shoe)
        return high_qnty
  

usage_message = '''
Welcome to the shoe factory! What would you like to do?

   r - read shoe data.
   a - add shoe to shoe list.
  va - view all shoes. 
  rs - re-stock.
   s - search for shoe.
 vpi - value per item.
   h - highest quality.
   e - exit this program.
'''

user_choice = ""
while True:
        
    user_choice = input(usage_message).strip().lower()
    if user_choice == "r":
        read_shoes_data()

    elif user_choice == "a":

        capture_shoes()
        
        
        
    elif user_choice == "va":
        view_all()
                 
    elif user_choice == "rs":
        re_stock()          

    elif user_choice == "s":
        user_code = input("Please enter the code for the shoe you would like to search ")
        search_shoe(user_code)      

    elif user_choice == "vpi":
        value_per_item()

    elif user_choice == "h":
        highest_qty()

    elif user_choice == "e":
         print("Goodbye")
         break

    else:
        print("OOPS - incorrect input")


'''
- Your 'Add Shoe' option is not adding the shoe information to the text file, which means that the 
shoe is not being saved and is disappearing once the application is closed. You have done an awesome
job with creating a new shoe object and appending to your shoe list, but you'll just need to also append
the information to your text file.

Everything else is working really well. :)
'''