import re
import sys

if __name__ == "__main__":
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    dictFile = "zh-dict.txt"
    endErrors = []
    startErrors = []
    dict = {}
    with open (dictFile,"r",encoding = "utf-8") as file:
        for _ in list(filter(None, file.read().split("\n"))):
            if _[-1] in dict:
                dict[_[-1]].add(_[0])
            else:
                dict[_[-1]] = set(_[0])

    with open ("breakErrorsEnd.txt","r",encoding = "utf-16") as file:
        endErrors = file.read().split("\n")

    with open ("breakErrorsStart.txt","r",encoding = "utf-16") as file:
        startErrors = file.read().split("\n")

    with open (inputFile,"r",encoding = "utf-8") as file:
        lines = []
        for _ in list(filter(None, file.read().split("\n"))):
            lines.append(_)

        for count in range(len(lines)-1,1,-1):
            line = lines[count]
            if line[0] in dict:
                if lines[count-1][-1] in dict[line[0]]:
                    lines[count-1] = "".join([lines[count-1],line])
                    lines[count] = ""

        lines = list(filter(None, lines))

        for count in range(0,len(lines)-2):
            line = lines[count]
            if line[-1] in endErrors:
                lines[count+1] = "".join([line,lines[count+1]])
                lines[count] = ""

        lines = list(filter(None, lines))

        for count in range(len(lines)-1,1,-1):
            line = lines[count]
            if line[0] in startErrors:
                lines[count-1] = "".join([lines[count-1],line])
                lines[count] = ""

        lines = list(filter(None, lines))

        for _ in lines:
            _.replace(" ","")

    with open(outputFile,"w",encoding = "utf-8") as file:
        for _ in lines:
            file.write(_ + "\n")
