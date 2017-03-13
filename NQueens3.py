
import sys
import random
import time

# Pick a random assignment.
# Randomly select a variable for update. Use min-Conflict measure to set the value of the selected variable.
# Instead of building things step by step, we pick a complete assignment and fix it
# States: 4 queens in 4 columns (4^4 = 256 states)
# Operators: Move queen in column
# Goal test: No attacks
# Evaluation: c(n) = number of attacks

# Constants
QUEEN = "Q"
EMPTY = "#"



def conflicts(row, col):
# def aboveConflict(row, col):
	numThreats = 0
	i = row
	j = col
	while(i > 0):
		i -= 1
		if board[i][j] == QUEEN:
			numThreats += 1

# def bottomConflict(row, col):
	i = row
	j = col
	while(i < n-1):
		i += 1
		if board[i][j] == QUEEN:
			numThreats += 1

# def rightAboveConflict(row, col):
	i = row
	j = col
	while(i > 0 and j < n-1):
		i -= 1
		j += 1
		if board[i][j] == QUEEN:
			numThreats += 1

# def rightBottomConflict(row, col):
	i = row
	j = col
	while(i < n-1 and j < n-1):
		i += 1
		j += 1
		if board[i][j] == QUEEN:
			numThreats += 1

# def leftAboveConflict(row, col):
	i = row
	j = col
	while(i > 0 and j > 0):
		i -= 1
		j -= 1
		if board[i][j] == QUEEN:
			numThreats += 1

# def leftBottomConflict(row, col):
	i = row
	j = col
	while(i < n-1 and j > 0):
		i += 1
		j -= 1
		if board[i][j] == QUEEN:
			numThreats += 1
	
	return numThreats


def move(row, old, new):
	row[old] = EMPTY
	row[new] = QUEEN


def printBoard():
	for i in range(n):
		print("".join(board[i]))
	print "-"*n

def boardEvaluation():
	numThreats = 0
	for i in range(n):
		for j in range(n):
			if board[i][j] == QUEEN:
				numThreats += conflicts(i, j)
	return numThreats

def isGoal():
	for i in range(n):
		for j in range(n):
			if board[i][j] == QUEEN:
				if conflicts(i, j) != 0:
					return False
	return True


def solve(t):
	print "#%d Solving for %d Queens.." % (t+1, n)
	# Initialize Board: random assignment to all rows
	timeStart = float(time.time())
	for i in range(n):
		row = []
		r = random.randint(0, n-1)
		for j in range(n):
			row.append(EMPTY)
		row[r] = QUEEN
		board.append(row)

	timeEnd = float(time.time())
	timeDiff = float(timeEnd - timeStart)
	print "Board Initialized in %.fms" % (timeDiff*1000)
	timeStart = float(time.time())
	# -------------------------------------------------------------------
	# Game Loop (one game)
	numberOfMoves = 0
	numberOfLoops = 0
	while(True):
		numberOfLoops += 1

		# Select a radnom variable row
		r = random.randint(0, n-1)
		# Assign it the minimum conflict column
		myRow = board[r]
		initialIndex = board[r].index(QUEEN)
		minConflict = conflicts(r, initialIndex)
		minConflictIndex = initialIndex
		# Evaluate conflicts for the whole row
		cellsConflicts = []
		for j in range(n):
			conflictResult = conflicts(r, j)
			if conflictResult < minConflict:
				minConflict = conflictResult
				minConflictIndex = j
			cellsConflicts.append(conflictResult)
		
		# Inlist all indexes, where conflict == minConflict
		# This is used to break ties fast
		minIndexes = []
		for j in range(n):
			if cellsConflicts[j] == minConflict:
				minIndexes.append(j)

		# Break ties randomly
		if len(minIndexes) > 1:
			# rnd = minIndexes[random.randint(0, len(minIndexes) - 1)]
			# minConflictIndex = rnd
			minEvaluation = boardEvaluation()
			for index in minIndexes:
				move(myRow, initialIndex, index)
				evaluation = boardEvaluation()
				move(myRow, index, initialIndex)
				if evaluation < minEvaluation:
					minEvaluation = evaluation
					minConflictIndex = index

		# Move Queen: assign another column to the row
		if minConflictIndex != initialIndex:
			numberOfMoves += 1
			move(myRow, initialIndex, minConflictIndex)


		if numberOfMoves % 1000 == 0:
			printBoard()

		# Goal Test
		if minConflict == 0:
			if isGoal():
				# printBoard()
				timeEnd = float(time.time())
				timeDiff = float(timeEnd - timeStart)
				print "DONE!"
				print "     \tN\tSeconds\tLoops\tMoves\tMoves/Loops"
				print "     \t%d\t%.3f\t%d\t%d\t%.2f" % (n, timeDiff, numberOfLoops, numberOfMoves, float(numberOfMoves)/numberOfLoops)
				print "--------------------------------------------------"
				return (timeDiff, numberOfLoops, numberOfMoves, float(numberOfMoves)/numberOfLoops)


if __name__ == "__main__":
	# Get Input
	n = int(sys.argv[1])
	times = int(sys.argv[2])
	board = []
	stats = []
	for t in range(times):
		stats.append(solve(t))
		board = []

	totalTimeDiff = 0
	totalNumberOfLoops = 0
	totalNumberOfMoves = 0
	totalRatio = 0
	for timeDiff, numberOfLoops, numberOfMoves, ratio in stats:
		totalTimeDiff += timeDiff
		totalNumberOfLoops += numberOfLoops
		totalNumberOfMoves += numberOfMoves
		totalRatio += ratio

	avgTimeDiff = totalTimeDiff/times
	avgNumberOfLoops = totalNumberOfLoops/times
	avgNumberOfMoves = totalNumberOfMoves/times
	avgRatio = totalRatio/times

	print "Average of %d times" % (times)
	print "\tN\tSeconds\tLoops\tMoves\tMoves/Loops"
	print "\t%d\t%.3f\t%d\t%d\t%.2f" % (n, avgTimeDiff, avgNumberOfLoops, avgNumberOfMoves, avgRatio)