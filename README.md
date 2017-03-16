# NQueens Problem [100 Points]
The N-Queens problem is the problem of positioning N Queens on a NxN chess board such that no Queen can "take" another Queen by moving horizontally, vertically, or diagonally (standard chess Queen movement).

Write a program to solve the N-Queens problem the iterative improvement technique and the min-Conflict measure. This problem requires that your program find a solution to the problem of placing the largest number of queens on a chess board with the constraint that no queen can "take" any other queen. Your program should print out the reached solution.

Note 1: Since this is an iterative approach, you should run your solution 1000 times to obtain the average time required to reach a solution state for the problem. 

Note 2: Your code should be flexible to run for different values of N (the number of queens). The average execution times using 1000 runs and different values of N should be provided in a table similar to that below:

To run 10-Queens 1000 times run:
```
python NQueens.py 10 1000
```
