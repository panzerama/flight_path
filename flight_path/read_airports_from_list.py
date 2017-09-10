AIRPORT_FILE = "us-primary-airports.txt"

airports = open(AIRPORT_FILE, 'r', encoding="utf-8")


for line in airports:
    for info in line.strip().split("\t"):
        print(info) #replace with creation of airports
