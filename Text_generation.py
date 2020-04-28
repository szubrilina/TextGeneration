#----------------------------------------------------------------------------------------
#Aim of this part is Calculating of probabilities 

def format(str): #make from pthrase , with , punctuation -> pthrase, with, punctuation
   
    list = str.split()
    
    ans = ""

    for elem in list:
        if (string.punctuation).find(elem) == -1 and len(ans) > 0:
            ans += " "
        ans += elem

    ans = ans.rstrip()

    return ans


def calculate_n_tokens(current_depth): # n = depth
    
    index = []
    for i in range(current_depth):
        index.append(0)

    while True:
        #count substr (n_token) in initial text
        n_token = ""
    
        for elem in index:
            n_token += list_of_all_tokens[elem] + ' '

        n_token = format(n_token)
        frequency[n_token] = initial_text.count(n_token) #here is the mainest part: counting

        #next permutation:
        is_the_last_permutaion = 1

        for i in range(len(index) - 1, -1, -1):
            if index[i] < len(list_of_all_tokens) - 1:
                index[i] += 1
                is_the_last_permutaion = 0
                break
            else:
                index[i] = 0

        if is_the_last_permutaion:
            break


#--------------------------------------------------------------------------------------------

import string

#Inputs
depth = 3 #(!!!) It schould be written from INPUT (!!!)

set_of_all_tokens = set()
initial_text = ""


frequency = dict() #dict [n-token] = number of appearence

#Catch all tokens
while True:
    try: 
        s = input()

        if len(s) == 0:
            raise 

        initial_text += s

        s = s.split()

        for token in s:
            if (string.punctuation).find(token[-1]) != -1:
                set_of_all_tokens.add(token[-1])

            token = token.strip(string.punctuation)
            set_of_all_tokens.add(token)
    except:
        break
        pass

#Calculate probabilities of n-token (n = depth)

list_of_all_tokens = []

for i in set_of_all_tokens:
    list_of_all_tokens.append(i)

for n in range(depth, 0, -1):
    calculate_n_tokens(n)

print(frequency)



