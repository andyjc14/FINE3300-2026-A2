import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the data and skip the first 8 rows 
df = pd.read_csv("STATIC_INFLATIONCALC.csv", skiprows=8)
df.columns = ["date", "cpi"]
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")

# This is to set up a valid range for the user input
first_date = df.index.min()
last_date = df.index.max()

#Part 1: Plot the graph

# Calculates annual percentage change based on twelve months previously
df["annual_change"] = df["cpi"].pct_change(periods=12) * 100

# Plots CPI and base level dotted line
fig, ax1 = plt.subplots() 
ax1.plot(df.index, df["cpi"], color="blue", label="CPI")
ax1.axhline(y=100, color="black", linestyle=":", label="Base level CPI = 100")

# Graph labels and positioning
ax1.set_xlabel("Year")
ax1.set_ylabel("CPI") 
ax1.set_title("CPI Time Series, 1914-2026")
ax1.legend(loc="upper center") 

# Plots annual percentage change on a secondary y-axis
ax2 = ax1.twinx()
ax2.plot(df.index, df["annual_change"], color="red", label="Annual % Change")
ax2.set_ylabel("Annual percentage change (%)")
ax2.legend(loc="lower right") 

plt.savefig("cpigraph.png")
plt.show()

# Part 2: Making the calculator from user input

# Loops until the input is valid
def get_price():
    while True:
        try:
            price = float(input("Enter a starting dollar amount: "))
        except ValueError:                        # not a number
            print("Please enter a number.")
            continue
        if price <= 0:                            # zero or negative
            print("The amount must be greater than zero.")
            continue
        return price


def get_date(prompt):
    while True:
        try:
            date = pd.to_datetime(input(prompt).strip(), format="%m/%Y")
        except ValueError:                        # wrong format, month 13, letters
            print("Please use the format MM/YYYY.")
            continue
        if date < first_date or date > last_date: # outside the data set
            print(f"Date must be between {first_date.month:02d}/{first_date.year} "
                  f"and {last_date.month:02d}/{last_date.year}.")
            continue
        return date


# Get inputs
price1 = get_price()
date1 = get_date("Enter the first date (MM/YYYY): ")
date2 = get_date("Enter the second date (MM/YYYY): ")
while date2 == date1:                             # The same date would crash
    print("The two dates must be different.")
    date2 = get_date("Enter the second date (MM/YYYY): ")

# Look up CPI in the data frame
cpi1 = df.loc[date1, "cpi"]
cpi2 = df.loc[date2, "cpi"]

# 4 major calculations (assume a annual inflation rate)
price2 = np.round(price1 * (cpi2 / cpi1), 2) # Numpy rounding
percent_change = ((cpi2 - cpi1) / cpi1) * 100
years = ((date2.year - date1.year) * 12 + (date2.month - date1.month)) / 12
avg_inf_rate = ((cpi2 / cpi1) ** (1 / years) - 1) * 100

# Output all information
print(f"- ${price1:,.2f} CAD in {date1.month:02d}/{date1.year} is worth ${price2:,.2f} CAD in {date2.month:02d}/{date2.year}")
print(f"- Percent Change: {percent_change:,.2f}%")
print(f"- Number of years: {years:.2f}")
print(f"- Average annual rate of inflation (decline in TVM) was {avg_inf_rate:.2f}%")
print(f"- CPI for first date: {cpi1:.2f} ({date1.month:02d}/{date1.year})")
print(f"- CPI for second date: {cpi2:.2f} ({date2.month:02d}/{date2.year})")