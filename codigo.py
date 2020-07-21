import time
from progressBar import *
# A List of Items
items = list(range(0, 57))
l = len(items)

# Initial call to print 0% progress
if __name__ == '__main__':
    # The code goes here
    printProgressBar(0, l, prefix = 'Solving ', suffix = 'Complete', length = 50)
    for i, item in enumerate(items):
        # Do stuff...
        time.sleep(0.1)
        # Update Progress Bar
        printProgressBar(i + 1, l, prefix = 'Solving ', suffix = 'Complete', length = 50)