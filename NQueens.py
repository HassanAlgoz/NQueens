import sys
import random
print(sys.argv)



# Pick a random assignment.
# Randomly select a variable for update. Use min-Conflict measure to set the value of the selected variable.
# Instead of building things step by step, we pick a complete assignment and fix it
# States: 4 queens in 4 columns (4^4 = 256 states)
# Operators: Move queen in column
# Goal test: No attacks
# Evaluation: c(n) = number of attacks


# conflicts
def conflicts(row, col):
	numThreats = 0
	# Column
	for i in range(n):
		if board[i][col] == QUEEN and i != row:
			numThreats += 1

	# Top-Left to Bottom-Right (Diagonal)
	m = min(row, col)
	i = row-m
	j = col-m
	while(i < n and j < n):
		if board[i][j] == QUEEN and i != row and j != col:
			numThreats += 1
		i += 1
		j += 1

	# Top-Right to Bottom-Left (Diagonal)
	m = min(row, n-col-1)
	i = row-m
	j = col+m
	while(i < n and j >= 0):
		if board[i][j] == QUEEN and i != row and j != col:
			numThreats += 1
		i += 1
		j -= 1

	return numThreats


def updateConflicts(row, col):
	# Column
	for i in range(n):
		if board[i][col] == QUEEN and i != row:
			rowConflicts[i] = conflicts(i, col)

	# Top-Left to Bottom-Right (Diagonal)
	m = min(row, col)
	i = row-m
	j = col-m
	while(i < n and j < n):
		if board[i][j] == QUEEN and i != row and j != col:
			rowConflicts[i] = conflicts(i, j)
		i += 1
		j += 1

	# Top-Right to Bottom-Left (Diagonal)
	m = min(row, n-col-1)
	i = row-m
	j = col+m
	while(i < n and j >= 0):
		if board[i][j] == QUEEN and i != row and j != col:
			rowConflicts[i] = conflicts(i, j)
		i += 1
		j -= 1


def move(row, old, new):
	row[old] = EMPTY
	row[new] = QUEEN




if __name__ == "__main__":
	# Constants
	QUEEN = "Q"
	EMPTY = "#"

	# Get Input
	n = int(sys.argv[1])

	# Initialize Board
	board = []
	for i in range(n):
		row = []
		r = random.randint(0, n-1)
		for j in range(n):
			row.append(EMPTY)
		row[r] = QUEEN
		board.append(row)

	for i in range(n):
		print("".join(board[i]))

	
	import datetime
	timeStart = datetime.datetime.now()
	# Initialize our conflicted rows storage
	rowConflicts = []
	for i in range(n):
		col = board[i].index(QUEEN)
		rowConflicts.append(conflicts(i, col))

	# Game Loop
	counter = 0
	while(True):
		counter += 1

		if sum(rowConflicts) == 0:
			for i in range(n):
				print("".join(board[i]))	
			print("GOAL!")
			print("num of moves " + str(counter))
			print("Elapsed Time", datetime.datetime.now() - timeStart)
			break

		r = random.randint(0, n-1)
		# while(rowConflicts[r] == 0):
		# 	r = random.randint(0, n-1)

		myRow = board[r]
		minConflict = rowConflicts[r]
		initialIndex = board[r].index(QUEEN)
		minConflictIndex = initialIndex


		cellsConflicts = []

		for j in range(n):
			conflictResult = conflicts(r, j)
			if (conflictResult < minConflict):
				minConflict = conflictResult
			cellsConflicts.append(conflictResult)
		while True:
			rnd = random.randint(0,n-1)
			if cellsConflicts[rnd] == minConflict:
				minConflictIndex = rnd
				break

		# Move
		move(myRow, initialIndex, minConflictIndex)
		rowConflicts[r] = minConflict
		updateConflicts(r, initialIndex)
		updateConflicts(r, minConflictIndex)

	# 	for i in range(n):
	# 		print("".join(board[i]))
	# print(rowConflicts)

	