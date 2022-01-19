# Sven-Automated-Workflow-Tool
This is a project to highlight my skills with python, javascript, html and using services like pandas and flask to make a functioning workflow tool. Take a look http://joeybaptiste11.pythonanywhere.com/

Demo - https://www.youtube.com/watch?v=HKP30fWCXCE

## Overview
This is flask application emulates a pharamcutical manufacturing company, but this service can be utilized by any delivery company. This is a workflow manager that allows user and customers to find the best route for parcel delivery. Customers will send in order that is parsed and assigned to the warehouse that can meet that order most efficiently. This platform has three main aspects: Email listener, Best Route Algorithm, Web Application.

## WebApp

This is a simple flask based web app that uses practical elements like secure hash bases logins, google maps api, CSS, html, javascript with inspiration from bootstrap templates

### How to use

Web you first open the website you will be asked to log in. You can select the sign up button on the top left to make a new account. See arrow in image link here: 
https://imgur.com/a/WkeB6H5

Once you have created an account you will be brought to the home page where you can randomly generate new workitems by typing in the number of location you want in the text bar and review existing items. Please see arrows in image link here: https://imgur.com/a/uiV2Diq

After clicking on an item you will be brought to that items detail page. You can see that items order and destinations. To see the a map best route you can select "Analyze Route" near the top. You can change the status of the workitem on the top right corner. Please see arrows in image link here: https://imgur.com/a/LqyA2Ys

There is much more that I do not want to spoil for you. Please explore the rest of the website!
## Email Listener 
This section listens to email orders and automatically creates a workitem in the Sven platform. This is done by using the imaplib package to listen for new emails and pandas to parse the data. 

Applicable Files - Email_payload.py, Data_Collections.py

### Give it a Try (PLEASE CONTACT ME FIRST TO SET UP LISTENER)
First - Make your order using the Excel_Template.xlsx. Please use no more than 15 locations. Under the product column just add any generic drug from this website https://www.rxassist.org/pap-info/generic-drug-list-print, Your name, company, and city and full state name. 

Second - Attach your order sheet to an email to SvenWorkFlowPlatform@gmail.com with a subject line following this format "New Order: (company name)" 

Please allow 1-3 minutes for the item to appear on the Sven platform. 


## Best Route Alogrithm (TSP)

This section takes the parsed data and reformats it into an adjecency matrix. This will contain the cities coordinates gathered using the PositionStack api. Learn more here https://positionstack.com/documentation. The distance between two coordinates is calculated using the geopy package. The value used to weigh the adjecency matrix is the order profit which is calculated by subtracting the revenue (price of good * # of units ordered) by the cost of travel ((distance / average truck mpg) * average gas price) learn more here https://afdc.energy.gov/data/10310 https://gasprices.aaa.com/. Traveling Salesman is ran multiple times on the adjecency matrix to determine the best warehouse to start from, best route, and the best profit.

Warehouse locations: Chicago, IL, Dallas, TX, Los Angeles, CA, Newark, NJ. Learn more here https://blog.kencogroup.com/top-10-cities-for-a-distribution-center.


Applicable Files - routeSetup.py, shortestRoute.py, Random_Order_Generator.py

### Traveling Salesman 

TSP algorithm was write with inspiration from https://www.geeksforgeeks.org/traveling-salesman-problem-tsp-implementation/. Problem is looking for heighest profits rather than shortest distance so we replace min_path with max_path. My algorith also looks to see if a more profitable route can be made by canceling a order. This is logic for this is not very robust. It simply find the location that has the worse profits from all other location on average and removes it. If this new route is superior, the alternate route is added along side the original. On the web platform users can determine if they would like to change to the alternate route. This may lead to unhappy customers but will save the drivers a long and miserable trip. 
