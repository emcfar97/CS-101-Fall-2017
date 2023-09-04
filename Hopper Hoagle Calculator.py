#Ethan McFarland
#COMP-SCI 101 Problem Solving and Programming I
#Created: 8/30/2017
#Due: 9/9/2017

while True:
    print('This is the Hopper Hoagle Calculator. The menu consists of:')
    print('Italian Small')
    print('Italian Large')
    print('Veges Small')
    print('Veges Large')
    print('T Bird Small')
    print('T Bird Large')
    print('Please enter the items sold and the amount below.')

    x = input('Enter a type of food: \n')

    amount_sold=int(input('How many were used:'))


    if x=="Italian Small":
        bread=.5*amount_sold
        salami=.3*amount_sold
        veges=.2*amount_sold
        cheese=4*amount_sold
        print("You have used", bread, "loaves of bread,", salami, "lbs of salami,", veges, "lbs of veges, and", cheese, "slices of cheese. Thanks for using Hopper Hoagle Calculator.")

    elif x=="Italian Large":
        bread=1*amount_sold
        salami=.5*amount_sold
        veges=.5*amount_sold
        cheese=8*amount_sold
        print("You have used", bread, "loaves of bread,", salami, "lbs of salami,", veges, "lbs of veges, and", cheese, "slices of cheese. Thanks for using Hopper Hoagle Calculator.")

    elif x=="Vegetarian Small":
        bread=.5*amount_sold
        veges=.5*amount_sold
        cheese=5*amount_sold
        print("You have used", bread, "loaves of bread,", veges, "lbs of veges, and", cheese, "slices of cheese. Thanks for using Hopper Hoagle Calculator.")

    elif x=="Vegetarian Large":
        bread=1*amount_sold
        veges=1.2*amount_sold
        cheese=11*amount_sold
        print("You have used", bread, "loaves of bread,", veges, "lbs of veges, and", cheese, "slices of cheese. Thanks for using Hopper Hoagle Calculator.")

    elif x=="T Bird Small":
        bread=.5*amount_sold
        turkey=.4*amount_sold
        cheese=3*amount_sold
        print("You have used", bread, "loaves of bread,", turkey, "lbs of turkey, and", cheese, "slices of cheese. Thanks for using Hopper Hoagle Calculator.")

    elif x=="T Bird Large":
        bread=1*amount_sold
        turkey=.9*amount_sold
        cheese=8*amount_sold
        print("You have used", bread, "loaves of bread,", turkey, "lbs of turkey, and", cheese, "slices of cheese. Thanks for using Hopper Hoagle Calculator.")
