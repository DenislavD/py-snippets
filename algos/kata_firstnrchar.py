# 5 kyu First non-repeating character
from collections import Counter

s = 'Go hang a salami, I\'m a lasagna hog!'
print(Counter(s)) 
def first_non_repeating_letter(s):
    my_list = list(Counter(s).elements())
    i = 0
    while i < len(my_list):
        if my_list[i] != my_list[i-1] and my_list[i] != my_list[i+1]: return my_list[i]
        i += 1
    return 'x'
print(first_non_repeating_letter(s))

def first_non_repeating_letter_final(s):
    # return [item[0] for item in cc if item[1] == 1] # works
    # return [k if v == 1 else '' for k, v in cc ] # if condition append X to string, else needs Y
    items = [k for (k, v) in Counter(s.lower()).items() if v == 1] # append to list only IF condition
    return s[s.lower().find(items[0])] if items else 'x'
print(first_non_repeating_letter_final(s))

# Codewars solution, better
def first_non_repeating_letter_TOP(string):
    res = [i for i in string if string.lower().count(i.lower()) == 1]
    return  res[0] if len(res) > 0 else ""
print(first_non_repeating_letter_TOP(s))

def first_non_repeating_letter_2(s):
    l=[i for i in s if s.lower().count(i.lower())<2];return l and l[0]or'' # smart return!
print(first_non_repeating_letter_2(s))

print(True and 'xxx' or 2) # prints xxx
