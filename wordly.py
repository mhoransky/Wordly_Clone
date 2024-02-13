def datalist():
    import os
    files = []
    with os.scandir('lib/') as entries:
        for entry in entries:
            files.append(entry.name)
    return(files)

def get_chars(word: str):
    import re
    return(re.sub('[^A-Z]+', '', word, 0, re.I))

def len_filter(puretext: list, length: int):
    len_filtered = set()
    for i in puretext:
        if len(i) == length:
            len_filtered.add(i)
    len_filtered = list(len_filtered)
    return(len_filtered)   

def get_dict(filename: str, length: int):
    with open(filename, "r", encoding="utf8") as input_file:
        content = input_file.read()
        #print(content)
        content = content.replace('\n', ' ')
        content = content.replace('-', ' ')

        content = content.replace("’s", '')
        content = content.replace("’d", '')
        content = content.replace("’ll", '')
        content = content.replace("n’t", '')
        content = content.replace("in’", '')
                
        content = content.replace("'s", '')
        content = content.replace("'d", '')
        content = content.replace("'ll", '')
        content = content.replace("n't", '')
        content = content.replace("in'", '')

        content = content.split()
        puretext = []

        for i in content:
            purified = get_chars(i)
            puretext.append(purified.lower())

        #print(puretext)

        len_dict = {}
        for i in range(4, length + 1):
            if len(len_filter(puretext, i)) > 0:
                len_dict[i] = len_filter(puretext, i)
        return(len_dict)
    
def merge_dicts():
    dictlist = []
    files = datalist()

    for file in files:
        filename = "lib/" + file
        file_dict = get_dict(filename, 45)
        dictlist.append(file_dict)

    merged_dict = {}
    for i in dictlist:
        merged_dict |= i
    return(merged_dict)

def make_new_dict():
    import json 
    new_dict = merge_dicts()
    with open("new_dict.json", "w") as outfile:
        json.dump(new_dict, outfile)

def analyze_dict(loaded_dict: dict):
    analysis = {}
    for l in range(45):
        if str(l) in loaded_dict.keys():
            analysis[str(l)] = len(loaded_dict[str(l)])
    return(analysis)

def load_dict():
    import json
    with open("new_dict.json") as json_file:
        loaded_dict = json.load(json_file)
        #print(loaded_dict)
        #print(analyze_dict(loaded_dict))
        return(loaded_dict)

def pick_word(num: int, all_words: dict):
    import random
    word = random.choice(all_words[str(num)])
    #print(word)
    return(word)

def select_length(all_words):
    valid = False
    while valid == False:
        print("Please specify word lenght:")
        num = input()
        if str(num) in all_words.keys():
            valid = True
            word = pick_word(num, all_words)
            #print(word)
            return(word)
        else:
            print("Your input is not valid.")

def game():
    dictionary = load_dict()
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    attempts = 5
    word = select_length(dictionary)
    num = str(len(word))
    relevant = dictionary[num]
    cipher = [*"_"*len(word)]
    superscript = [*" "*len(word)]
    notes = "".join(superscript)
    report = "".join(cipher)   
    
    print("I have a word for you! You have 5 attempts at finding it.")
    print("Try typing a lowercase word, using standard English alphabet.")
    
    while attempts > 0:
        valid = True
        user_word = input()
        if user_word in relevant:
            user_word = [*user_word]
            for i in range(len(word)):
                if user_word[i] in alphabet:
                    if user_word[i] == word[i]:
                        cipher[i] = user_word[i]
                    else:
                        if user_word[i] in word:
                            superscript[i] = user_word[i]
                else:
                    valid = False
        else:
            valid = False
        if valid == True:
            notes = "".join(superscript)
            report = "".join(cipher)
            print(notes)
            print(report)
            if report == word:
                print("Well done!")
                return()
            attempts = attempts - 1                      
            print("You have ", attempts, " attempts left.")
        if valid == False:
            print("Invalid input, try again.")
        superscript = [*" "*len(word)]

    print("Seems like you have run out of attempts.")
    print("The word you failed to find was", word)
    return()


game()
