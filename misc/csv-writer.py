import csv

with open("tsp.csv","w",newline='') as ofile:
    writer = csv.writer(ofile, delimiter = ',')
    s1 = "{},{},{},{},{},{}".format("GreedyTime","GreedyLen","GeneticTime","GeneticLen","GeneticPlusTime","GeneticPlusLen")
    s2 = "{},{},{},{},{},{}".format(1,2,3,3,2,1)

    s1 = s1.split(",")
    s2 = s2.split(",")

    writer.writerow(s1)
    writer.writerow(s2)

"""RESULT = ['apple','cherry','orange','pineapple','strawberry']
resultFile = open("output.csv",'wb')
wr = csv.writer(resultFile, dialect='excel')
wr.writerow(RESULT)

resultFile.close()"""
"""
with open('eggs.csv', 'w', newline='') as csvfile:
    s2 = "{},{},{},{},{},{}".format(1,2,3,3,2,1)
    s2 = s2.split(",")
    spamwriter = csv.writer(csvfile, delimiter=',')
    spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
    spamwriter.writerow(s2)"""