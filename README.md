# Turtle Tallies

[Live Site](https://turtle-tallies.herokuapp.com/)



1. [Introduction](#1-introduction)
2. [Technologies used](#2-technologies-used)
3. [Testing](#3-testing)
4. [Bugs](#4-bugs)
5. [Credits](#5-credits)
6. [Deployment](#6-deployment)
7. [Acknowledgements](#7-acknowledgements)

## Introduction

***

Turtle Tallies is a program designed to automate data analysis for a turtle nest abundance study.  
It allows users to input collected data and calculations are carried out on the nest abundance of green and loggerhead turtles.

### Project Background



### Data required

Each worker / volunteer will be given a standardised form to record data. This data is then entered into the program to be stored in a google sheet document and analyses performed. 



### Calculations

This is a made up project to investigate the nesting distribution of sea turtles in the mediterannean, as this is a knowledge gap identified in a 2018 review. Two turtle species nest here, the green sea turtle and the loggerhead turtle.
The premise is over a 4 week period during the nesting season, two beaches are patrolled at night to record the turtle data. If a turtle attempts to lay a nest but leaves, their id and this attempt is recorded to investigate in the future if the beaches surroundings could be impacting the nesting behaviour. If a nest is laid, it is marked and protected. 
If a turtle does not have an id tag, one is put on while the turtle is laying her nest and oblivious to her surroundings.
Temperature data loggers record the temperature of the nest over the period it is in it. This will be used to estimate the sex of the hatchlings (cold temperatures produce males, warm temperatures females and inbetween can result in a mixed gendered nest). The data returned from these are not relevant to this project, but it's important to know for the other study to know which nests have them and its important for this study to know how many are in stock.

The focus of this study is to calculate the abundance of nests on two beaches in North Cyprus, and how many each species is laying. This project is in the early stages of a long term study investigating the nesting abundance and distribution of these two turtle species. 

## Technologies Used

***

## Testing 

***

## Bugs

- For user_verify_input, 'y' isn't registered as 'Y' and it restarts the function
    - Fix: Add an or statement. Change this later to lower method if possible
-Data entered into worksheets wasn't changed to uppercase
    - Add the upper() method before appending
- When data was added to species specific worksheets, the species data was also being transferred when there wasn't a column for it 
    - Add remove method to function before appending
- Type_print works great in terminal, but not deployed version
    - NOT FIXED
- Input validation can't have spaces
    - NOT FIXED
- Colour doesn't work properly for inputs
    - NOT FIXED

***

## Credits

***

## Deployment

***

## Acknowledgements

***