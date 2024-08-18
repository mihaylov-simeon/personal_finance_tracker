import pandas as pd  # Importing the pandas library, which helps us work with data in tables.
import csv  # Importing the csv module, which helps us read and write CSV (Comma-Separated Values) files.
from datetime import datetime  # Importing the datetime module to work with dates and times.

# Importing functions from another file called data_entry.
# These functions will get input from the user, such as date, amount, category, and description.
from data_entry import get_date, get_amount, get_category, get_description

# Defining a class called CSV that will handle our CSV file operations.
class CSV:
    # This is a constant variable that holds the name of the CSV file where we store data.
    CSV_FILE = "finance_data.csv"
    
    # These are the column names for our CSV file.
    COLUMNS = ['date', 'amount', 'category', 'description']
    
    # This is the format in which dates will be stored in the CSV file (e.g., "18-08-2024").
    FORMAT = "%d-%m-%Y"

    """
    This function checks if the CSV file already exists. If it doesn't, it creates a new one
    with the specified columns (date, amount, category, description).
    """
    @classmethod
    def initialize_csv(cls):
        try:
            # Try to read the CSV file. If it exists, do nothing.
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            # If the file doesn't exist, create a new one with the specified columns.
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)
            
    # This function adds a new entry (row) to the CSV file.
    @classmethod
    def add_entry(cls, date, amount, category, description):
        # Store the new entry data in a dictionary (a way to organize key-value pairs).
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }

        """ 
        Open the CSV file in append mode ("a"), which means we are adding to the end of the file.
        The 'newline=""' argument makes sure that no extra lines are added between entries.
        """
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            # Create a CSV writer object to write the new entry into the file.
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            # Write the new entry (a new row) to the file.
            writer.writerow(new_entry)
        # Print a message to the console to confirm the entry was added successfully.
        print("Entry added successfully!")

    # This function retrieves transactions between two dates.
    @classmethod
    def get_transaction(cls, start_date, end_date):
        # Read the CSV file into a pandas DataFrame (a table of data).
        df = pd.read_csv(cls.CSV_FILE)
        
        # Convert the 'date' column to datetime format for easier comparison.
        df['date'] = pd.to_datetime(df['date'], format=cls.FORMAT)
        
        # Convert the user-provided start and end dates into datetime objects.
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        # Create a mask (a filter) to find rows where the date is within the specified range.
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        
        # Use the mask to filter the DataFrame to only include rows where the date is within the specified range.
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            # Check if the filtered DataFrame is empty (i.e., no transactions were found within the specified date range).
            # If it is empty, print a message saying that no transactions were found.
            print('No transactions found in the given date range.')
        else:
            # If the filtered DataFrame is not empty (i.e., transactions were found within the date range):
            
            # Print a message showing the start and end dates of the transactions found.
            # The dates are formatted according to the format specified in CSV.FORMAT (e.g., "dd-mm-yyyy").
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            
            # Print the filtered DataFrame as a string, showing the transaction data.
            # The 'index=False' argument means that the row numbers won't be printed.
            # The 'formatters' argument makes sure that the dates are shown in the specified format.
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))

            # Calculate and print the total amount of income and expense for each amount based on the category
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()

            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")

        return filtered_df

# This function gathers data from the user and adds it to the CSV file.
def add():
    # Make sure the CSV file is initialized (created if it doesn't exist).
    CSV.initialize_csv()
    
    # Get the date of the transaction from the user.
    date = get_date(
                    "Enter the date of the transaction (dd-mm-yyyy) or press enter for today's date: ", 
                    allow_default=True)
    
    # Get the amount of the transaction from the user.
    amount = get_amount()
    
    # Get the category of the transaction from the user (e.g., "Groceries").
    category = get_category()
    
    # Get a description of the transaction from the user (e.g., "Monthly shopping.").
    description = get_description()
    
    # Add the new entry to the CSV file using the data gathered from the user.
    CSV.add_entry(date, amount, category, description)

    # Ask the user if they want to add another transaction.
    add_another_transaction = input('Would you like to add another transaction (y/n)?: ' )

    # Convert the user's input to lowercase to handle both "y" and "Y".
    if add_another_transaction.lower() == "y":
        # Call the add function again to restart the process of adding a new transaction.
        add()
    else:
        # If the user doesn't want to add another transaction, print a thank you message.
        print("Thank you for using our finance tracker!")

# Call the add function to start the process of adding a new transaction.
add()