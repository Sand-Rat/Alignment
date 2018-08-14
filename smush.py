import sys
import re

def istitle(wordslist):
   return wordslist[0][-1] != "." and wordslist[1][0].isupper() and wordslist[2][0].isupper()

# Remove empty fields in a list
def remove_spaces(lines):
    return list(filter(lambda a: a != "", lines))

# Returns True if the text has neither English nor Chinese characters
def find_chinese_and_english(line):
    regex = "[a-zA-z\u4e00-\u9fff]"
    return re.findall(regex, line) == []

# Check if a word uses only the English alphabets
def is_english(word):
    try:
        return word.encode('ascii').isalpha()
    except:
        return False

# Build dictionary of Chinese words that should be merged back
def build_dict(file):
    _dict = {}
    for _ in load_file(file):
        if _[-2] in _dict:
            _dict[_[-2]].add(_[0])
        else:
            _dict[_[-2]] = set(_[0])
    return _dict

# Remove spaces between Chinese words
def chinese_smush(line):
    characters = [""] + list(line) + [""]
    for index in range(len(characters)):
        if characters[index].isspace() and not is_english(characters[index-1]) and not is_english(characters[index+1]):
            characters[index] = ""
    return "".join(remove_spaces(characters))

# Check common word pairing which gets broken up accidentally
def check_word_pair(dict, prev_line, curr_line):
    curr_first_char, prev_last_char = curr_line[0], prev_line[-1]
    prev_characters = list(prev_line)
    curr_characters = list(curr_line)
    return curr_first_char in dict and prev_last_char in dict[curr_first_char] \
    or curr_characters[0] == "」" or curr_characters[0] == "）" \
    or prev_characters[-1] == "「" or prev_characters[-1] == "（" \

# Check exceptions to merge back to the previous sentence based on the last words of the previous line
# Backward Pass
def backward_pass(start_exceptions, prev_line, curr_line):
    first_char, last_char = curr_line[0], curr_line[-1]
    curr_split, prev_split = curr_line.split(), prev_line.split()
    
    curr_first_word = curr_split[0]
    curr_first_word_last_char = curr_first_word[-1]
    prev_last_word = prev_split[-1]    
    prev_last_char = prev_line[-1]
    
    # Bunch of if/else return statements
    return (last_char == "." or last_char == ":" or last_char == ";") and first_char.islower() \
    or prev_last_word in start_exceptions \
    or (len(curr_split) == 1) and (curr_line.islower() or curr_first_word_last_char == ")" or curr_first_word_last_char == ".") \
    # or (len(prev_split) == 1) and (prev_last_char == ".")
    # or ")" in curr_first_word \

# Get exception files
def get_exceptions(start, end):
    print ("Getting exceptions from exception files...")
    with open(start, "r", encoding="utf-8") as file:
        start_exceptions = file.read().split("\n")
    with open(end, "r", encoding="utf-8") as file:
        end_exceptions = file.read().split("\n")
    return start_exceptions, end_exceptions

# Load file to be processed
def load_file(file):
    print ("Loading", file,"to be processed...")
    with open(file, "r", encoding="utf-8") as inp:
        return inp.readlines()

# Write output to file
def write_output(lines, file):
    print ("Writing to file...")
    #lines = [line[1:].replace("  ", " ") + "\n" if line[0].isspace() else line.replace("  ", " ") + "\n" for line in lines]
    lines = [line.replace("  ", " ") + "\n" for line in lines]
    lines = purge_noise(lines)
    with open(file, "w", encoding="utf-8") as outp:
        outp.writelines(lines)
        print ("Completed.")

# Splitting handler
def split_by(data, symbol):
    output = []
    data = list(filter(None, data))

    if symbol == "\n":
        print ("Splitting data by line break")
        for _ in data:
            output.append(_.replace("\n", ""))

    elif symbol == ". ":
        print ("Splitting data by full stop")
        for _ in data:
            if symbol in _:
                split = _.split(symbol)
                mylist = [split[i] + "." for i in range(len(split)-1)] + [split[-1]]
                
                for segment in mylist:
                    output.append(segment)

            else:
                output.append(_)
    else:
        print ("Splitting data by ", symbol)
        for _ in data:
            if symbol in _:
                split = _.split(symbol)
                mylist = [split[i] + symbol for i in range(len(split)-1)] + [split[-1]]
                for segment in mylist:
                    output.append(segment)
            else:
                output.append(_)
    
    return output

# Remove noises
def purge_noise(lines):
    noise_file = "noise.txt"
    noises = load_file(noise_file)
    output = []

    for line in lines:
        if find_chinese_and_english(line):
            print ("Purged: ", line)
            continue    
        for noise in noises:
            if line == noise or find_chinese_and_english(line.replace(noise, "")):
                print ("Purged: ", line)
                break
        else:
            output.append(line)
    return output

if __name__ == "__main__":
    input_file, output_file, language = sys.argv[1], sys.argv[2], sys.argv[3]
    se, ee = "start_exceptions.txt", "end_exceptions.txt"
    zh_dict_file = "zh_dict.txt"
    
    print ("Processing file in the following language: ", language)

    # Splitting part
    symbols = {
        "en" : {". ", ";", ":", "\n"},
        "zh" : {"。", "：", "；", "\n"}
    }
   
    start_exceptions, end_exceptions = get_exceptions(se, ee)
    data = load_file(input_file)
    lines = data

    for symbol in symbols[language]:
        lines = split_by(lines, symbol)
        lines = remove_spaces(lines)

        # print (lines)
    if language == "en":
        for index in range(len(lines)-1, 1, -1):
            if backward_pass(start_exceptions, lines[index-1], lines[index]):
                lines[index-1] = " ".join([lines[index-1], lines[index]])
                lines[index] = ""
    
    elif language == "zh":
        zh_dict = build_dict(zh_dict_file)
        
        # Remove spaces between characters
        for index in range(len(lines)):
            lines[index] = chinese_smush(lines[index])

        for index in range(len(lines)-1, 1, -1):
            if check_word_pair(zh_dict, lines[index-1], lines[index]):                
                lines[index-1] = "".join([lines[index-1], lines[index]])
                lines[index] = ""
    
    write_output(lines, output_file)