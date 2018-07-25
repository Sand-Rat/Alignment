import sys

def istitle(wordslist):
   return wordslist[0][-1] != "." and wordslist[1][0].isupper() and wordslist[2][0].isupper()

def removespace(wordslist):
    return [k for k in wordslist if not len(k) == 0 or not k == "\n"]

def initials(line):
    pres = False
    if len(line) > 3:
        if line[-2].isupper():
            if line[-3] == " " or line[-3] == ".":
                pres = True
    return pres

if __name__ == "__main__":
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    lines = []
    temp = []
    end_exceptions = []
    start_exceptions = []
    title_indices = []
    with open("end_exceptions.txt","r",encoding = "utf-16") as file:
        end_exceptions = file.read().split("\n")

    with open("start_exceptions.txt","r",encoding = "utf-16") as file:
        start_exceptions = file.read().split("\n")

    with open(inputFile,"r", encoding="utf-8") as file:
        data = file.readlines()

        #Exceptions that start with an uppercase
        for x in start_exceptions:
            for count in range(len(lines)-1,0,-1):
                line = lines[count]
                if (x in line.split(" ")[0]):
                    lines[count-1] = " ".join([lines[count-1],lines[count]])
                    lines[count] = ""

        lines = list(filter(None, lines))

        for _ in data:
            if ". " in _:
                elem = _.split(". ")
                for i in range(len(elem)-1):
                    elem[i] = elem[i] + "."
                for item in elem:
                    temp.append(item)
            else:
                temp.append(_)

        lines = list(filter(None, lines))

        for _ in temp:
            if "\n" in _:
                broke = _.split("\n")
                for i in broke:
                    lines.append(i)
            else:
                lines.append(_)

        lines = list(filter(None, lines))

        for i in range(1, len(lines)-1):
           microsegment = [lines[j] for j in range(i-1, i+2)]
           if istitle(microsegment):
               title_indices.append(i)

        #Merging fragments by full stop and lowercase
        for count in range(len(lines)-1,1,-1):
            elem = lines[count]
            if count not in title_indices:
                if (elem[-1] == "." or elem[-1] == ":" or elem[-1] == ";") and (elem[0].islower()):
                    lines[count-1] = " ".join([lines[count-1],lines[count]])
                    lines[count] = ""

        lines = list(filter(None, lines))

        #Exceptions with full stops/shouldn't end a sentence
        global lines_range
        lines_range = len(lines)
        for x in end_exceptions:
            count = 0
            while(count<lines_range):
                line = lines[count]
                if (x == line.split(" ")[-1]) or initials(line):
                    lines[count+1] = " ".join([lines[count],lines[count+1]])
                    lines[count] = ""
                count += 1
                lines = list(filter(None, lines))
                lines_range = len(lines)

        lines = list(filter(None, lines))

    with open(outputFile,"w",encoding = "utf-8") as file:
        for i in lines:
            if not len(i) == 0 or not i.isspace() or i == "":
                file.write(i + "\n")
