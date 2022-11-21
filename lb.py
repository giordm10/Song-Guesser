import csv

def read_text():
    with open('leaderboard.csv', newline='') as csvfile:
        infoReader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        infoDict = dict()
        for row in infoReader:
            row = str(row[0]).split(",")
            # print(row[0])
            # print(row[1])
            infoDict[row[0]] = row[1]
        return infoDict

# TODO: DELETE THIS AFTER TESTING
read_text()