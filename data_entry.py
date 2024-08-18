from datetime import datetime


"""
we create a function that will get the date and take 2 parameters
the prompt will be if we want to get the date from different places
so before we get the date, we can specify the reason we need it for.

Example:

we may want the date the amount was received/spent OR we may want a date range
for the transactions made.

"""

date_format = "%d-%m-%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}

def get_date(prompt, allow_default=False):
    # we prompt the user to give the date
    date_str = input(prompt)

    # if the user didn't provide a date, we return today's date converted to a string
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)
    
    # if the user provided a date, we try to convert it to a datetime object
    try:
        valid_date = datetime.strptime(date_str, date_format)
        # if the conversion was successful, we return the date as a string
        return valid_date.strftime(date_format)
    except ValueError:
        # if the conversion was not successful, we print an error message and ask for the date again
        # until the user gives a valid date
        print("Invalid date format. Please enter the date in dd-mm-yyyy format")
        return get_date(prompt, allow_default)

def get_amount():
    try:
        amount = float(input("Enter the amount: "))

        if amount <= 0:
            return ValueError("Amount must be a non-negative and non-zero value.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()

    if category in CATEGORIES:
        return CATEGORIES[category]


    print("Invalid category. Please enter 'I' for Income or 'E' for Expense!")

def get_description():
    return input("Enter a description (optional): ")