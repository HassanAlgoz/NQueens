import sys
print(sys.argv)

n = argv[1]

rows = [] # Throw queens on the board

# Pick a random assignment.
# Randomly select a variable for update. Use min-Conflict measure to set the value of the selected variable.
# Instead of building things step by step, we pick a complete assignment and fix it
# States: 4 queens in 4 columns (4^4 = 256 states)
# Operators: Move queen in column
# Goal test: No attacks
# Evaluation: c(n) = number of attacks



def heuristic(x, y):
	threats = 0
	# Top-Left to Right-Down (Diagonal)
	m = min(x, y)
	topLeft = [x-m][y-m]
	while(n - max(x+i, y+i) > 0):
		if rows[x+i][y+i] == "Q":
			threats += 1
			break;
		i += 1
