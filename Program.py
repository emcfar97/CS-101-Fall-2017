#Ethan McFarland
#COMP-SCI 101 Prblm Slvng & Prgmg I
#Created: 10/6/2017
#Due: 10/15/2017

{
    "cmd": ["C:\\python27\\python.exe", "-u", "$file"],
    "file_regex": "^[ ]*File \"(...*?)\", line ([0-9]*)",
    "selector": "source.python"
}

import sys
import os
from termcolor import *
import colorama
import heapq
import csv
import prettytable
import texttable as tt

def ave(quiz,midterm,final):
    average=(quiz+midterm+final)/3
    return average

os.chdir("C:\\Users\\Emc11\\OneDrive - University of Missouri")

with open('grades.csv', 'r') as file:
    grades=[line.strip().split(',') for line in file]

names=[i[0] for i in grades]
quiz=[int(i[1]) for i in grades]
midterm=[int(i[2]) for i in grades]
final=[int(i[3]) for i in grades]
average=[]
for i in range(0,14):
    average.append(ave(quiz[i],midterm[i],final[i]))
    
tab = tt.Texttable()
headings = ('Name','Quiz','Midterm','Final','Average')
tab.header(headings)

names_table= ['Quiz','Midterm','Final','Average']
quiz_table=quiz
midterm_table=midterm
final_table=final
average_table=average

for row in zip(names,quiz,midterm,final,average):
    tab.add_row(row)
    average_grade=tab.draw()

while True:
    print('Welcome to UMKC software\nPlease choose one of the following options:\n1.Calculate the average grade for each student.\n2.Print the higest or lowest scores based on the user input.\n3.Dind the average score of the entire class (all students) in the final exam.\n4.To quit.')
    input('Enter your option:')

input(average_grade+'\nWould you like to continue?\n')


        
        
