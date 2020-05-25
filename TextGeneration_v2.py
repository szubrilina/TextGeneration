

import random
import string
import argparse
import sys
import json
#import dill
import collections
import re

# ---------------------------------------------------------------------------
# ---------------------CALCULATING PROBABILITIES-----------------------------
# ---------------------------------------------------------------------------


def final_format(my_string):

    if len(my_string) <= 1:
        return my_string

    # for i in range(3):
    #     for char in string.punctuation:
    #         my_string = my_string.replace(char + " " + char, char)

    punctuation = ",.!':;$%?"
    for char in punctuation:
        my_string = my_string.replace(" " + char, char);
        
    my_string = my_string.replace(" )", ")")
    my_string = my_string.replace("( ", "(")
    my_string = my_string.replace(",.", ".")
    my_string = my_string.replace(",)", ")")

    my_string = my_string.lstrip()
    my_string = my_string.lstrip((string.punctuation).replace('"', ''))
    my_string = my_string.rstrip(";:,")

    new_string = ""
    # quotes = 0
    # brackets = 0

    quotes = 0
    brackets = ""

    is_skiping_next_space = 0
    for ch in my_string:
        fl = 1

        if is_skiping_next_space == 1 and ch not in string.ascii_letters:
            continue

        if is_skiping_next_space == 1 and ch in string.ascii_letters:
            is_skiping_next_space = 0

        if ch == '"':
            if quotes > 0:
                quotes -= 1
                new_string = new_string[:-1]
            else:
                quotes += 1
                is_skiping_next_space = 1

        if ch == ')':
            if len(brackets) > 0:
                brackets = brackets[:-1]
            else:
                fl = 0

        if ch == '(':
            brackets += '('

        if fl:
            new_string += ch

    my_string = new_string

    my_string = my_string.replace(" )", ")")
    my_string = my_string.replace("( ", "(")

    my_string = my_string.replace("  ", " ")

    for ch in string.ascii_lowercase:
        my_string = my_string.replace(". " + ch, ". " + ch.upper())

    for ch in string.ascii_lowercase:
        my_string = my_string.replace("? " + ch, "? " + ch.upper())

    for ch in string.ascii_lowercase:
        my_string = my_string.replace("! " + ch, "! " + ch.upper())

    for ch in string.ascii_lowercase:
        my_string = my_string.replace(", " + ch, ", " + ch.lower())

    my_my_string = my_string[::-1]
    my_string = (my_string).replace('(', "", len(brackets))
    my_string = (my_string).replace('"', "", quotes)
    my_string = my_string[::-1]

    my_string = my_string.rstrip()
    my_string = my_string.lstrip()

    my_string = my_string[::-1]

    my_string = my_string.replace("  ", " ")

    if my_string != "" and my_string[-1] not in "!?.":
        my_string += '.'

    if len(my_string) >= 2:
        my_string = my_string[0].upper() + my_string[1:]

    return my_string


def get_string(list):
    str = ""
    for item in list:
        str = ' '.join([str, item])

    str = str.lstrip()
    return str

def is_correct(my_str):

    for char in string.punctuation:
        if (char + " " + char) in my_str:
            return 0
    quotes = 0
    brackets = ""

    is_skiping_next_space = 0
    for ch in my_str:
        fl = 1

        if is_skiping_next_space == 1 and ch not in string.ascii_letters:
            continue

        if is_skiping_next_space == 1 and ch in string.ascii_letters:
            is_skiping_next_space = 0

        if ch == '"':
            if quotes > 0:
                quotes -= 1
            else:
                quotes += 1
                is_skiping_next_space = 1

        if ch == ')':
            if len(brackets) > 0:
                brackets = brackets[:-1]
            else:
                fl = 0

        if ch == '(':
            brackets += '('

    if quotes > 0 or len(brackets) > 0:
        return 0;

    return 1;

def calculate_n_tokens(depth, tokens_tuple, probabilities):

    if depth - 1 > 0:
        current = tokens_tuple[:depth - 1]
    else:
        current = ()

    for item in tokens_tuple[depth - 1:]:
        
        key = get_string(current)
        if is_correct(key + item):
            probabilities[key][item] += 1

        current = list(current)
        current.append(item)
        currecnt = tuple(current)
        current = current[1:]

    return probabilities


def calculate_all_len_tokens(max_depth,
                             my_tuple, 
                             probabilities):

    for d in range(1, max_depth + 1, 1):
        probabilities = calculate_n_tokens(d,
                                           my_tuple,
                                           probabilities)

    return probabilities


def read_initial_text(input_file, args):

    with open(input_file, "r") as input:
        full_text = input.read()

    tokens_tuple = tuple(re.findall(args.mask, full_text))

    input.close()
    return tokens_tuple

# -------------------------------------------------------------------------
# ------------------------GENERATING TEXT----------------------------------
# -------------------------------------------------------------------------


def decide(history, probabilities, uniform_proba):

    random_number = random.random()

    if uniform_proba > random_number:
        history = []

    history = get_string(history)

    total_sum = sum(probabilities[history].values())

    random_number = random.uniform(0, total_sum)

    current_sum = 0

    for key, value in probabilities[history].items():
        current_sum += value

        if current_sum >= random_number:
            return key

def print_result(args, result):
     if args.output_file is None:
            print(result)
     else:
            with open(args.output_file, "w") as write_file:
                write_file.write(result)

def generate(args, probabilities, history = []):

    depth = args.depth
    len_of_generating_text = args.number_of_tokens
    uniform_proba = args.uniform_proba

    #history = []
    result = []

    for i in range(len_of_generating_text):

        key = get_string(history)
        while (len(history) > depth or
               key not in probabilities.keys() or 
               len(probabilities[key]) == 0):
           history = history[1:]
           key = key[1:]
           key = key.lstrip()

        new_item = decide(history, probabilities, uniform_proba)

        history.append(new_item)
        result.append(new_item)

    result = final_format(get_string(result))
    print_result(args, result)
    return result, history


# -----------------------------------------------------------------------
# ------------------------MAIN-------------------------------------------
# -----------------------------------------------------------------------


def calculate_probabilities(args):

    tokens_list = read_initial_text(args.input_file, args)

    probabilities = collections.defaultdict(lambda: collections.defaultdict(int))
    
    calculate_all_len_tokens(args.depth, tokens_list, probabilities)

    with open(args.probabilities_file, "w") as write_file:
        json.dump(probabilities, write_file)


def generate_text(args):

    #probabilities = collections.defaultdict(lambda: collections.defaultdict(int))

    with open(args.probabilities_file, "r") as read_file:
        probabilities = json.load(read_file)

    history = []

    generate(args, 
             probabilities, 
             history)

    while (True):
      
        total_input = str(input())

        try:
            next_command, new_args = total_input.split(maxsplit = 1)
        except:
            next_command = total_input
            new_args = ""

        next_command = next_command.lstrip()
        next_command= next_command.rstrip()


        if next_command == '--help':
            with open("help.txt") as file:
                ans = file.read()
                print(ans)
            

        elif next_command == 'generate':
            args.number_of_tokens = (0 if new_args == "" else int(new_args))
            history = generate(args, 
                               probabilities, 
                               history)[1]

        elif next_command == 'clear':
            history = []

        elif next_command == 'set_history':
            history = new_args.split()
            #history = tuple(re.findall(args.mask, new_history))
        elif next_command == 'observe_history':
            print(history)

        elif next_command == 'change_depth':
            new_depth = int(new_args)
            args.depth = new_depth

        elif next_command == "probabilities":
            str_history = get_string(history)

            while (len(history) > args.depth or
                   str_history not in probabilities.keys() or 
                   len(probabilities[str_history]) == 0):
                       history = history[1:]
                       str_history = str_history[1:]
                       str_history = str_history.lstrip()

            list_items = list(probabilities[str_history].items())
            list_items.sort(key=lambda i: i[1])

            total_sum = sum(probabilities[str_history].values())

            for key, val in list_items:
                print(key, end=": ")
                print(val / total_sum)

        elif next_command == "finish":
            break
        else:
            print("Incorrect command. Use --help and try again")


parser = argparse.ArgumentParser(description='Parser')
subparsers = parser.add_subparsers(help='sub-command help')

parser_probab = subparsers.add_parser('calculate_probabilities',
                                      help='for colculating probabilities')

parser_probab.add_argument('--mask', 
                            type=str, 
                            default="\w+|[{string.punctuation}]")

parser_probab.add_argument('--input_file',
                           help='file name with text, more than 10000 words')

parser_probab.add_argument('--probabilities_file',
                           help='file name where dict' +
                                ' with probabilities will be writen. (.json)')

parser_probab.add_argument('--depth', type=int,
                           help='maximal depth for tokens')

parser_probab.set_defaults(func=calculate_probabilities)

parser_gen = subparsers.add_parser('generate_text',
                                   help='for generating random text')

parser_gen.add_argument('--probabilities_file',
                        help='File name where dict with probabilities is.' +
                             ' It must be .json')

parser_gen.add_argument('--depth', type=int, default=0,
                        help='maximal depth for tokens')

parser_gen.add_argument('--number_of_tokens', type=int, default=0,
                        help='number_of_tokens')

parser_gen.add_argument('--uniform_proba', default=0, type=float,
                        help='with uniform_proba probability we ' +
                             'schoose new token' +
                             ' from all ignoring depth-1 last ones')

parser_gen.add_argument('--output_file',
                        help='(Optional, defaul terminal). ' +
                             'File name where generated text will' +
                             'be written. (.txt)')

parser_gen.set_defaults(func=generate_text)

args = parser.parse_args('generate_text --probabilities_file probabilities.json --depth 2 --number_of_tokens 15'.split())
#args = parser.parse_args('calculate_probabilities --mask \d+ --input_file text.txt --probabilities_file probabilities.json --depth 2'.split())

# args = parser.parse_args()
args.func(args)
