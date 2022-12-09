import csv

def read_text():
    with open('leaderboard.csv', newline='') as csvfile:
        infoReader = csv.reader(csvfile, delimiter='\n', quotechar='|')
        infoDict = dict()
        for row in infoReader:
            row = str(row[0]).split(",")
            # print(row[0])
            # print(row[1])
            infoDict[row[0]] = int(row[1])
        return infoDict

def write_text(itemInfo):
    with open('leaderboard.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for key, value in itemInfo.items():
            writer.writerow([key, value])
