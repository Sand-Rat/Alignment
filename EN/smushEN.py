def istitle(wordslist):
   return wordslist[0][-1] != "." and wordslist[1][0].isupper() and wordslist[2][0].isupper()

def initials(line):
    pres = False
    if len(line) > 3:
        if line[-2].isupper():
            if line[-3] == " " or line[-3] == ".":
                pres = True
    return pres

def hasNext(iterator):
    if next(iterator,None) == None:
        return False
    else:
        return True

if __name__ == "__main__":
    inputFile = "file.txt"
    lines = []
    temp = []
    end_exceptions = []
    start_exceptions = []
    title_indices = []
    with open("end_exceptions.txt","r",encoding = "utf-16") as file:
        end_exceptions = file.read().split("\n")

    with open("start_exceptions.txt","r",encoding = "utf-16") as file:
        start_exceptions = file.read().split("\n")

    with open(inputFile,"r", encoding="utf-16") as file:
        data = file.readlines()

        lines = list(filter(None, lines))

        #Splitting by full stops
        for _ in data:
            if ". " in _:
                line = _.split(". ")
                for i in range(len(line)-1):
                    line[i] = line[i] + "."
                for item in line:
                    temp.append(item)
            else:
                temp.append(_)

        lines = list(filter(None, lines))

        #Splitting by line breaks
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

        #Merging fragments by full stop + lowercase, and exceptions with an uppercase
        for count in range(len(lines)-1,1,-1):
            line = lines[count]
            #if count not in title_indices:
            if (line[-1] == "." or line[-1] == ":" or line[-1] == ";") and ((line[0].islower()) or (line.split(" ")[0] in start_exceptions)) and (lines[count-1][-1] != "."):
                lines[count-1] = " ".join([lines[count-1],lines[count]])
                lines[count] = ""

        lines = list(filter(None, lines))

        #Exceptions with full stops/shouldn't end a sentence
        #for x in end_exceptions:
        count = 0
        length = len(lines)
        while (count<length-1):
            line = lines[count]
            if (line.split(" ")[-1] in end_exceptions) or initials(line):
                lines[count+1] = " ".join([lines[count],lines[count+1]])
                lines[count] = ""
            count += 1
            lines = list(filter(None, lines))
            length = len(lines)

        lines = list(filter(None, lines))

    with open("alignmentSorted.txt","w",encoding = "utf-8") as file:
        for i in lines:
            if not len(i) == 0 or not i.isspace() or i == "":
                file.write(i + "\n")
