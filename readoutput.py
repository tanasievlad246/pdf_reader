import csv

# Read csv into a list of lists
with open('output.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='')
    for row in reader:
        print(', '.join(row))