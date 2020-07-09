
readingTheTextFile = open("H:\\report&demoPaper\\class number class name QID.txt", "r")

# reading the entire ccontent
# readingTheContents=readingTheTextFile.read()
# print(readingTheContents)

# https://www.geeksforgeeks.org/python-string-split/
# reading the contents line by line
allQIDs=[]
for contentsLineByLine in readingTheTextFile:
#   print(contentsLineByLine)
  attemptingContentModification = contentsLineByLine.split('-')
  justWantQIDs=attemptingContentModification[1]
  justWantQIDs=justWantQIDs.split('\n')
  QIDs=justWantQIDs[0]
  allQIDs.append(QIDs)
print(allQIDs)

for individualQID in allQIDs:
    print(individualQID)

