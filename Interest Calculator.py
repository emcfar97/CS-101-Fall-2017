#Ethan McFarland
#COMP-SCI 101 Prblm Slvng & Prgmg I
#Created: 9/20/2017
#Due: 9/30/2017

import time

def interest_rate_func(x):
    if x<=500:
        interest_rate=.05
        return interest_rate
    elif x>=500 and x<=700:
        interest_rate=.02
        return interest_rate
    elif x<=700:
        interest_rate=.01
        return interest_rate

def calMonthlyPayment(x):
    A=((house_price-down_payment)*(1+(interest_rate_func(credit_score)))**year)/(12*year)
    monthly_payment=A
    return monthly_payment

def calTotalInterest(x):
    total_interest=(monthly_payment*year*12)-(house_price-down_payment)
    return total_interest

#Useful variables 
proceed=["yes", "y", "Yes", "Y", "yEs", "yeS", "YES"]
not_proceed=["no", "n", "No", "N", "nO"]
house_price=0
down_payment=0
credit_score=0
year=0
x=0

print('Welcome to the interest calculator program.')

time.sleep(1)

while True:
    
    #Asks user for house price
    while x==0:
        house_price=input('\nEnter the price of your dream house: ')
        if str.isdigit(house_price)==True:
            house_price=int(house_price)
            if house_price>=0:
                x=1
            else:
                print('\nHouse price must be a positive number only. Please try again.')
                time.sleep(1)
                continue
        else:
            print("\nSorry, that's not a number. Please try again.")
            time.sleep(1)
            continue

    #Asks user for down payment
    while x==1:           
        time.sleep(1)
        yes_no=input('\nAre you making any down payments? Please enter only "yes" or "no" \n')
        if yes_no in proceed:
            down_payment=input('\nPlease enter only a number for the down payment: ')
            if str.isdigit(down_payment)==True:
                down_payment=int(down_payment)
                if down_payment<=house_price or down_payment>=0:
                    x=2
                elif down_payment>=house_price or down_payment<=0:
                    print('Down payment must be less than the house price and greater than zero. Please try again.')
                    continue
            else:
                print("Sorry, that's not a number. Please try again.")
                continue
        elif yes_no in not_proceed:   
            x=2
        else:
            print('Please only enter "yes" or "no"')
            continue

    #Asks user for credit score
    while x==2:
        time.sleep(1)
        credit_score=input('\nPlease enter your credit score: ')
        if str.isdigit(credit_score)==True:
            credit_score=int(credit_score)
            if credit_score>=0:
                x=3    
            else:
                print('Credit score must be a positive number only. Please try again.')
                continue
        else:
            print("Sorry, that's not a number. Please try again.")
            continue

    #Displays result of user input
    while x==3:
        time.sleep(1)
        print('\nBased on your credit score, your interest rate is:\n')
        for year in range(10,26):
            monthly_payment=calMonthlyPayment(0)
            interest_rate=interest_rate_func(credit_score)
            total_interest=calTotalInterest(0)
            print('Pay in', year, 'years. Monthly payment is', round(monthly_payment,2), 'Total interest is', round(total_interest,2))
            time.sleep(1)
        x=4
            
    #Asks user if they would like to use program again
    while x==4:       
        again=input('\nWould you like to use the application again?\n')
        if again in proceed:
            x=0
        elif again in not_proceed:
            print('Thanks for using Interest Calculator application!')
            break
        else:
            print('Please only enter "yes" or "no"')
            continue
