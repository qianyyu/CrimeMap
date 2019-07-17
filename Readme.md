# Assignment 4: 
## Overview:
This program provide a simply command line interface. The interface can guide user to execute a series of SQL queries.
The main logic inside the interface is straightforward. Once an option is selected, we execute the corresponding function 
to solve it. The program can finish the following tasks:
- Given a range of years and crime type, show (in a bar plot) the month-wise total count of the given crime type. 
- Given an integer N, show (in a map) the N-most populous and N-least populous neighborhoods with their population count. 
- Given a range of years, a crime type and an integer N, show (in a map) the Top-N neighborhoods and their crime count where the given crime type occurred most within the given range. 
- Given a range of years and an integer N, show (in a map) the Top-N neighborhoods with the highest crimes to population ratio within the provided range. Also, show the most frequent crime type in each of these neighborhoods. 


## User Guides:
Enter the following commands in any command line tool.
python3 a4.py

a. enter your choice from 3 options 
- `1` <==> represent 'question1'
- `2` <==> represent 'question2'
- `3` <==> represent 'question3'
				       
b. Enter your choice base on the prompt				     

c. Get the output

d  Enter `e` to exit 

### Class Interface:

#### Function:

- main_interface(self): <br />

  The function `main_interface` is called by default, which means that the main interface will be displayed 
immediately if the program is executed.(or another task is finished) The main interface can provide 5 options for user.
are for tasks and another one is for exiting the program. Once the user enter a valid number, we will execute the corresponding
function.
-----------------------

### Class Database(path):

### Functions
-  `def question1(self)`:
	- Finish Task 1

-  `def question2(self)`:
	- Finish Task 2

-  `def question3(self)`: 
	- Finish Task 3




## Test Strategy:
Description: We divide the test into two parts. The first part is whether the test program can complete the basic tasks. In the second part we enter any characters to ensure that the program does not crash.

### First part:Make sure the program can correctly finish those tasks
- pre-step: We import a sample database called `new.db`
- Step 1: We then opened it with both the program and DB browser. For example, we first enter information according to the prompt of the topic on the e-class. Then run our program and get the results. 
- Step 2: Next, according to the database information in the DB browser, manually filter the results we want and compare them with the results given by the program to check whether they are consistent. Once the results are different, we will discuss and solve it.
 
### 2nd part: Make sure the program can be executed without any bug.
- General Idea: We uses some unsatisfactory input to test the usability of this program to make sure it doesn't crash. 
- Case 1: If the program ask us to enter an  integer number, we will try to enter some character. Program will catch the errors and throw an error message.
- Case 2: If the program ask us to pick an options from the following list, we will enter an invalid number.Program will catch the errors and throw an error message.
- Case 3: If the user want to find a specific info but enter a invalid name. The program can tell the user the valid name list. 


