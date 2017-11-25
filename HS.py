import csv
import os

def readFromCSV():
    Scores = [] # new list
    with open("HighScores.csv",newline='') as csvfile: 
            read = csv.reader(csvfile,delimiter=',',quotechar='|')
            next(read,None) # add first line to list
            for row in read: # for each line in file
                temp = [row[0],int(row[1])]
                Scores.append(temp) # add to list planets
    csvfile.close()
    return Scores


def writeToCSV(Scores):
    with open("newHighScore.csv",'w', newline='') as newFile: # open/create file for writing
        write = csv.writer(newFile)
        write.writerow(["Name","Score"])
        write.writerows(Scores) 
    newFile.close()

    #Remove and rename file
    os.remove("HighScores.csv")
    os.rename("newHighScore.csv","HighScores.csv")

def updateList(Scores,name,newScore):
    Scores.append([name,newScore])
    # Bubble sort
    n = len(Scores)
    # For every element in list
    for i in range(n):
        # For sublist not sorted
        for j in range(0,n-i-1):
            # If comparison function true
            if Scores[j][1] < Scores[j+1][1]:
                #Swap
                Scores[j],Scores[j+1] = Scores[j+1],Scores[j]
                
    Scores = Scores[:5]

'''
Scores = [] # new list
readFromCSV()
updateList(Scores,"Test",100)
writeToCSV(Scores)
'''

                
