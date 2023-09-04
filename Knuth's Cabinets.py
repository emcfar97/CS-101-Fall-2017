##############################################################################
##
## CS 101
## Program #1
## Ethan McFarland
## Em463@mail.umkc.edu
##
## PROBLEM: The program is designed to get input about the number of cabinets
##          to be produced and give the amount of time it would take in hours
##          to complete these cabinets.
##
## ALGORITHM: 
##      1. Retrieve user input for cabinets
##      2. Multiply user input with list of multipliers 
##      3. Output resulting values
## 
## ERROR HANDLING:
##      None
##
## OTHER COMMENTS:
##      None
##
##############################################################################

#List of multipliers
cut_lbr    = (1.2, 1.5, 1.9)
sand_lbr   = (2.4, 1.8, 1.2)
finish_lbr = (3.4, 2.5, 1.5)

#User input for cabinets
upp_cab = float(input('Enter the number of upper cabinets: '))
low_cab = float(input('Enter the number of lower cabinets: '))
cor_cab = float(input('Enter the number of corner cabinets: '))

#Labor time calculations
cut_hours    = (cut_lbr[0]*upp_cab) + (cut_lbr[1]*low_cab) + (cut_lbr[2]*cor_cab)
sand_hours   = (sand_lbr[0]*upp_cab) + (sand_lbr[1]*low_cab) + (sand_lbr[2]*cor_cab)
finish_hours = (finish_lbr[0]*upp_cab) + (finish_lbr[1]*low_cab) + (finish_lbr[2]*cor_cab)

#Printing final values
print('\nTotal cutting hours', cut_hours,
      '\nTotal sanding hours', sand_hours,
      '\nTotal finishing hours', finish_hours,
      '\nTotal labor hours', cut_hours + sand_hours + finish_hours)
