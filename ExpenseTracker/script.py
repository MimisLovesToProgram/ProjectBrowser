import os
import re
import datetime
from operator import itemgetter

# Get the user's desired action.
action = input("""Would you like to: 1) Add a new expense,
2) Search for an expense using its info,
or 3) check/analyze current expense info and get budget recommendations?  """)

# Key: Item/Service, Value: Category
AutomatedAnalysisItemCategories = {}
# Key: Category, Value: Importance ("important" or "normal")
category_importance = {}
# Index 0: The percentage of the user's income to be allocated with "important" expenses, Index 1: Like Index 0, but for "normal" expenses, Index 2: Like Index 0, but for "savings".
importance_percentages = []
# Key: Category, Value: That category's set budget
set_category_budgets = {}

list_AutomatedAnalysisLines = []
def AutomatedAnalysisLines():
    with open(os.path.join(os.getcwd(), "ExpenseTracker", "AutomatedAnalysisData.txt")) as f:
        for line in f.readlines():
            yield line

list_lines = []
def lines():
    with open(os.path.join(os.getcwd(), "ExpenseTracker", "result.txt")) as f:
        for line in f.readlines():
            yield line

# Looping through all lines in AutomatedAnalysisData.txt to fill the above dictionaries up.
for line in AutomatedAnalysisLines():
    if not line == "":
        list_AutomatedAnalysisLines.append(line)
        # As each type of info in AutomatedAnalysisData.txt is separated by different characters, identify the one existing in this line, and add it's info to that its dictionary.
        if ":" in line:
            AutomatedAnalysisItemCategories[line[:line.index(':')]] = line[line.index(':') + 1:].rstrip()
        elif "," in line:
            category_importance[line[:line.index(',')]] = line[line.index(',') + 1:].rstrip()
        # The next 3 line checks are always consecutive and at the following order, that's why we know what element of importance_percentages is without it being a dict.
        elif "important=" in line:
            importance_percentages.append(int(line[line.index('=') + 1:].rstrip()))
        elif "normal=" in line:
            importance_percentages.append(int(line[line.index('=') + 1:].rstrip()))
        elif "savings=" in line:
            importance_percentages.append(int(line[line.index('=') + 1:].rstrip()))
        elif ">" in line:
            set_category_budgets[line[:line.index('>')]] = int(line[line.index('>') + 1:].rstrip())

# Index 0: Number of total "important" categories, Index 1: Number of total "normal" categories
importance_nums = [0, 0]
for line in lines():
    list_lines.append(line)
    # Filling "lines" up with result.txt's lines, and adding the number of important and normal expenses in importance_nums
    category = line[:line.index(',')]
    if category_importance[category] == "important":
        importance_nums[0] += 1
    else:
        importance_nums[1] += 1

# Checking the user's desired action.
if action == "1":
    with open(os.path.join(os.getcwd(), "ExpenseTracker", "result.txt"), "a") as f:
        # Setting the variable "category" up for later use, getting info about the expense being logged, and validating it.
        category = ""
        item = input("Enter the Item/Service bought (e.g. Starbucks): ")
        while item == "":
            item = input("Please enter an Item/Service's name: ")

        amount = input("Enter the amount you spent on it in $ (e.g. 34): ")
        while not re.match(r"[0-9][0-9\.]*", amount):
            amount = input("Please enter a valid amount of money spent: ")

        date = input("Enter the date of the expense (e.g. 2023-10-26): ")
        while not re.match(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", date):
            date = input("Please enter a valid date, according to the example above: ")

        # If the item being loged is new, get it's category, and if not, get it's category from AutomatedAnalysisItemCategories.
        if not item in AutomatedAnalysisItemCategories:
            with open(os.path.join(os.getcwd(), "ExpenseTracker", "AutomatedAnalysisData.txt"), "a") as AutomatedAnalysisData:
                # Show the user all existing categories available to use (if any), and get the category given.
                if not AutomatedAnalysisItemCategories == {}:
                    print(f"Here are all currently used categories: {','.join(category_importance)}")
                else:
                    print(f"There are no categories currently being used.")
                category = input('Enter a category for this new item: ')
                while category == "":
                    category = input('Please enter a category for this new item: ')

                # If the category is new, get it's importance, and then, write all necessary info on AutomatedAnalysisData.txt
                if not category in category_importance:
                    importance = input("Enter the type this category belongs to in general (Is it 'important' or just 'normal'?): ").lower()
                    while not importance in ["important", "normal"]:
                        importance = input("Please enter the type this category belongs to ('important' or 'normal'): ").lower()
                    AutomatedAnalysisData.write(f"{category},{importance}\n")
                AutomatedAnalysisData.write(f"{item}:{category}\n")
        else:
            category = AutomatedAnalysisItemCategories[item]

        # Finally, log the expense at result.txt.
        f.write(f"{category}, {item}, {amount}, {date}\n")
elif action == "2":
    # Get the substring(s) to look for.
    substrings = input("Enter as much info as possible about the expense, separated by spaces (e.g. Apples Groceries ...): ").split()
    # Iterate ober all expenses, then for each expense check if it contains every substring given.
    for line in list_lines:
        for substring in substrings:
            if not substring in line:
                break
        else:
            # If no break statement is run, we can confirm that the expense is what the user is looking for. Then, breaking the loop so that the else block below does not run.
            print(f"Here is the first expense found with this info: \n{line}")
            break
    else:
        # If the break statement of the first for loop didn't run, no expense was found.
        print("No expense with such info was found.\n")
else:
    # Sum of all expenses logged.
    total = 0
    month_total = 0
    # Number of expenses made this month
    monthly_expenses = 0
    # Key: Category, Value: The number of times this category has been used.
    num_categories = {}
    # Like num_categories, but for the current month.
    month_categories = {}
    # Key: Category, Value: The category's percentage of total expenses.
    spendings_of_categories = {}
    # Key: Category, Value: The category's percentage of total money spent.
    money_of_categories = {}
    # Like the above dict, but for categories the user has spent money on this month.
    month_money_of_categories = {}
    # Like the above dict, but for the previous month's category expenses.
    prev_month_category_money = {}
    for line in list_lines:
        # Iterating over the expenses logged on the result file, and filling the above variables up with each line's info.
        category = line[:line.index(',')]
        amount = float(re.search(r"([0-9][0-9\.]*), ", line).group(1))
        total += amount
        money_of_categories[category] = money_of_categories.get(category, 0) + amount
        num_categories[category] = num_categories.get(category, 0) + 1

        # Getting the line's log day, today's date, and comparing them to fill different variables up if the log month and today's month differ or not.
        line_date = re.search(r"([0-9]+)-([0-9]+)-[0-9]+", line).groups()
        today_date = re.search(r"([0-9]+)-([0-9]+)-[0-9]+", str(datetime.datetime.today())).groups()
        if line_date == today_date:
            month_total += amount
            monthly_expenses += 1
            month_money_of_categories[category] = month_money_of_categories.get(category, 0) + amount
            month_categories[category] = month_categories.get(category, 0) + 1
        elif line_date[0] == today_date[0] and int(line_date[1]) == int(int(today_date[1]) - 1):
            prev_month_category_money[category] = prev_month_category_money.get(category, 0) + amount

    # Adding categories and their percentages as described above, and sorting the dicts with spending percentages by their percentages (values)
    spendings_of_categories = {category:round(num_categories[category] / len(list(list_lines)) * 100) for category in num_categories}
    spendings_of_categories = dict(sorted(spendings_of_categories.items(), key=itemgetter(1), reverse=True))
    money_of_categories = {category:round(money_of_categories[category] / total * 100) for category in num_categories}

    # Getting the user's financial info, and validating it.
    income = input("Enter your monthly income in $: ")
    while not re.match(r"[0-9][0-9\.]*", income):
        income = input("Please enter a valid monthly income (e.g. 2000.08) in $: ")
    income = float(income)
    debt = input("Enter your total monthly debt payments in $: ")
    while not re.match(r"[0-9][0-9\.]*", debt):
        debt = input("Please enter a monthly debt payment amount (e.g. 4000.67) in $: ")
    debt = float(debt)
    goal = input("Do you have any goals or major expenses you wish to save money for? ('yes' or 'no') ").lower()
    while not goal in ["yes", "no"]:
        goal = input("Please type 'yes' or 'no': ").lower()

    # If the user would like to save money for a goal or major expense, find a way to raise the "savings" stat by 20%
    if goal != "no":
        if importance_percentages[1] - 20 < 0:
            # If the "normal" percentage is too low to be reduced, cut it down to 0% and remove the rest from the "important" percentage
            if importance_percentages[0] + importance_percentages[1] - 20 < 30:
                # If the "important" percentage is also too low, set the normal percentage to 0, and the important one at 30, the lowest it should go.
                importance_percentages[0] = 30
                importance_percentages[1] = 0
                importance_percentages[2] = 70
                print("\nSet income distribution as follows, due to savings budget set far too high: important: 30%, normal: 0%, savings: 70%")
            else:
                importance_percentages[0] += importance_percentages[1] - 20
                importance_percentages[1] = 0
                importance_percentages[2] += 20
                print("\nRaised the 'savings' budget by 20%, to prepare for your goal/major expense.")
        else:
            # If we can, we remove 20% straight from the "normal" percentage.
            importance_percentages[1] = importance_percentages[1] - 20
            importance_percentages[2] += 20
            print("\nRaised the 'savings' budget by 20%, to prepare for your goal/major expense.")

    # If the user's DTI is above 43%, raise the "savings" budget by 30% to try to counteract this unhealthy DTI.
    if debt / income > .43:
        if importance_percentages[1] - 30 < 0:
            # If the "normal" budget is already too low to be lowered, set it to 0 and subtract what remains from the "important" budget.
            importance_percentages[0] += importance_percentages[1] - 30
            importance_percentages[1] = 0
            importance_percentages[2] += 30
        else:
            # If possible, subtract the 30% from the "normal" budget straight away.
            importance_percentages[1] = importance_percentages[1] - 30
            importance_percentages[2] += 30
        print("\nRaised the 'savings' budget by 30%, due to a quite unhealthy amount of debt.")

    # Key: Category, Value: The category's budget in $, after all calculations.
    final_category_budgets = {}
    # Key: Category, Value: The category's estimated budget, according to the "important", "normal" and "savings" percentages only.
    est_category_budgets = {}
    for category in num_categories:
        # Iterating over all categories being used, and setting their estimated budgets according to their importance percentages.
        if category_importance[category] == "important":
            # Getting the money available to spend for this category, and setting the estimated budget by evenly splitting the available money to spend.
            available = income * importance_percentages[0] / 100
            est_category_budgets[category] = round(available / importance_nums[0])
        else:
            available = income * importance_percentages[1] / 100
            # Unlike important categories, normal ones can sure have a percentage of 0%, something we need to look out for here.
            try:
                est_category_budgets[category] = round(available / importance_nums[1])
            except ZeroDivisionError:
                est_category_budgets[category] = 0

    print("\nHere are category budget recommendations, according to your previous monthly expenses (if any), budgeting rules, and your set preferences (if any):")
    for category in num_categories:
        # Iterating over all categories, and calculating their final budgets according to the estimated budget, the previous month's expenses on this category (if any), and the budget the user has set.
        if category in prev_month_category_money and category in set_category_budgets:
            final_category_budgets[category] = round((est_category_budgets[category] + prev_month_category_money[category] + set_category_budgets[category]) / 3)
        elif not category in prev_month_category_money and not category in set_category_budgets:
            final_category_budgets[category] = est_category_budgets[category]
        elif category in set_category_budgets:
            final_category_budgets[category] = round((est_category_budgets[category] + set_category_budgets[category]) / 2)
        elif category in prev_month_category_money:
            final_category_budgets[category] = round((est_category_budgets[category] + prev_month_category_money[category]) / 2)
        print(f"{category}: ${final_category_budgets[category]}")

    with open(os.path.join(os.getcwd(), "ExpenseTracker", "AutomatedAnalysisData.txt"), "w") as f:
        # Preparing for adjustments on the way income is split, or set category budgets.
        new_lines = list_AutomatedAnalysisLines
        category_budget_adjustment = input("\nWould you like to change any category's budget? ('yes' or 'no') ").lower()
        # As long as the user wants to, change category budgets.
        while category_budget_adjustment == "yes":
            # Getting the category whose budget will be changed, and validating it.
            category = input(f"""Enter the name of the category whose budget needs adjustments. Used categories:
{','.join(num_categories.keys())}\n""")
            while not category in num_categories:
                category = input(f"""Please enter the name of the category whose budget needs adjustments, form one of the following categories:
{','.join(num_categories.keys())}\n""")
            
            # Then, getting the prefered budget for this category, and validating it.
            prefered_budget = input("Enter your prefered budget for this category in $: ")
            while not re.match(r"[0-9][0-9\.]*", prefered_budget):
                prefered_budget = input("Please enter a vaild budget for this category in $ (e.g. 308.9): ")
            
            # Removing the line with the previous budget from new_lines
            for line in list_AutomatedAnalysisLines:
                if f"{category}>" in line:
                    new_lines.remove(line)
                    break
            
            # Appending the new budget with its category, and restarting the loop if the user wants to.
            new_lines.append(f"{category}>{prefered_budget}\n")
            category_budget_adjustment = input("\nWould you like to change another category's budget? ('yes' or 'no') ").lower()

        income_split_adjustment = input("\nWould you like to change the way your income is split? ('yes' or 'no') ").lower()
        if income_split_adjustment == "yes":
            important_percent = 0
            normal_percent = 0
            savings_percent = 0
            # Making sure that all new percentages add up to 100.
            while not int(important_percent) + int(normal_percent) + int(savings_percent) == 100:
                print("Note: The percentages to be given should, obviously, add up to 100.")

                # getting all percentages, and validating them.
                important_percent = input("Enter a percentage of your income to be spent on important categories (e.g. 50, >30): ")
                while not important_percent.isnumeric():
                    important_percent = input("Please enter a valid percentage (Must be an integer, 30 or above): ")
                normal_percent = input("Enter a percentage of your income to be spent on normal categories (e.g. 30): ")
                while not normal_percent.isnumeric():
                    normal_percent = input("Please enter a valid percentage (Must be an integer): ")
                savings_percent = input("Enter a percentage of your income to be saved/invested etc. (e.g. 20): ")
                while not savings_percent.isnumeric():
                    savings_percent = input("Please enter a valid percentage (Must be an integer): ")

                # Making sure that the "important" percentage is at least 30.
                if int(important_percent) < 30:
                    important_percent = "30"

            # Removing the previous percentages from new_lines.
            for line in list_AutomatedAnalysisLines:
                if "important=" in line or "normal=" in line or "savings=" in line:
                    new_lines.remove(line)

            # Then, appending the new ones.
            new_lines.append(f"important={important_percent}\n")
            new_lines.append(f"normal={normal_percent}\n")
            new_lines.append(f"savings={savings_percent}\n")

        # Finally, write new_lines to AutomatedAnalysisData.txt
        f.writelines(new_lines)
        print("All adjustments made will be used on the next summary/review.")

    # Printing the general review/summary using the dicts spendings_of_categories and money_of_categories.
    print("\nHere are all the categories you have spent money on, their % of all expenses made, and their % of all money spent:\n")
    for category, spendings_percent in spendings_of_categories.items():
        print(f"{category}: {spendings_percent}% of expenses, {money_of_categories[category]}% of all money spent.")
    print(f"\nTotal money spent: ${total}\n\n")

    # Printing the monthly review/summary using month_money_of_categories.
    print("Here is your monthly summary, in the format of the general report above:\n")
    for category in month_categories:
        print(f"{category}: {round(month_categories[category] / monthly_expenses * 100)}% of monthly expenses, {round(month_money_of_categories[category] / month_total * 100)}% of all money spent during this month. ${month_money_of_categories[category]} spent, compared to a budget of ${final_category_budgets.get(category, '-')}")
    print(f"\nTotal money spent this month: ${month_total}\n")
    print("""NOTE: All percentages that would be decimal have been rounded, 
And the shown budgets are the average of the estimated budget, the set one, and your previous month's expenses on that category.""")
