import json
import csv
import codecs
def main():
    #READ IN DATA
    diagCode = []
    csvFile = open('PivotNoSymptoms.csv', 'r')
    for line in csvFile:
        diagCode.append(line.strip()) #get rid of \n at end of each line
    #format header, 
    header= diagCode[0].split(',')
    for x in range(0, len(header)):
        header[x] = '"' + header[x] + '"'
    header = ','.join(header[2: ]) #keeps only the categories
    diagCode = diagCode[1: ] #get rid of header
    #READ IN DATA OF NAMES
    namesArr = []
    with codecs.open('names-codes.csv','r',encoding='ascii', errors ='ignore') as csvNamesFile:
        namesArr = csvNamesFile.read().split('\r\n')
    temp = []
    namesArrFormatted = []
    for x in range(1,len(namesArr)):
        temp = namesArr[x].split(',')
        codesTemp = temp[0]
        namesTemp = ','.join(temp[1: ])
        combinedTemp = [codesTemp, namesTemp]
        namesArrFormatted.append(combinedTemp) #namesArrFormatted now contains all code-name combos
    namesList = []        
    for x in range(0, len(diagCode)):
        temp = diagCode[x].split(',') #nameCode is now in pos 0
        for y in range(0, len(namesArrFormatted)):
            lookingAt = namesArrFormatted[y]
            if(temp[0] == lookingAt[0]):
                namesList.append(lookingAt[1])
                break
    #FORMAT TO JSON
    jsonFile = open('codes.json', 'w')
    #Header
    jsonFile.write('{"header" : [' + header)
    jsonFile.write('],')
    jsonFile.write("\n")
    #Diagnoses
    dataLinked = []
    for x in range(0, len(diagCode)-1) :
        temp = diagCode[x].split(',')
        print(temp[1])
        data = '''
            {"fullName" : "''' + namesList[x].encode('UTF-8') + '''",
            "nameCode" : "''' + temp[0].encode('UTF-8') + '''",
            "code" : [''' + ','.join(temp[2: ]).encode('UTF-8') + '],' + '''
            "chapter" : ''' + temp[1].encode('UTF-8') + '}'
        
        dataLinked.append(data)
    jsonFile.write('"diagnoses" : [')
    jsonFile.write(','.join(dataLinked))
    jsonFile.write(']}')
    
main()
